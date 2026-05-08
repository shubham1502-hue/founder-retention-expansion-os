from founder_retention_expansion.config import load_company_config, load_scoring_config
from founder_retention_expansion.expansion import expansion_signal_score
from founder_retention_expansion.ingest import load_accounts
from founder_retention_expansion.reporting import build_expansion_opportunity_queue
from founder_retention_expansion.scoring import build_scored_accounts


def test_expansion_signal_score_orders_strong_signal():
    assert expansion_signal_score("upsell requested") > expansion_signal_score("none")


def test_expansion_readiness_logic_finds_ready_accounts():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    scored = build_scored_accounts(accounts, company_config, scoring_config)

    ready = scored[scored["expansion_category"] == "Expansion-ready"]

    assert not ready.empty
    assert ready["retention_risk_score"].lt(70).all()


def test_expansion_queue_generation():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    scored = build_scored_accounts(accounts, company_config, scoring_config)

    queue = build_expansion_opportunity_queue(scored)

    assert "suggested_expansion_motion" in queue.columns
    assert len(queue) > 0
