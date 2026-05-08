# Scoring Methodology

This repo uses deterministic scoring. It does not use an LLM, paid API, or hidden model for the base workflow.

## Inputs

Scores are calculated from:

- `data/sample_customer_accounts.csv`
- `config/company_profile.yml`
- `config/scoring_rules.yml`

## Customer health score

Customer health is a 0 to 100 score. Higher is better.

Main drivers:

- usage trend
- product adoption score
- active user ratio
- support ticket load
- critical ticket load
- NPS score
- last customer touchpoint
- last business review
- stakeholder change
- payment status
- product gap
- churn risk signal

Categories:

- Healthy: 80 to 100
- Watch: 60 to 79
- At risk: 40 to 59
- Critical: below 40

## Retention risk score

Retention risk is a 0 to 100 score. Higher means more risk.

Main drivers:

- declining usage
- weak adoption
- low active user ratio
- support tickets
- critical tickets
- low NPS
- stale touchpoint
- stale business review
- stakeholder change
- payment issue
- product gap
- renewal proximity
- churn risk signal

Categories:

- Low risk: below 35
- Watch: 35 to 59
- At risk: 60 to 79
- Critical: 80 to 100

## Expansion readiness score

Expansion readiness is a 0 to 100 score. Higher means stronger expansion readiness.

The score rewards healthy usage, adoption, NPS, low support load, clean payment status, and clear expansion signals. It is capped down when customer health is weak or retention risk is high.

Categories:

- Expansion-ready: 80 to 100
- Expansion candidate: 60 to 79
- Not yet: 35 to 59
- Do not expand: below 35 or blocked by health risk

## Founder attention score

Founder attention is a 0 to 100 score. Higher means more founder or executive review is needed.

The score combines retention risk, health risk, contract value, renewal proximity, churn risk, expansion leverage, and reference potential.

Categories:

- Founder intervention now: 85 to 100
- Executive review this week: 65 to 84
- Owner follow-up: 40 to 64
- Monitor: 20 to 39
- No action needed: below 20

## Score explanations

Open `outputs/account_score_explanations.csv` to see why each account received its recommendation. This file is designed to make the scoring easy to audit and edit.
