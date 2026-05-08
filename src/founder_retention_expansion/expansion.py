"""Expansion readiness and customer proof logic."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .health import (
    active_user_ratio_score,
    critical_ticket_score,
    nps_health_score,
    payment_status_score,
    product_gap_health_score,
    support_ticket_score,
    usage_trend_score,
)
from .retention import churn_risk_signal_score, risk_from_positive_score
from .utils import clamp, normalize_text, weighted_average


def expansion_signal_score(value: Any) -> float:
    """Return expansion signal strength."""
    text = normalize_text(value)
    mapping = {
        "upsell requested": 100,
        "more seats requested": 95,
        "product-led expansion signal": 90,
        "usage growth": 85,
        "new team interested": 80,
        "champion asks roadmap": 75,
        "mild interest": 65,
        "none": 35,
        "not yet": 30,
        "budget concern": 15,
        "churn risk": 0,
    }
    return mapping.get(text, 35)


def reference_potential_score(value: Any) -> float:
    """Return customer proof potential score."""
    text = normalize_text(value)
    mapping = {
        "high": 100,
        "champion": 100,
        "medium": 65,
        "low": 25,
        "none": 0,
        "not now": 10,
    }
    return mapping.get(text, 30)


def case_study_potential_score(value: Any) -> float:
    """Return case study potential score."""
    return reference_potential_score(value)


def calculate_expansion_readiness_score(
    row: pd.Series,
    scoring_config: dict[str, Any],
) -> int:
    """Calculate whether an account is ready for expansion."""
    weights = scoring_config["weights"]
    factors = {
        "usage_trend": usage_trend_score(row.get("usage_trend")),
        "product_adoption_score": clamp(float(row.get("product_adoption_score", 0))),
        "active_user_ratio": active_user_ratio_score(float(row.get("active_user_ratio", 0))),
        "support_ticket_load": support_ticket_score(int(row.get("support_tickets_open", 0))),
        "critical_ticket_load": critical_ticket_score(int(row.get("critical_tickets_open", 0))),
        "nps_score": nps_health_score(row.get("nps_score")),
        "payment_status": payment_status_score(row.get("payment_status")),
        "product_gap_severity": product_gap_health_score(row.get("product_gap")),
        "churn_risk_signal": 100 - churn_risk_signal_score(row.get("churn_risk_signal")),
        "expansion_signal": expansion_signal_score(row.get("expansion_signal")),
    }
    score = weighted_average(factors, weights)

    if row.get("customer_health_score", 100) < 60:
        score = min(score, 35)
    if row.get("retention_risk_score", 0) >= 70:
        score = min(score, 30)
    if normalize_text(row.get("expansion_signal")) in {"none", "not yet", ""}:
        score = min(score, 55)
    if risk_from_positive_score(product_gap_health_score(row.get("product_gap"))) >= 70:
        score = min(score, 50)
    return int(round(clamp(score)))


def expansion_category(row: pd.Series) -> str:
    """Convert expansion readiness score into a category."""
    score = float(row.get("expansion_readiness_score", 0))
    if row.get("retention_risk_score", 0) >= 70 or row.get("customer_health_score", 0) < 50:
        return "Do not expand"
    if score >= 80:
        return "Expansion-ready"
    if score >= 60:
        return "Expansion candidate"
    if score >= 35:
        return "Not yet"
    return "Do not expand"


def calculate_reference_readiness_score(
    row: pd.Series,
    scoring_config: dict[str, Any],
) -> int:
    """Calculate readiness for references, champions, or case studies."""
    weights = scoring_config["weights"]
    factors = {
        "reference_potential": reference_potential_score(row.get("reference_potential")),
        "expansion_signal": expansion_signal_score(row.get("expansion_signal")),
        "nps_score": nps_health_score(row.get("nps_score")),
        "usage_trend": usage_trend_score(row.get("usage_trend")),
        "product_adoption_score": clamp(float(row.get("product_adoption_score", 0))),
        "active_user_ratio": active_user_ratio_score(float(row.get("active_user_ratio", 0))),
    }
    score = weighted_average(factors, weights)
    score = max(score, case_study_potential_score(row.get("case_study_potential")) * 0.8)
    if row.get("customer_health_score", 100) < 70 or row.get("retention_risk_score", 0) >= 50:
        score = min(score, 45)
    return int(round(clamp(score)))


def suggested_expansion_motion(row: pd.Series) -> str:
    """Return the most likely expansion motion."""
    signal = normalize_text(row.get("expansion_signal"))
    if signal in {"more seats requested", "product-led expansion signal"}:
        return "Seat expansion discovery with account owner and CS."
    if signal == "upsell requested":
        return "Package upgrade proposal with success proof."
    if signal in {"usage growth", "new team interested"}:
        return "Map new team use case and quantify incremental value."
    if signal == "champion asks roadmap":
        return "Use roadmap conversation to validate expansion use case."
    return "Confirm value proof before starting expansion motion."


def proof_angle(row: pd.Series) -> str:
    """Return the customer proof angle."""
    industry = row.get("industry")
    if row.get("case_study_potential") in {"High", "high", "Champion", "champion"}:
        return f"Case study on retained value in {industry}."
    if row.get("reference_potential") in {"High", "high", "Champion", "champion"}:
        return f"Reference for {row.get('segment')} customers."
    if normalize_text(row.get("expansion_signal")) in {
        "usage growth",
        "more seats requested",
        "product-led expansion signal",
    }:
        return "Expansion story with usage growth proof."
    return "Customer proof after next value review."
