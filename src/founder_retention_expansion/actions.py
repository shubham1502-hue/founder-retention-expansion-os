"""Founder attention and action generation."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .expansion import (
    expansion_signal_score,
    reference_potential_score,
    suggested_expansion_motion,
)
from .retention import (
    churn_risk_signal_score,
    contract_value_risk,
    renewal_proximity_risk,
)
from .utils import clean_text, format_currency, normalize_text, weighted_average


def founder_attention_category(score: float) -> str:
    """Convert founder attention score to a queue category."""
    if score >= 85:
        return "Founder intervention now"
    if score >= 65:
        return "Executive review this week"
    if score >= 40:
        return "Owner follow-up"
    if score >= 20:
        return "Monitor"
    return "No action needed"


def calculate_founder_attention_score(
    row: pd.Series,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> int:
    """Score founder attention need as a weighted risk and leverage score."""
    weights = scoring_config["weights"]
    high_value_threshold = float(company_config["high_value_threshold"])
    health_score = float(row.get("customer_health_score", 100))
    retention_risk = float(row.get("retention_risk_score", 0))
    expansion_score = float(row.get("expansion_readiness_score", 0))
    founder_need = max(retention_risk, 100 - health_score)

    if float(row.get("contract_value", 0)) >= high_value_threshold and retention_risk >= 50:
        founder_need = max(founder_need, 88)
    if churn_risk_signal_score(row.get("churn_risk_signal")) >= 85:
        founder_need = max(founder_need, 92)
    if normalize_text(row.get("stakeholder_change")) in {
        "champion left",
        "executive sponsor left",
        "buyer changed",
    }:
        founder_need = max(founder_need, 70)
    if expansion_score >= 80 and float(row.get("contract_value", 0)) >= high_value_threshold:
        founder_need = max(founder_need, 68)

    value_score = contract_value_risk(row, high_value_threshold)
    factors = {
        "founder_attention_need": founder_need,
        "contract_value": value_score,
        "renewal_proximity": renewal_proximity_risk(row.get("days_to_renewal")),
        "churn_risk_signal": churn_risk_signal_score(row.get("churn_risk_signal")),
        "expansion_signal": expansion_signal_score(row.get("expansion_signal")),
        "reference_potential": reference_potential_score(row.get("reference_potential")),
    }
    score = weighted_average(factors, weights)
    if founder_need >= 90:
        score = max(score, 88)
    if float(row.get("contract_value", 0)) >= high_value_threshold and row.get(
        "retention_risk_category"
    ) in {"At risk", "Critical"}:
        score = max(score, 82)
    return int(round(max(0, min(100, score))))


def primary_owner(row: pd.Series) -> str:
    """Choose the best currently accountable owner."""
    for field in ["customer_success_owner", "account_owner", "executive_sponsor"]:
        owner = clean_text(row.get(field))
        if owner:
            return owner
    return "Founder"


def recommended_next_action(row: pd.Series, company_config: dict[str, Any]) -> str:
    """Return the most important next action for an account."""
    churn_signal = normalize_text(row.get("churn_risk_signal"))
    product_gap = normalize_text(row.get("product_gap"))
    payment_status = normalize_text(row.get("payment_status"))
    stakeholder_change = normalize_text(row.get("stakeholder_change"))

    if row.get("founder_attention_category") == "Founder intervention now":
        return "Founder should contact the executive sponsor and reset the retention plan."
    if row.get("retention_risk_category") == "Critical":
        return "Create a save plan with owner, customer sponsor, risk driver, and due date."
    if row.get("days_to_renewal") is not None and row.get("days_to_renewal") <= 60:
        if row.get("retention_risk_category") in {"At risk", "Watch"}:
            return "Run renewal value proof review and confirm renewal owner."
    if payment_status in {"overdue", "unpaid", "payment failed"}:
        return "Resolve payment status with finance and customer sponsor."
    if stakeholder_change in {"champion left", "executive sponsor left", "buyer changed"}:
        return "Rebuild stakeholder map and secure a new executive sponsor."
    if product_gap in {"critical missing feature", "compliance blocker", "repeated product gap"}:
        return "Align product and CS on a customer-facing product gap plan."
    if row.get("expansion_category") == "Expansion-ready":
        return suggested_expansion_motion(row)
    if row.get("days_since_last_touchpoint") is None or row.get("days_since_last_touchpoint") > 21:
        return "Schedule a customer touchpoint and document value proof."
    if row.get("reference_readiness_score", 0) >= 75:
        return "Ask for reference or case study after confirming customer value proof."
    if churn_signal in {"watch", "usage concern", "budget concern"}:
        return "Run a success plan review around the main churn signal."
    return "Monitor account and keep health signals current."


def risk_reason(row: pd.Series) -> str:
    """Summarize why an account needs attention."""
    reasons: list[str] = []
    if float(row.get("contract_value", 0)) >= 75000:
        reasons.append("High-value account")
    if row.get("retention_risk_category") in {"At risk", "Critical"}:
        reasons.append(f"{row.get('retention_risk_category')} retention risk")
    if row.get("health_category") in {"At risk", "Critical"}:
        reasons.append(f"{row.get('health_category')} customer health")
    if row.get("days_to_renewal") is not None and row.get("days_to_renewal") <= 90:
        reasons.append(f"Renewal in {row.get('days_to_renewal')} days")
    for field in ["churn_risk_signal", "renewal_risk_signal", "product_gap", "stakeholder_change"]:
        value = clean_text(row.get(field))
        if normalize_text(value) not in {"", "none", "no", "no risk", "stable", "no gap"}:
            reasons.append(value)
    if row.get("expansion_category") == "Expansion-ready":
        reasons.append("Expansion-ready")
    return "; ".join(reasons[:5]) or "Needs weekly review"


def founder_action(row: pd.Series) -> str:
    """Return the founder-level action."""
    if row.get("retention_risk_category") == "Critical":
        return "Founder or executive sponsor call to reset value and renewal path."
    if churn_risk_signal_score(row.get("churn_risk_signal")) >= 75:
        return "Escalate churn driver and confirm customer save plan."
    if normalize_text(row.get("stakeholder_change")) in {"champion left", "executive sponsor left"}:
        return "Use executive touch to rebuild sponsorship."
    if row.get("expansion_category") == "Expansion-ready":
        return "Review expansion motion and approve customer-facing ask."
    if row.get("reference_readiness_score", 0) >= 75:
        return "Approve reference or case study ask."
    return "Review customer health and assign the highest leverage owner action."


def due_timing(row: pd.Series) -> str:
    """Return timing for the founder queue."""
    category = row.get("founder_attention_category")
    if category == "Founder intervention now":
        return "Today"
    if category == "Executive review this week":
        return "This week"
    if category == "Owner follow-up":
        return "Next 3 business days"
    return "Next review"


def expected_leverage(row: pd.Series) -> str:
    """Describe why action is worth taking."""
    value = format_currency(row.get("contract_value", 0))
    if row.get("retention_risk_category") in {"At risk", "Critical"}:
        return f"Protects {value} in renewal or retention risk."
    if row.get("expansion_category") == "Expansion-ready":
        return f"Can turn {value} account into expansion pipeline."
    if row.get("reference_readiness_score", 0) >= 75:
        return "Creates customer proof for sales and investor narrative."
    return "Keeps customer health visible before renewal risk grows."


def escalation_note(row: pd.Series) -> str:
    """Return escalation note for founder attention queue."""
    if row.get("founder_attention_category") == "Founder intervention now":
        return "Do not wait for the next weekly review."
    if row.get("retention_risk_category") == "Critical":
        return "Needs a named save plan and customer-facing owner."
    if row.get("expansion_category") == "Expansion-ready":
        return "Confirm expansion timing before making a commercial ask."
    return "Review in weekly retention and expansion operating review."


def risk_or_opportunity(row: pd.Series) -> str:
    """Classify attention item as risk or opportunity."""
    if row.get("retention_risk_category") in {"At risk", "Critical"}:
        return "Retention risk"
    if row.get("expansion_category") in {"Expansion-ready", "Expansion candidate"}:
        return "Expansion opportunity"
    if row.get("reference_readiness_score", 0) >= 75:
        return "Customer proof opportunity"
    return "Customer health watch"


def build_founder_attention_queue(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Build a ranked founder intervention queue."""
    queue = scored_accounts[
        scored_accounts["founder_attention_category"].isin(
            ["Founder intervention now", "Executive review this week", "Owner follow-up"]
        )
    ].copy()
    queue = queue.sort_values(
        by=["founder_attention_score", "retention_risk_score", "contract_value"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    queue["priority_rank"] = queue.index + 1
    queue["risk_or_opportunity"] = queue.apply(risk_or_opportunity, axis=1)
    queue["reason"] = queue.apply(risk_reason, axis=1)
    queue["founder_action"] = queue.apply(founder_action, axis=1)
    queue["owner"] = queue.apply(primary_owner, axis=1)
    queue["due_timing"] = queue.apply(due_timing, axis=1)
    queue["escalation_note"] = queue.apply(escalation_note, axis=1)
    return queue[
        [
            "priority_rank",
            "account_id",
            "customer_name",
            "contract_value",
            "risk_or_opportunity",
            "reason",
            "founder_action",
            "owner",
            "due_timing",
            "escalation_note",
        ]
    ]
