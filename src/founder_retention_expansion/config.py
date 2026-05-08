"""Configuration loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .utils import parse_date


REQUIRED_COMPANY_KEYS = {
    "company_name",
    "stage",
    "business_model",
    "retention_model",
    "renewal_cycle_days",
    "expansion_motion",
    "high_value_threshold",
    "founder_intervention_threshold",
    "health_score_thresholds",
    "target_segments",
    "customer_health_signals",
    "churn_risk_signals",
    "expansion_signals",
    "reference_signals",
    "escalation_rules",
    "owner_roles",
    "review_cadence",
    "tools_used",
    "sensitive_data_note",
}


REQUIRED_SCORING_WEIGHTS = {
    "usage_trend",
    "product_adoption_score",
    "active_user_ratio",
    "support_ticket_load",
    "critical_ticket_load",
    "nps_score",
    "days_since_last_touchpoint",
    "days_since_last_business_review",
    "stakeholder_change",
    "payment_status",
    "product_gap_severity",
    "renewal_proximity",
    "churn_risk_signal",
    "expansion_signal",
    "reference_potential",
    "contract_value",
    "founder_attention_need",
}


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file and return a dictionary."""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a YAML mapping: {config_path}")
    return data


def load_company_config(path: str | Path) -> dict[str, Any]:
    """Load and validate company profile configuration."""
    config = load_yaml(path)
    missing = sorted(REQUIRED_COMPANY_KEYS - set(config))
    if missing:
        raise ValueError("Company config missing required keys: " + ", ".join(missing))
    thresholds = config.get("health_score_thresholds")
    if not isinstance(thresholds, dict):
        raise ValueError("company_profile.yml must define health_score_thresholds")
    config["analysis_date"] = parse_date(config.get("analysis_date"))
    return config


def load_scoring_config(path: str | Path) -> dict[str, Any]:
    """Load and validate scoring rules configuration."""
    config = load_yaml(path)
    weights = config.get("weights", {})
    if not isinstance(weights, dict):
        raise ValueError("scoring_rules.yml must include a weights mapping")
    missing = sorted(REQUIRED_SCORING_WEIGHTS - set(weights))
    if missing:
        raise ValueError("Scoring config missing required weights: " + ", ".join(missing))
    return config
