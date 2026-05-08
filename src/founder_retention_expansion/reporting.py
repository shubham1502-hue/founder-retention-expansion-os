"""Output generation for CSV and Markdown reports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .actions import (
    build_founder_attention_queue,
    expected_leverage,
    founder_action,
    primary_owner,
    risk_reason,
)
from .expansion import proof_angle, suggested_expansion_motion
from .scoring import build_customer_health_scorecard, build_scored_accounts
from .utils import clean_text, format_currency, join_names, normalize_text


def markdown_table(df: pd.DataFrame, columns: list[str], limit: int = 10) -> str:
    """Render a compact Markdown table."""
    if df.empty:
        return "No rows found.\n"
    display = df[columns].head(limit).copy()
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in display.iterrows():
        values = [markdown_value(column, row.get(column)) for column in columns]
        lines.append("| " + " | ".join(value.replace("|", "/") for value in values) + " |")
    return "\n".join(lines) + "\n"


def markdown_value(column: str, value: Any) -> str:
    """Return founder-readable display text for Markdown tables."""
    if pd.isna(value):
        return ""
    if isinstance(value, pd.Timestamp):
        return value.date().isoformat()
    if column in {"contract_value", "estimated_revenue_at_risk"}:
        return format_currency(value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return clean_text(value, "")


def build_renewal_risk_queue(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Build the renewal risk queue."""
    queue = scored_accounts[
        (scored_accounts["retention_risk_score"] >= 35)
        | (scored_accounts["days_to_renewal"].fillna(9999) <= 90)
    ].copy()
    queue = queue.sort_values(
        by=["retention_risk_score", "days_to_renewal", "contract_value"],
        ascending=[False, True, False],
    ).reset_index(drop=True)
    queue["priority_rank"] = queue.index + 1
    queue["risk_reason"] = queue.apply(risk_reason, axis=1)
    queue["owner"] = queue.apply(primary_owner, axis=1)
    queue["founder_action"] = queue.apply(founder_action, axis=1)
    queue["due_timing"] = queue["retention_risk_category"].map(
        {"Critical": "Today", "At risk": "This week", "Watch": "Next 2 weeks", "Low risk": "Next review"}
    )
    queue["expected_leverage"] = queue.apply(expected_leverage, axis=1)
    return queue[
        [
            "priority_rank",
            "account_id",
            "customer_name",
            "contract_value",
            "renewal_date",
            "days_to_renewal",
            "risk_reason",
            "owner",
            "founder_action",
            "due_timing",
            "expected_leverage",
        ]
    ]


def build_expansion_opportunity_queue(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Build the expansion opportunity queue."""
    queue = scored_accounts[
        scored_accounts["expansion_category"].isin(["Expansion-ready", "Expansion candidate"])
    ].copy()
    queue = queue.sort_values(
        by=["expansion_readiness_score", "contract_value"],
        ascending=[False, False],
    ).reset_index(drop=True)
    queue["priority_rank"] = queue.index + 1
    queue["suggested_expansion_motion"] = queue.apply(suggested_expansion_motion, axis=1)
    queue["owner"] = queue.apply(primary_owner, axis=1)
    queue["expected_leverage"] = queue.apply(expected_leverage, axis=1)
    return queue[
        [
            "priority_rank",
            "account_id",
            "customer_name",
            "contract_value",
            "expansion_signal",
            "expansion_readiness_score",
            "suggested_expansion_motion",
            "owner",
            "next_step",
            "expected_leverage",
        ]
    ]


CHURN_DRIVER_RULES = {
    "Declining usage": (
        lambda row: normalize_text(row.get("usage_trend")) in {"declining", "inactive", "low"},
        "Run adoption recovery plan with customer success owner.",
        "Customer Success",
    ),
    "Low product adoption": (
        lambda row: float(row.get("product_adoption_score", 0)) < 55,
        "Identify unused value drivers and rebuild success plan.",
        "Customer Success",
    ),
    "Low active user ratio": (
        lambda row: float(row.get("active_user_ratio", 0)) < 0.45,
        "Map inactive licensed users and run enablement push.",
        "Customer Success",
    ),
    "Support ticket load": (
        lambda row: int(row.get("support_tickets_open", 0)) >= 6,
        "Prioritize support closure by renewal and customer value.",
        "Support Lead",
    ),
    "Critical support tickets": (
        lambda row: int(row.get("critical_tickets_open", 0)) > 0,
        "Escalate critical tickets with owner and customer-facing timeline.",
        "Support Lead",
    ),
    "Product gap": (
        lambda row: normalize_text(row.get("product_gap"))
        not in {"", "none", "no gap", "minor workflow gap"},
        "Create a product gap response with scope, owner, and customer message.",
        "Product Lead",
    ),
    "Stakeholder change": (
        lambda row: normalize_text(row.get("stakeholder_change"))
        in {"buyer changed", "champion left", "executive sponsor left", "procurement changed"},
        "Rebuild stakeholder map and confirm executive sponsor.",
        "Account Owner",
    ),
    "Payment issue": (
        lambda row: normalize_text(row.get("payment_status"))
        in {"overdue", "unpaid", "payment failed", "delayed"},
        "Resolve billing path before renewal conversation.",
        "Finance or RevOps",
    ),
    "Renewal value proof unclear": (
        lambda row: normalize_text(row.get("renewal_risk_signal"))
        in {"unclear value proof", "renewal risk", "churn risk"},
        "Run renewal value proof review and document outcomes.",
        "Customer Success",
    ),
    "Churn risk signal": (
        lambda row: normalize_text(row.get("churn_risk_signal"))
        in {"usage concern", "budget concern", "competitive evaluation", "churn risk", "cancellation threat"},
        "Open save plan with commercial and product owner.",
        "Customer Success",
    ),
    "Stale touchpoint": (
        lambda row: row.get("days_since_last_touchpoint") is None
        or row.get("days_since_last_touchpoint") > 21,
        "Set customer touchpoint SLA and review stale accounts weekly.",
        "Customer Success",
    ),
    "Stale business review": (
        lambda row: row.get("days_since_last_business_review") is None
        or row.get("days_since_last_business_review") > 120,
        "Schedule business review and confirm value proof.",
        "Customer Success",
    ),
}


def build_churn_driver_summary(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Summarize churn drivers across customer accounts."""
    rows: list[dict[str, Any]] = []
    for driver, (predicate, suggested_fix, owner_role) in CHURN_DRIVER_RULES.items():
        affected = scored_accounts[scored_accounts.apply(predicate, axis=1)]
        if affected.empty:
            continue
        rows.append(
            {
                "driver": driver,
                "count": int(len(affected)),
                "affected_accounts": join_names(affected["customer_name"].tolist()),
                "estimated_revenue_at_risk": int(affected["contract_value"].sum()),
                "suggested_fix": suggested_fix,
                "owner_role": owner_role,
            }
        )
    return pd.DataFrame(
        rows,
        columns=[
            "driver",
            "count",
            "affected_accounts",
            "estimated_revenue_at_risk",
            "suggested_fix",
            "owner_role",
        ],
    ).sort_values(by=["estimated_revenue_at_risk", "count"], ascending=[False, False])


def build_customer_proof_opportunities(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Build customer proof, reference, and case study opportunities."""
    proof = scored_accounts[
        (scored_accounts["reference_readiness_score"] >= 60)
        | (scored_accounts["reference_potential"].str.lower().isin(["high", "champion"]))
        | (scored_accounts["case_study_potential"].str.lower().isin(["high", "champion"]))
    ].copy()
    proof = proof[
        (proof["customer_health_score"] >= 70) & (proof["retention_risk_score"] < 55)
    ].copy()
    proof["proof_angle"] = proof.apply(proof_angle, axis=1)
    proof["owner"] = proof.apply(primary_owner, axis=1)
    proof["next_step"] = proof.apply(
        lambda row: "Confirm value proof and request reference or case study approval.",
        axis=1,
    )
    proof = proof.sort_values(
        by=["reference_readiness_score", "contract_value"],
        ascending=[False, False],
    )
    return proof[
        [
            "account_id",
            "customer_name",
            "reference_potential",
            "case_study_potential",
            "proof_angle",
            "owner",
            "next_step",
        ]
    ]


def health_score_drivers(row: pd.Series) -> str:
    """Summarize health score drivers."""
    drivers: list[str] = []
    if normalize_text(row.get("usage_trend")) in {"declining", "inactive", "low"}:
        drivers.append(f"Usage trend: {clean_text(row.get('usage_trend'))}")
    if float(row.get("product_adoption_score", 0)) < 60:
        drivers.append(f"Adoption score: {int(row.get('product_adoption_score'))}")
    if float(row.get("active_user_ratio", 0)) < 0.5:
        drivers.append(f"Active user ratio: {row.get('active_user_ratio')}")
    if int(row.get("critical_tickets_open", 0)) > 0:
        drivers.append(f"Critical tickets: {row.get('critical_tickets_open')}")
    if normalize_text(row.get("payment_status")) in {"overdue", "unpaid", "payment failed"}:
        drivers.append(f"Payment status: {clean_text(row.get('payment_status'))}")
    if not drivers:
        drivers.append("Healthy usage, adoption, support, and payment signals")
    return "; ".join(drivers[:5])


def retention_risk_drivers(row: pd.Series) -> str:
    """Summarize retention risk drivers."""
    drivers: list[str] = []
    if row.get("days_to_renewal") is not None and row.get("days_to_renewal") <= 90:
        drivers.append(f"Renewal in {row.get('days_to_renewal')} days")
    for field in ["renewal_risk_signal", "churn_risk_signal", "stakeholder_change", "product_gap"]:
        value = clean_text(row.get(field))
        if normalize_text(value) not in {"", "none", "no", "no risk", "stable", "no gap"}:
            drivers.append(value)
    if row.get("days_since_last_business_review") is None or row.get(
        "days_since_last_business_review"
    ) > 120:
        drivers.append("Stale business review")
    return "; ".join(drivers[:5]) or "No major renewal risk drivers"


def expansion_score_drivers(row: pd.Series) -> str:
    """Summarize expansion score drivers."""
    drivers: list[str] = []
    if row.get("expansion_category") in {"Expansion-ready", "Expansion candidate"}:
        drivers.append(clean_text(row.get("expansion_signal"), "Expansion signal"))
    if row.get("customer_health_score", 0) < 60:
        drivers.append("Health too low for expansion")
    if row.get("retention_risk_score", 0) >= 70:
        drivers.append("Retention risk blocks expansion")
    if row.get("product_adoption_score", 0) >= 80:
        drivers.append("Strong product adoption")
    return "; ".join(drivers[:5]) or "Expansion not yet supported by signals"


def founder_attention_drivers(row: pd.Series) -> str:
    """Summarize founder attention drivers."""
    drivers: list[str] = []
    if row.get("founder_attention_category") in {
        "Founder intervention now",
        "Executive review this week",
    }:
        drivers.append(row.get("founder_attention_category"))
    if float(row.get("contract_value", 0)) >= 75000:
        drivers.append("High-value account")
    if row.get("retention_risk_category") in {"At risk", "Critical"}:
        drivers.append(f"{row.get('retention_risk_category')} retention risk")
    if row.get("expansion_category") == "Expansion-ready":
        drivers.append("Expansion-ready")
    if row.get("reference_readiness_score", 0) >= 75:
        drivers.append("Customer proof opportunity")
    return "; ".join(drivers[:5]) or "Routine owner follow-up"


def score_interpretation(row: pd.Series) -> str:
    """Explain how a founder should read the scores."""
    return (
        f"Health {row.get('customer_health_score')} means {row.get('health_category')}. "
        f"Retention risk {row.get('retention_risk_score')} means {row.get('retention_risk_category')}. "
        f"Expansion {row.get('expansion_readiness_score')} means {row.get('expansion_category')}. "
        f"Founder attention {row.get('founder_attention_score')} means {row.get('founder_attention_category')}."
    )


def build_account_score_explanations(scored_accounts: pd.DataFrame) -> pd.DataFrame:
    """Build account-level score explanations for founder trust."""
    explanations = scored_accounts.copy()
    explanations["health_score_drivers"] = explanations.apply(health_score_drivers, axis=1)
    explanations["retention_risk_drivers"] = explanations.apply(retention_risk_drivers, axis=1)
    explanations["expansion_score_drivers"] = explanations.apply(expansion_score_drivers, axis=1)
    explanations["founder_attention_drivers"] = explanations.apply(
        founder_attention_drivers, axis=1
    )
    explanations["score_interpretation"] = explanations.apply(score_interpretation, axis=1)
    explanations = explanations.sort_values(
        by=["founder_attention_score", "retention_risk_score", "contract_value"],
        ascending=[False, False, False],
    )
    return explanations[
        [
            "account_id",
            "customer_name",
            "health_score_drivers",
            "retention_risk_drivers",
            "expansion_score_drivers",
            "founder_attention_drivers",
            "recommended_next_action",
            "score_interpretation",
        ]
    ]


def build_founder_memo(
    scored_accounts: pd.DataFrame,
    scorecard: pd.DataFrame,
    renewal_queue: pd.DataFrame,
    expansion_queue: pd.DataFrame,
    founder_queue: pd.DataFrame,
    churn_drivers: pd.DataFrame,
    proof_opportunities: pd.DataFrame,
    company_config: dict[str, Any],
) -> str:
    """Build the founder retention memo."""
    total_accounts = len(scored_accounts)
    unhealthy = int(scored_accounts["health_category"].isin(["At risk", "Critical"]).sum())
    renewal_risk = int(
        scored_accounts["retention_risk_category"].isin(["At risk", "Critical"]).sum()
    )
    expansion_ready = int(
        scored_accounts["expansion_category"].isin(["Expansion-ready", "Expansion candidate"]).sum()
    )
    founder_now = int(
        (scored_accounts["founder_attention_category"] == "Founder intervention now").sum()
    )
    product_gaps = scored_accounts[
        scored_accounts["product_gap"].str.lower().isin(
            [
                "critical missing feature",
                "compliance blocker",
                "repeated product gap",
                "integration gap",
                "data export gap",
            ]
        )
    ]

    lines = [
        "# Founder Retention Memo",
        "",
        "## Data note",
        "",
        company_config.get(
            "data_context_note",
            "Sample data is synthetic and fictionalized. Confirm your own data source before making customer decisions.",
        ),
        "",
        "## Executive summary",
        "",
        f"{company_config['company_name']} has {total_accounts} activated customer accounts in this review. "
        f"{unhealthy} are at risk or critical, {renewal_risk} have at-risk or critical retention risk, "
        f"{expansion_ready} are expansion-ready or candidates, and {founder_now} need founder intervention now.",
        "",
        "Read the founder attention queue first, then review renewal risk, expansion opportunities, and churn drivers.",
        "",
        "Scores are deterministic. They use `config/scoring_rules.yml`, visible account fields, and rule-based queue logic. Review `outputs/account_score_explanations.csv` when you want the reason behind a score.",
        "",
        "## Customer health snapshot",
        "",
        markdown_table(
            scorecard,
            [
                "customer_name",
                "customer_health_score",
                "health_category",
                "retention_risk_score",
                "expansion_category",
                "founder_attention_category",
            ],
            limit=12,
        ),
        "## Accounts needing founder attention this week",
        "",
        markdown_table(
            founder_queue,
            ["priority_rank", "customer_name", "risk_or_opportunity", "reason", "founder_action"],
            limit=10,
        ),
        "## Renewal risks",
        "",
        markdown_table(
            renewal_queue,
            ["priority_rank", "customer_name", "renewal_date", "risk_reason", "founder_action"],
            limit=10,
        ),
        "## Expansion opportunities",
        "",
        markdown_table(
            expansion_queue,
            [
                "priority_rank",
                "customer_name",
                "expansion_signal",
                "expansion_readiness_score",
                "suggested_expansion_motion",
            ],
            limit=10,
        ),
        "## Churn drivers",
        "",
        markdown_table(
            churn_drivers,
            ["driver", "count", "estimated_revenue_at_risk", "suggested_fix", "owner_role"],
            limit=10,
        ),
        "## Customer proof opportunities",
        "",
        markdown_table(
            proof_opportunities,
            ["customer_name", "reference_potential", "case_study_potential", "proof_angle"],
            limit=10,
        ),
        "## Product gaps affecting retention",
        "",
        markdown_table(
            product_gaps,
            ["customer_name", "contract_value", "product_gap", "recommended_next_action"],
            limit=10,
        ),
        "## Recommended next 7-day actions",
        "",
        "1. Review every account in the founder attention queue and confirm owner, customer action, and due date.",
        "2. Build save plans for critical renewal risks before discussing lower-priority expansion.",
        "3. Turn expansion-ready accounts into named discovery or proposal motions.",
        "4. Convert the top churn drivers into product, success, finance, or executive actions.",
        "5. Update CRM or customer success tracker with current health, renewal risk, expansion signal, and next step.",
    ]
    return "\n".join(lines)


def build_operating_review(
    scored_accounts: pd.DataFrame,
    renewal_queue: pd.DataFrame,
    expansion_queue: pd.DataFrame,
    founder_queue: pd.DataFrame,
    churn_drivers: pd.DataFrame,
    company_config: dict[str, Any],
) -> str:
    """Build the weekly retention and expansion operating review."""
    lines = [
        "# Retention Expansion Operating Review",
        "",
        "## Data note",
        "",
        company_config.get(
            "data_context_note",
            "Sample data is synthetic and fictionalized. Confirm your own data source before making customer decisions.",
        ),
        "",
        "## Weekly retention and expansion review agenda",
        "",
        "1. Review customer health and renewal risk movement.",
        "2. Discuss founder attention queue.",
        "3. Inspect expansion-ready accounts and proof opportunities.",
        "4. Decide churn driver fixes and owner assignments.",
        "5. Confirm CRM or customer success tracker updates.",
        "",
        "## Metrics to inspect",
        "",
        f"- Accounts reviewed: {len(scored_accounts)}",
        f"- Healthy accounts: {int((scored_accounts['health_category'] == 'Healthy').sum())}",
        f"- At-risk or critical accounts: {int(scored_accounts['health_category'].isin(['At risk', 'Critical']).sum())}",
        f"- At-risk or critical retention risks: {int(scored_accounts['retention_risk_category'].isin(['At risk', 'Critical']).sum())}",
        f"- Expansion-ready or candidate accounts: {int(scored_accounts['expansion_category'].isin(['Expansion-ready', 'Expansion candidate']).sum())}",
        f"- Founder attention accounts: {len(founder_queue)}",
        "",
        "## Accounts to discuss",
        "",
        markdown_table(
            founder_queue,
            ["priority_rank", "customer_name", "risk_or_opportunity", "owner", "due_timing"],
            limit=12,
        ),
        "## Decisions needed",
        "",
        "- Which renewal risks need founder or executive touch this week?",
        "- Which expansion-ready accounts should move to discovery or proposal?",
        "- Which product gaps need a customer-facing response?",
        "- Which customers should become references, case studies, or champions?",
        "- Which churn drivers should be escalated into the weekly operating review?",
        "",
        "## Owners and due dates",
        "",
        markdown_table(
            founder_queue,
            ["customer_name", "owner", "founder_action", "due_timing"],
            limit=12,
        ),
        "## What to update in CRM or customer success tracker",
        "",
        "- Customer health category and health score",
        "- Renewal date, renewal risk, and save plan status",
        "- Expansion signal, expansion category, and next expansion step",
        "- Executive sponsor, account owner, and customer success owner",
        "- Latest business review and customer touchpoint dates",
        "- Product gaps, support ticket risk, payment status, and churn signal",
        "- Reference or case study readiness",
        "",
        "## What to escalate to founder or board narrative",
        "",
        markdown_table(
            founder_queue[founder_queue["due_timing"].isin(["Today", "This week"])],
            ["customer_name", "risk_or_opportunity", "reason", "founder_action"],
            limit=10,
        ),
        "## Renewal and expansion queues",
        "",
        markdown_table(
            renewal_queue,
            ["priority_rank", "customer_name", "days_to_renewal", "risk_reason", "owner"],
            limit=8,
        ),
        markdown_table(
            expansion_queue,
            ["priority_rank", "customer_name", "expansion_signal", "suggested_expansion_motion"],
            limit=8,
        ),
        "## Churn drivers to fix",
        "",
        markdown_table(
            churn_drivers,
            ["driver", "count", "suggested_fix", "owner_role"],
            limit=10,
        ),
    ]
    return "\n".join(lines)


def generate_outputs(
    input_csv: str | Path,
    company_config: dict[str, Any],
    scoring_config: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Path]:
    """Run the full reporting pipeline and write all outputs."""
    from .ingest import load_accounts

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    accounts = load_accounts(input_csv)
    scored_accounts = build_scored_accounts(accounts, company_config, scoring_config)
    scorecard = build_customer_health_scorecard(scored_accounts)
    renewal_queue = build_renewal_risk_queue(scored_accounts)
    expansion_queue = build_expansion_opportunity_queue(scored_accounts)
    founder_queue = build_founder_attention_queue(scored_accounts)
    churn_drivers = build_churn_driver_summary(scored_accounts)
    proof_opportunities = build_customer_proof_opportunities(scored_accounts)
    score_explanations = build_account_score_explanations(scored_accounts)

    files = {
        "scorecard": output_path / "customer_health_scorecard.csv",
        "renewal_queue": output_path / "renewal_risk_queue.csv",
        "expansion_queue": output_path / "expansion_opportunity_queue.csv",
        "founder_queue": output_path / "founder_attention_queue.csv",
        "churn_drivers": output_path / "churn_driver_summary.csv",
        "proof_opportunities": output_path / "customer_proof_opportunities.csv",
        "score_explanations": output_path / "account_score_explanations.csv",
        "founder_memo": output_path / "founder_retention_memo.md",
        "operating_review": output_path / "retention_expansion_operating_review.md",
    }

    scorecard.to_csv(files["scorecard"], index=False)
    renewal_queue.to_csv(files["renewal_queue"], index=False)
    expansion_queue.to_csv(files["expansion_queue"], index=False)
    founder_queue.to_csv(files["founder_queue"], index=False)
    churn_drivers.to_csv(files["churn_drivers"], index=False)
    proof_opportunities.to_csv(files["proof_opportunities"], index=False)
    score_explanations.to_csv(files["score_explanations"], index=False)
    files["founder_memo"].write_text(
        build_founder_memo(
            scored_accounts,
            scorecard,
            renewal_queue,
            expansion_queue,
            founder_queue,
            churn_drivers,
            proof_opportunities,
            company_config,
        ),
        encoding="utf-8",
    )
    files["operating_review"].write_text(
        build_operating_review(
            scored_accounts,
            renewal_queue,
            expansion_queue,
            founder_queue,
            churn_drivers,
            company_config,
        ),
        encoding="utf-8",
    )
    return files
