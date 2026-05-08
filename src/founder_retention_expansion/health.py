"""Customer health scoring logic."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .utils import clamp, normalize_text, weighted_average


def active_user_ratio(row: pd.Series) -> float:
    """Return active users divided by licensed users."""
    licensed_users = float(row.get("licensed_users", 0))
    active_users = float(row.get("active_users", 0))
    if licensed_users <= 0:
        return 0.0
    return round(clamp(active_users / licensed_users, 0, 1), 4)


def active_user_ratio_score(value: float) -> float:
    """Convert active user ratio into a 0 to 100 score."""
    return clamp(float(value) * 100)


def health_category(score: float) -> str:
    """Convert a 0 to 100 health score into a founder-readable category."""
    if score >= 80:
        return "Healthy"
    if score >= 60:
        return "Watch"
    if score >= 40:
        return "At risk"
    return "Critical"


def usage_trend_score(value: Any) -> float:
    """Return a positive health score from usage trend."""
    text = normalize_text(value)
    mapping = {
        "growing": 100,
        "expanding": 100,
        "healthy": 95,
        "stable": 85,
        "flat": 75,
        "spiky": 65,
        "low": 45,
        "declining": 30,
        "inactive": 10,
    }
    return mapping.get(text, 60)


def support_ticket_score(open_tickets: int) -> float:
    """Return a positive health score from support ticket load."""
    if open_tickets <= 0:
        return 100
    if open_tickets <= 2:
        return 85
    if open_tickets <= 5:
        return 65
    if open_tickets <= 8:
        return 40
    return 20


def critical_ticket_score(open_tickets: int) -> float:
    """Return a positive health score from critical ticket load."""
    if open_tickets <= 0:
        return 100
    if open_tickets == 1:
        return 45
    if open_tickets == 2:
        return 25
    return 10


def nps_health_score(value: Any) -> float:
    """Convert NPS from -100 to 100 into a 0 to 100 score."""
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 50
    return clamp((score + 100) / 2)


def touchpoint_recency_score(days_since: int | None) -> float:
    """Return a positive score for customer touchpoint recency."""
    if days_since is None:
        return 35
    if days_since <= 7:
        return 100
    if days_since <= 14:
        return 85
    if days_since <= 30:
        return 65
    if days_since <= 45:
        return 40
    return 20


def business_review_recency_score(days_since: int | None) -> float:
    """Return a positive score for business review recency."""
    if days_since is None:
        return 35
    if days_since <= 45:
        return 100
    if days_since <= 90:
        return 80
    if days_since <= 180:
        return 50
    return 25


def stakeholder_change_score(value: Any) -> float:
    """Return a positive score for stakeholder continuity."""
    text = normalize_text(value)
    mapping = {
        "none": 100,
        "no": 100,
        "stable": 100,
        "new champion": 75,
        "new evaluator": 65,
        "buyer changed": 45,
        "procurement changed": 45,
        "champion left": 20,
        "executive sponsor left": 20,
    }
    return mapping.get(text, 65)


def payment_status_score(value: Any) -> float:
    """Return a positive health score from payment status."""
    text = normalize_text(value)
    mapping = {
        "current": 100,
        "paid": 100,
        "invoiced current": 90,
        "invoice pending": 70,
        "delayed": 45,
        "overdue": 25,
        "unpaid": 15,
        "payment failed": 10,
    }
    return mapping.get(text, 65)


def product_gap_health_score(value: Any) -> float:
    """Return a positive health score from product gap severity."""
    text = normalize_text(value)
    mapping = {
        "none": 100,
        "no gap": 100,
        "minor workflow gap": 80,
        "reporting gap": 65,
        "integration gap": 50,
        "admin workflow gap": 55,
        "data export gap": 50,
        "mobile gap": 55,
        "critical missing feature": 20,
        "compliance blocker": 15,
        "repeated product gap": 30,
    }
    return mapping.get(text, 60)


def churn_signal_health_score(value: Any) -> float:
    """Return a positive health score from churn signal."""
    text = normalize_text(value)
    mapping = {
        "none": 100,
        "no risk": 100,
        "watch": 70,
        "budget concern": 45,
        "competitive evaluation": 30,
        "usage concern": 35,
        "churn risk": 20,
        "cancellation threat": 10,
    }
    return mapping.get(text, 75)


def calculate_customer_health_score(
    row: pd.Series,
    scoring_config: dict[str, Any],
) -> int:
    """Calculate a transparent weighted customer health score."""
    weights = scoring_config["weights"]
    factors = {
        "usage_trend": usage_trend_score(row.get("usage_trend")),
        "product_adoption_score": clamp(float(row.get("product_adoption_score", 0))),
        "active_user_ratio": active_user_ratio_score(float(row.get("active_user_ratio", 0))),
        "support_ticket_load": support_ticket_score(int(row.get("support_tickets_open", 0))),
        "critical_ticket_load": critical_ticket_score(int(row.get("critical_tickets_open", 0))),
        "nps_score": nps_health_score(row.get("nps_score")),
        "days_since_last_touchpoint": touchpoint_recency_score(
            row.get("days_since_last_touchpoint")
        ),
        "days_since_last_business_review": business_review_recency_score(
            row.get("days_since_last_business_review")
        ),
        "stakeholder_change": stakeholder_change_score(row.get("stakeholder_change")),
        "payment_status": payment_status_score(row.get("payment_status")),
        "product_gap_severity": product_gap_health_score(row.get("product_gap")),
        "churn_risk_signal": churn_signal_health_score(row.get("churn_risk_signal")),
    }
    return int(round(clamp(weighted_average(factors, weights))))
