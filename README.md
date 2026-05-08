# Founder Retention Expansion OS

Turn activated customers into retained, expanding, referenceable customers with renewal risk, expansion readiness, founder attention queues, and weekly operating reviews.

This helps founders prevent activated customers from drifting toward churn, shows which accounts need founder or executive touch, identifies expansion-ready customers, and turns scattered post-activation signals into owner-backed actions.

## Founder quick read

| If you need to know... | Open this |
| --- | --- |
| What should I review first | `outputs/founder_retention_memo.md` |
| Which activated customers are unhealthy | `outputs/customer_health_scorecard.csv` |
| Which customers need founder or executive touch this week | `outputs/founder_attention_queue.csv` |
| Which renewals are at risk | `outputs/renewal_risk_queue.csv` |
| Which customers are ready for expansion | `outputs/expansion_opportunity_queue.csv` |
| Which churn drivers need owner action | `outputs/churn_driver_summary.csv` |
| Which customers could become proof, references, or case studies | `outputs/customer_proof_opportunities.csv` |
| Why an account received a score or recommendation | `outputs/account_score_explanations.csv` |

Fastest path:

1. Replace `data/sample_customer_accounts.csv`.
2. Edit `config/company_profile.yml`.
3. Run `make run`.
4. Open `outputs/founder_retention_memo.md`.

## The founder problem

Founders often track sales and onboarding, but lose visibility after activation. Retention risk hides inside declining usage, weak adoption, unpaid invoices, product gaps, stakeholder changes, support tickets, renewal proximity, and silent customers.

This repo turns post-activation customer chaos into a founder-ready retention and expansion control tower.

## What this repo does

- Scores customer health
- Flags renewal risk
- Identifies expansion-ready accounts
- Creates founder attention queue
- Summarizes churn drivers
- Finds customer proof opportunities
- Explains account scores
- Generates a weekly retention memo
- Creates a retention and expansion operating review

## What a founder gets in 10 minutes

- Customer health scorecard
- Renewal risk queue
- Expansion opportunity queue
- Founder attention queue
- Churn driver summary
- Customer proof opportunities
- Score explanations
- Founder retention memo

## Before and after

Before:

- Activated customers drift quietly
- Renewal risk appears too late
- Expansion signals stay buried in notes
- Customer proof opportunities are missed
- Founder only hears about churn when it is urgent

After:

- Customer health scorecard
- Renewal risk queue
- Expansion opportunity queue
- Churn driver summary
- Customer proof list
- Founder-ready retention memo
- Clear next actions and owners

## Who this is for

- Early-stage founders
- Founder's Office teams
- BizOps operators
- RevOps operators
- Customer Success operators
- B2B SaaS teams
- AI startup founders
- Founder-led services businesses
- Retention-driven startups

## Quick start

1. Fork repo
2. Clone repo
3. Install dependencies
4. Edit company config
5. Replace sample customer CSV
6. Run the system
7. Review outputs

```bash
make install
make run
```

| Step | File or command | What to do |
| --- | --- | --- |
| 1 | `data/sample_customer_accounts.csv` | Replace with your customer health tracker |
| 2 | `config/company_profile.yml` | Edit renewal cycle, health thresholds, segments, risk rules |
| 3 | `make run` | Generate scorecards, queues, memo, and review |
| 4 | `outputs/founder_retention_memo.md` | Read this first |
| 5 | `outputs/account_score_explanations.csv` | Check why scores and recommendations were assigned |

## How to fork and use this for your company

- Click Fork
- Rename repo if needed
- Replace `data/sample_customer_accounts.csv`
- Edit `config/company_profile.yml`
- Edit `config/scoring_rules.yml` if needed
- Run `make run`
- Review `outputs/founder_retention_memo.md` first
- Review `outputs/renewal_risk_queue.csv` second
- Review `outputs/expansion_opportunity_queue.csv` third
- Connect outputs to Google Sheets, Notion, Airtable, HubSpot, Salesforce, Attio, Pipedrive, Intercom, Zendesk, Linear, or your CS tracker if relevant

Non-technical path:

- Replace one CSV
- Edit one YAML file
- Run one command
- Read one memo

## Standalone or integrated

Standalone:
Use this repo by itself if you only need retention, renewal, expansion, and customer health visibility after activation. Fork it, replace the sample input, run the workflow, and use the main outputs in your next founder review.

Integrated:
Use this repo with the Founder OS ecosystem if you want to connect customer health to onboarding, weekly review, board narrative, revenue diagnosis, or AI workflow prioritization.

- Use after `founder-customer-onboarding-os` when customers reach activation.
- Feed renewal risk, expansion signals, churn drivers, and founder attention accounts into `founder-weekly-operating-review-agent`.
- Feed material retention or expansion risk into `board-pack-investor-update-agent` when investor narrative matters.
- Use `founder-ai-workflow-roi-os` when retention workflows become repetitive or ops-heavy.

## Lifecycle handoff

Before:

- `founder-customer-onboarding-os` for onboarding and activation
- `founder-os-revenue-engine` for revenue leakage diagnosis
- `founder-weekly-operating-review-agent` for weekly operating cadence

This repo produces:

- Customer health scorecard
- Renewal risk queue
- Expansion opportunity queue
- Founder attention queue
- Churn driver summary
- Customer proof opportunities
- Founder retention memo

After:

- `founder-weekly-operating-review-agent` for weekly review
- `board-pack-investor-update-agent` for investor or board narrative
- `founder-ai-workflow-roi-os` if retention workflows should be automated, hired for, outsourced, or left manual

## Where this fits in the Founder OS

- Use [ai-gtm-command-center](https://github.com/shubham1502-hue/ai-gtm-command-center) before calls to research accounts and prepare outreach.
- Use [founder-led-sales-call-os](https://github.com/shubham1502-hue/founder-led-sales-call-os) after sales calls to extract objections, risks, and deal rescue actions.
- Use [founder-os-revenue-engine](https://github.com/shubham1502-hue/founder-os-revenue-engine) to diagnose revenue leakage.
- Use [founder-customer-onboarding-os](https://github.com/shubham1502-hue/founder-customer-onboarding-os) after close-won to track activation.
- Use [founder-retention-expansion-os](https://github.com/shubham1502-hue/founder-retention-expansion-os) after activation to protect renewals and find expansion.
- Use [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent) to roll risks and opportunities into weekly review.
- Use [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent) for investor narrative.
- Use [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) to decide what retention workflows to automate.
- Use [revops-infrastructure-playbook](https://github.com/shubham1502-hue/revops-infrastructure-playbook) to design CRM, reporting, handoff, and automation backbone.
- Use [startup-metrics-playbook](https://github.com/shubham1502-hue/startup-metrics-playbook) to define metrics before building dashboards.
- Use [founder-os](https://github.com/shubham1502-hue/founder-os) as the umbrella operating system.

## Input format

Replace `data/sample_customer_accounts.csv` with your customer health tracker. The sample file is synthetic and fictionalized.

Required columns:

| Column | What it means |
| --- | --- |
| `account_id` | Unique account identifier |
| `customer_name` | Customer account name |
| `segment` | Customer segment such as Startup, Mid-market, Enterprise, or Strategic |
| `industry` | Customer industry |
| `contract_value` | Current annual contract value or retained revenue value |
| `plan_type` | Current plan or package |
| `activation_date` | Date the customer reached activation or initial value |
| `renewal_date` | Next renewal date |
| `account_owner` | Commercial owner for renewal and expansion |
| `customer_success_owner` | Owner for health, adoption, and value proof |
| `executive_sponsor` | Internal or founder sponsor for high-value or at-risk accounts |
| `key_stakeholder_role` | Main customer stakeholder role |
| `health_status` | Current team-entered health label |
| `usage_trend` | Usage direction such as growing, stable, flat, low, declining, or inactive |
| `product_adoption_score` | Adoption score from 0 to 100 |
| `active_users` | Active users in the review period |
| `licensed_users` | Licensed users or purchased seats |
| `support_tickets_open` | Open support ticket count |
| `critical_tickets_open` | Open critical support ticket count |
| `nps_score` | NPS-style score from -100 to 100 |
| `last_business_review_date` | Last QBR, EBR, or value review date |
| `last_customer_touchpoint_date` | Last meaningful customer interaction date |
| `stakeholder_change` | Stakeholder continuity signal |
| `payment_status` | Current, paid, invoice pending, delayed, overdue, unpaid, or payment failed |
| `product_gap` | Most important product gap affecting retention |
| `expansion_signal` | Expansion signal such as more seats requested or usage growth |
| `renewal_risk_signal` | Renewal signal such as no risk, watch, unclear value proof, budget concern, or churn risk |
| `churn_risk_signal` | Churn signal such as none, usage concern, competitive evaluation, churn risk, or cancellation threat |
| `reference_potential` | Potential for reference use |
| `case_study_potential` | Potential for case study use |
| `next_step` | Next owner-backed action |
| `notes` | Short account context |

## Output files

Open `outputs/founder_retention_memo.md` first.

| Output | What it tells a founder to do next |
| --- | --- |
| `outputs/customer_health_scorecard.csv` | Review account health, risk category, expansion category, founder attention category, and recommended next action |
| `outputs/renewal_risk_queue.csv` | Prioritize renewal saves by risk, owner, founder action, due timing, and expected leverage |
| `outputs/expansion_opportunity_queue.csv` | Decide which expansion motions should move to discovery, proposal, value proof, or delay |
| `outputs/founder_attention_queue.csv` | Decide which accounts need founder intervention, executive review, or owner follow-up this week |
| `outputs/churn_driver_summary.csv` | Pick recurring churn drivers to fix, with affected accounts, revenue at risk, suggested fix, and owner role |
| `outputs/customer_proof_opportunities.csv` | Choose reference, champion, and case study asks with owner and next step |
| `outputs/account_score_explanations.csv` | Audit why each health, retention, expansion, and founder attention recommendation was assigned |
| `outputs/founder_retention_memo.md` | Read the weekly founder memo and commit the next 7-day actions |
| `outputs/retention_expansion_operating_review.md` | Run the weekly retention and expansion review with decisions, owners, and escalation topics |

## How to trust the scores

The base workflow uses deterministic scoring. It does not call an LLM, paid API, or hidden model.

- Inputs come from the CSV.
- Company assumptions come from `config/company_profile.yml`.
- Weights come from `config/scoring_rules.yml`.
- Scores are bounded from 0 to 100.
- `account_score_explanations.csv` explains the main drivers for every account.
- You can edit the weights and thresholds without changing code.

Use the scores as a founder review system, not as an automatic customer decision engine.

| Score | Direction | Founder interpretation |
| --- | --- | --- |
| Customer health score | Higher is better | 80 to 100 is Healthy, 60 to 79 is Watch, 40 to 59 is At risk, below 40 is Critical |
| Retention risk score | Higher means more risk | 80 to 100 is Critical, 60 to 79 is At risk, 35 to 59 is Watch, below 35 is Low risk |
| Expansion readiness score | Higher is better | 80 to 100 is Expansion-ready, 60 to 79 is Expansion candidate, 35 to 59 is Not yet, below 35 is Do not expand |
| Founder attention score | Higher means more leadership action | 85 to 100 is Founder intervention now, 65 to 84 is Executive review this week, 40 to 64 is Owner follow-up |

The clearest audit trail is `outputs/account_score_explanations.csv`. It lists health score drivers, retention risk drivers, expansion score drivers, founder attention drivers, recommended next action, and score interpretation for every account.

## Example founder workflow

- Monday: Review founder retention memo
- Tuesday: Inspect renewal risk queue
- Wednesday: Review expansion opportunity queue
- Thursday: Assign founder or executive touch actions
- Friday: Update weekly operating review and board narrative if needed

## Customization guide

Customize these before using the repo for a real company:

- Renewal cycle in `config/company_profile.yml`
- Health thresholds in `config/company_profile.yml`
- Risk thresholds in `config/scoring_rules.yml`
- Owner roles in `config/company_profile.yml`
- Expansion rules in `config/company_profile.yml`
- Founder attention rules through thresholds and weights
- Score weights in `config/scoring_rules.yml`
- Output format in `src/founder_retention_expansion/reporting.py`

## Why this matters

This is not a customer success dashboard. It is a founder operating system for making sure activated customers become retained, expanding, and referenceable customers.

## Roadmap

- Google Sheets export
- Notion export
- Streamlit dashboard
- HubSpot integration
- Salesforce integration
- Attio integration
- Intercom/Zendesk support import
- Slack escalation alerts
- Customer health trend tracking
- Renewal forecasting
- Expansion forecasting
- Case study and reference workflow

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License. See [LICENSE](LICENSE).

## Built by

Built by Shubham Singh, a founder-facing operator focused on RevOps, GTM systems, startup metrics, AI workflows, and operating systems for early-stage teams.
