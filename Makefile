.PHONY: install run demo test clean

install:
	python3 -m pip install -e ".[dev]"

run:
	PYTHONPATH=src python3 -m founder_retention_expansion.cli run --input data/sample_customer_accounts.csv --company-config config/company_profile.yml --scoring-config config/scoring_rules.yml --output-dir outputs

demo:
	PYTHONPATH=src python3 -m founder_retention_expansion.cli demo

test:
	PYTHONPATH=src python3 -m pytest

clean:
	rm -f outputs/*.csv outputs/*.md
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
