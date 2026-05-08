from founder_retention_expansion.config import load_company_config, load_scoring_config
from founder_retention_expansion.ingest import load_accounts
from founder_retention_expansion.retention import (
    calculate_retention_risk_score,
    renewal_proximity_risk,
    retention_risk_category,
)
from founder_retention_expansion.scoring import build_scored_accounts


def test_renewal_proximity_risk_increases_near_renewal():
    assert renewal_proximity_risk(20) > renewal_proximity_risk(200)


def test_retention_risk_logic_flags_churn_account():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    scored = build_scored_accounts(accounts, company_config, scoring_config)
    account = scored[scored["account_id"] == "A025"].iloc[0]

    assert account["retention_risk_category"] in {"At risk", "Critical"}
    assert account["founder_attention_category"] == "Founder intervention now"


def test_retention_score_boundary():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    row = build_scored_accounts(accounts, company_config, scoring_config).iloc[0]

    score = calculate_retention_risk_score(row, company_config, scoring_config)

    assert 0 <= score <= 100
    assert retention_risk_category(score) in {"Low risk", "Watch", "At risk", "Critical"}
