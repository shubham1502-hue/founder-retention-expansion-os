"""Scorecard assembly."""

from __future__ import annotations

from typing import Any

import pandas as pd

from .retention import enrich_accounts


SCORECARD_COLUMNS = [
    "account_id",
    "customer_name",
    "segment",
    "contract_value",
    "renewal_date",
    "customer_health_score",
    "health_category",
    "retention_risk_score",
    "retention_risk_category",
    "expansion_readiness_score",
    "expansion_category",
    "founder_attention_score",
    "founder_attention_category",
    "recommended_next_action",
]


def build_scored_accounts(
    accounts: pd.DataFrame,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
) -> pd.DataFrame:
    """Return accounts with all calculated scores and recommended actions."""
    from .actions import recommended_next_action

    scored = enrich_accounts(accounts, company_config, scoring_config)
    scored["recommended_next_action"] = scored.apply(
        lambda row: recommended_next_action(row, company_config),
        axis=1,
    )
    return scored


def build_customer_health_scorecard(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Return the founder-facing customer health scorecard."""
    return scored_accounts[SCORECARD_COLUMNS].sort_values(
        by=["founder_attention_score", "retention_risk_score", "contract_value"],
        ascending=[False, False, False],
    )
