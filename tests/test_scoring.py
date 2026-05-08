from founder_retention_expansion.config import load_company_config, load_scoring_config
from founder_retention_expansion.ingest import load_accounts
from founder_retention_expansion.scoring import (
    SCORECARD_COLUMNS,
    build_customer_health_scorecard,
    build_scored_accounts,
)


def test_scorecard_columns_and_sorting():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    scored = build_scored_accounts(accounts, company_config, scoring_config)

    scorecard = build_customer_health_scorecard(scored)

    assert list(scorecard.columns) == SCORECARD_COLUMNS
    assert scorecard["founder_attention_score"].iloc[0] >= scorecard["founder_attention_score"].iloc[-1]
