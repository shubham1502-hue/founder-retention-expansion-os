from pathlib import Path

import pandas as pd
import pytest

from founder_retention_expansion.config import load_company_config, load_scoring_config
from founder_retention_expansion.ingest import REQUIRED_COLUMNS, load_accounts, validate_required_columns


def test_load_accounts_sample_csv():
    df = load_accounts("data/sample_customer_accounts.csv")

    assert len(df) >= 25
    assert set(REQUIRED_COLUMNS).issubset(df.columns)
    assert pd.api.types.is_datetime64_any_dtype(df["renewal_date"])
    assert df["contract_value"].dtype == float


def test_required_column_validation():
    df = pd.DataFrame({"account_id": ["A001"]})

    with pytest.raises(ValueError, match="Input CSV missing required columns"):
        validate_required_columns(df)


def test_config_loading():
    company_config = load_company_config("config/company_profile.yml")
    scoring_config = load_scoring_config("config/scoring_rules.yml")

    assert company_config["company_name"] == "Acme Retention Systems"
    assert "usage_trend" in scoring_config["weights"]
