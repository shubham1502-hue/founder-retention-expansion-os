"""Retention and renewal risk logic."""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from .health import (
    active_user_ratio,
    business_review_recency_score,
    calculate_customer_health_score,
    critical_ticket_score,
    health_category,
    nps_health_score,
    payment_status_score,
    product_gap_health_score,
    stakeholder_change_score,
    support_ticket_score,
    touchpoint_recency_score,
    usage_trend_score,
)
from .utils import clamp, days_between, normalize_text, weighted_average


def retention_risk_category(score: float) -> str:
    """Convert retention risk score into a category."""
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "At risk"
    if score >= 35:
        return "Watch"
    return "Low risk"


def renewal_proximity_risk(days_to_renewal: int | None) -> float:
    """Return higher risk as renewal gets closer."""
    if days_to_renewal is None:
        return 45
    if days_to_renewal < 0:
        return 90
    if days_to_renewal <= 30:
        return 85
    if days_to_renewal <= 60:
        return 70
    if days_to_renewal <= 90:
        return 50
    if days_to_renewal <= 180:
        return 30
    return 15


def churn_risk_signal_score(value: Any) -> float:
    """Return a risk score from churn risk signal."""
    text = normalize_text(value)
    mapping = {
        "none": 0,
        "no risk": 0,
        "watch": 35,
        "usage concern": 55,
        "budget concern": 65,
        "competitive evaluation": 75,
        "churn risk": 90,
        "cancellation threat": 100,
    }
    return mapping.get(text, 25)


def renewal_risk_signal_score(value: Any) -> float:
    """Return a risk score from renewal risk signal."""
    text = normalize_text(value)
    mapping = {
        "none": 0,
        "no risk": 0,
        "expansion potential": 5,
        "watch": 40,
        "unclear value proof": 60,
        "budget concern": 70,
        "stakeholder concern": 70,
        "renewal risk": 85,
        "churn risk": 95,
    }
    return mapping.get(text, 25)


def risk_from_positive_score(score: float) -> float:
    """Convert a positive score into a risk score."""
    return clamp(100 - score)


def contract_value_risk(row: pd.Series, high_value_threshold: float) -> float:
    """Increase attention when high-value accounts have risk."""
    value = float(row.get("contract_value", 0))
    risk = float(row.get("retention_risk_score", 0))
    if value >= high_value_threshold and risk >= 60:
        return 100
    if value >= high_value_threshold and risk >= 35:
        return 75
    if value >= high_value_threshold:
        return 45
    if value >= high_value_threshold * 0.6 and risk >= 60:
        return 65
    return 20


def calculate_retention_risk_score(
    row: pd.Series,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> int:
    """Calculate renewal and retention risk where higher means more risk."""
    weights = scoring_config["weights"]
    factors = {
        "usage_trend": risk_from_positive_score(usage_trend_score(row.get("usage_trend"))),
        "product_adoption_score": risk_from_positive_score(
            float(row.get("product_adoption_score", 0))
        ),
        "active_user_ratio": risk_from_positive_score(
            float(row.get("active_user_ratio", 0)) * 100
        ),
        "support_ticket_load": risk_from_positive_score(
            support_ticket_score(int(row.get("support_tickets_open", 0)))
        ),
        "critical_ticket_load": risk_from_positive_score(
            critical_ticket_score(int(row.get("critical_tickets_open", 0)))
        ),
        "nps_score": risk_from_positive_score(nps_health_score(row.get("nps_score"))),
        "days_since_last_touchpoint": risk_from_positive_score(
            touchpoint_recency_score(row.get("days_since_last_touchpoint"))
        ),
        "days_since_last_business_review": risk_from_positive_score(
            business_review_recency_score(row.get("days_since_last_business_review"))
        ),
        "stakeholder_change": risk_from_positive_score(
            stakeholder_change_score(row.get("stakeholder_change"))
        ),
        "payment_status": risk_from_positive_score(payment_status_score(row.get("payment_status"))),
        "product_gap_severity": risk_from_positive_score(
            product_gap_health_score(row.get("product_gap"))
        ),
        "renewal_proximity": renewal_proximity_risk(row.get("days_to_renewal")),
        "churn_risk_signal": churn_risk_signal_score(row.get("churn_risk_signal")),
    }
    score = weighted_average(factors, weights)
    score = max(score, renewal_risk_signal_score(row.get("renewal_risk_signal")))

    high_value_threshold = float(company_config["high_value_threshold"])
    if float(row.get("contract_value", 0)) >= high_value_threshold and score >= 50:
        score = max(score, 72)
    if row.get("days_to_renewal") is not None and row.get("days_to_renewal") <= 45:
        if row.get("customer_health_score", 100) < 65:
            score = max(score, 78)
    if normalize_text(row.get("payment_status")) in {"overdue", "unpaid", "payment failed"}:
        score = max(score, 70)
    return int(round(clamp(score)))


def enrich_accounts(
    accounts: pd.DataFrame,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> pd.DataFrame:
    """Add calculated health, retention, expansion, and attention fields."""
    from .actions import calculate_founder_attention_score, founder_attention_category
    from .expansion import (
        calculate_expansion_readiness_score,
        calculate_reference_readiness_score,
        expansion_category,
    )

    df = accounts.copy()
    analysis_date = company_config.get("analysis_date") or date.today()

    df["active_user_ratio"] = df.apply(active_user_ratio, axis=1)
    df["days_to_renewal"] = df["renewal_date"].apply(
        lambda value: days_between(analysis_date, value.date()) if pd.notna(value) else None
    )
    df["days_since_last_touchpoint"] = df["last_customer_touchpoint_date"].apply(
        lambda value: days_between(value.date(), analysis_date) if pd.notna(value) else None
    )
    df["days_since_last_business_review"] = df["last_business_review_date"].apply(
        lambda value: days_between(value.date(), analysis_date) if pd.notna(value) else None
    )
    df["customer_health_score"] = df.apply(
        lambda row: calculate_customer_health_score(row, scoring_config),
        axis=1,
    )
    df["health_category"] = df["customer_health_score"].apply(health_category)
    df["retention_risk_score"] = df.apply(
        lambda row: calculate_retention_risk_score(row, company_config, scoring_config),
        axis=1,
    )
    df["retention_risk_category"] = df["retention_risk_score"].apply(retention_risk_category)
    df["expansion_readiness_score"] = df.apply(
        lambda row: calculate_expansion_readiness_score(row, scoring_config),
        axis=1,
    )
    df["expansion_category"] = df.apply(expansion_category, axis=1)
    df["reference_readiness_score"] = df.apply(
        lambda row: calculate_reference_readiness_score(row, scoring_config),
        axis=1,
    )
    df["founder_attention_score"] = df.apply(
        lambda row: calculate_founder_attention_score(row, company_config, scoring_config),
        axis=1,
    )
    df["founder_attention_category"] = df["founder_attention_score"].apply(
        founder_attention_category
    )
    return df
