# Founder Use Case

## Scenario

A seed-stage B2B SaaS founder has 25 activated customers. The team knows which customers reached activation, but customer health is scattered across usage notes, support tickets, NPS, renewal dates, payment status, and founder memory.

The founder wants to know:

- Which customers are drifting toward churn?
- Which renewals need action this week?
- Which customers are ready for expansion?
- Which accounts need founder or executive touch?
- Which customers can become references or case studies?

## Workflow

1. Export the customer health tracker from CRM, CS tracker, support system, or spreadsheet.
2. Replace `data/sample_customer_accounts.csv`.
3. Edit `config/company_profile.yml`.
4. Run `make run`.
5. Open `outputs/founder_retention_memo.md`.
6. Review `outputs/founder_attention_queue.csv`.
7. Use `outputs/account_score_explanations.csv` to understand why accounts were scored.

## What the founder learns

The founder can quickly separate:

- urgent renewal risk
- customer health watches
- expansion-ready customers
- proof-ready champions
- churn drivers that need process or product action

The output is not a dashboard. It is a weekly operating review packet with owners and next actions.
