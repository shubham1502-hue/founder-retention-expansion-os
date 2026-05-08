from pathlib import Path

from founder_retention_expansion.config import load_company_config, load_scoring_config
from founder_retention_expansion.ingest import load_accounts
from founder_retention_expansion.reporting import (
    build_account_score_explanations,
    build_churn_driver_summary,
    build_customer_proof_opportunities,
    generate_outputs,
)
from founder_retention_expansion.scoring import build_scored_accounts


def test_churn_driver_summary_generation():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    scored = build_scored_accounts(accounts, company_config, scoring_config)

    summary = build_churn_driver_summary(scored)

    assert not summary.empty
    assert "estimated_revenue_at_risk" in summary.columns


def test_proof_opportunity_detection():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    scored = build_scored_accounts(accounts, company_config, scoring_config)

    proof = build_customer_proof_opportunities(scored)

    assert not proof.empty
    assert "proof_angle" in proof.columns


def test_score_explanations_include_recommendations():
    accounts = load_accounts("data/sample_customer_accounts.csv")
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")
    scored = build_scored_accounts(accounts, company_config, scoring_config)

    explanations = build_account_score_explanations(scored)

    assert "recommended_next_action" in explanations.columns
    assert explanations["score_interpretation"].str.contains("Health").all()


def test_memo_generation(tmp_path: Path):
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")

    files = generate_outputs(
        "data/sample_customer_accounts.csv",
        company_config,
        scoring_config,
        tmp_path,
    )

    memo = files["founder_memo"].read_text(encoding="utf-8")

    assert "## Executive summary" in memo
    assert "## Recommended next 7-day actions" in memo
    assert files["scorecard"].exists()
