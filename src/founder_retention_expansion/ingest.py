"""CSV ingestion and input validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "account_id",
    "customer_name",
    "segment",
    "industry",
    "contract_value",
    "plan_type",
    "activation_date",
    "renewal_date",
    "account_owner",
    "customer_success_owner",
    "executive_sponsor",
    "key_stakeholder_role",
    "health_status",
    "usage_trend",
    "product_adoption_score",
    "active_users",
    "licensed_users",
    "support_tickets_open",
    "critical_tickets_open",
    "nps_score",
    "last_business_review_date",
    "last_customer_touchpoint_date",
    "stakeholder_change",
    "payment_status",
    "product_gap",
    "expansion_signal",
    "renewal_risk_signal",
    "churn_risk_signal",
    "reference_potential",
    "case_study_potential",
    "next_step",
    "notes",
]


DATE_COLUMNS = [
    "activation_date",
    "renewal_date",
    "last_business_review_date",
    "last_customer_touchpoint_date",
]


NUMERIC_COLUMNS = [
    "contract_value",
    "product_adoption_score",
    "active_users",
    "licensed_users",
    "support_tickets_open",
    "critical_tickets_open",
    "nps_score",
]


def validate_required_columns(df: pd.DataFrame) -> None:
    """Raise a useful error when required columns are missing."""
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError("Input CSV missing required columns: " + ", ".join(missing))


def load_accounts(path: str | Path) -> pd.DataFrame:
    """Load customer accounts from CSV and normalize common types."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    df = pd.read_csv(csv_path, keep_default_na=False)
    validate_required_columns(df)

    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    df["contract_value"] = df["contract_value"].astype(float)
    df["product_adoption_score"] = df["product_adoption_score"].astype(float)
    df["active_users"] = df["active_users"].astype(int)
    df["licensed_users"] = df["licensed_users"].astype(int)
    df["support_tickets_open"] = df["support_tickets_open"].astype(int)
    df["critical_tickets_open"] = df["critical_tickets_open"].astype(int)
    df["nps_score"] = df["nps_score"].astype(float)
    return df
