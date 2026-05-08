import pandas as pd

from founder_retention_expansion.health import (
    active_user_ratio,
    calculate_customer_health_score,
    health_category,
)
from founder_retention_expansion.ingest import load_accounts
from founder_retention_expansion.config import load_company_config, load_scoring_config
from founder_retention_expansion.scoring import build_scored_accounts


def test_active_user_ratio_calculation():
    row = pd.Series({"active_users": 25, "licensed_users": 100})

    assert active_user_ratio(row) == 0.25


def test_active_user_ratio_handles_zero_licensed_users():
    row = pd.Series({"active_users": 10, "licensed_users": 0})

    assert active_user_ratio(row) == 0.0


def test_health_score_boundaries():
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    row = pd.Series(
        {
            "usage_trend": "growing",
            "product_adoption_score": 100,
            "active_user_ratio": 1.0,
            "support_tickets_open": 0,
            "critical_tickets_open": 0,
            "nps_score": 100,
            "days_since_last_touchpoint": 1,
            "days_since_last_business_review": 10,
            "stakeholder_change": "none",
            "payment_status": "current",
            "product_gap": "none",
            "churn_risk_signal": "none",
        }
    )

    score = calculate_customer_health_score(row, scoring_config)

    assert 0 <= score <= 100
    assert health_category(score) == "Healthy"


def test_scored_accounts_add_health_fields():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")

    scored = build_scored_accounts(accounts, company_config, scoring_config)

    assert scored["customer_health_score"].between(0, 100).all()
    assert "health_category" in scored.columns
