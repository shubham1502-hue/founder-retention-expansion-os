from founder_retention_expansion.actions import build_founder_attention_queue
from founder_retention_expansion.config import load_company_config, load_scoring_config
from founder_retention_expansion.ingest import load_accounts
from founder_retention_expansion.scoring import build_scored_accounts


def test_founder_attention_queue_generation():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    scored = build_scored_accounts(accounts, company_config, scoring_config)

    queue = build_founder_attention_queue(scored)

    assert not queue.empty
    assert queue.iloc[0]["priority_rank"] == 1
    assert "founder_action" in queue.columns
    assert "owner" in queue.columns
