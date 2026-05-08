# Founder Retention Memo

## Data note

Sample data is synthetic and fictionalized for demo use. Replace it with your own internal customer health tracker before making customer decisions.

## Executive summary

Acme Retention Systems has 25 activated customer accounts in this review. 8 are at risk or critical, 9 have at-risk or critical retention risk, 13 are expansion-ready or candidates, and 3 need founder intervention now.

Read the founder attention queue first, then review renewal risk, expansion opportunities, and churn drivers.

Scores are deterministic. They use `config/scoring_rules.yml`, visible account fields, and rule-based queue logic. Review `outputs/account_score_explanations.csv` when you want the reason behind a score.

## Customer health snapshot

| customer_name | customer_health_score | health_category | retention_risk_score | expansion_category | founder_attention_category |
| --- | --- | --- | --- | --- | --- |
| Stonebridge Procurement | 26 | Critical | 95 | Do not expand | Founder intervention now |
| Halcyon Robotics | 19 | Critical | 95 | Do not expand | Founder intervention now |
| Atlas Freight Works | 38 | Critical | 85 | Do not expand | Founder intervention now |
| Silverline Insurance | 37 | Critical | 85 | Do not expand | Executive review this week |
| Beacon Clinic Group | 51 | At risk | 78 | Do not expand | Executive review this week |
| Orchid Payments | 56 | At risk | 78 | Do not expand | Executive review this week |
| Northstar Analytics | 85 | Healthy | 20 | Expansion-ready | Owner follow-up |
| Terrace Construction Tech | 46 | At risk | 85 | Do not expand | Owner follow-up |
| Marigold Marketplace | 60 | Watch | 78 | Do not expand | Owner follow-up |
| Pioneer Data Co | 87 | Healthy | 14 | Expansion-ready | Owner follow-up |
| Quartz Retail Systems | 57 | At risk | 60 | Not yet | Owner follow-up |
| Granite Wealth Partners | 72 | Watch | 40 | Expansion candidate | Owner follow-up |

## Accounts needing founder attention this week

| priority_rank | customer_name | risk_or_opportunity | reason | founder_action |
| --- | --- | --- | --- | --- |
| 1 | Stonebridge Procurement | Retention risk | High-value account; Critical retention risk; Critical customer health; cancellation threat; churn risk | Founder or executive sponsor call to reset value and renewal path. |
| 2 | Halcyon Robotics | Retention risk | High-value account; Critical retention risk; Critical customer health; Renewal in 28 days; cancellation threat | Founder or executive sponsor call to reset value and renewal path. |
| 3 | Atlas Freight Works | Retention risk | High-value account; Critical retention risk; Critical customer health; Renewal in 63 days; churn risk | Founder or executive sponsor call to reset value and renewal path. |
| 4 | Silverline Insurance | Retention risk | High-value account; Critical retention risk; Critical customer health; Renewal in 12 days; competitive evaluation | Founder or executive sponsor call to reset value and renewal path. |
| 5 | Beacon Clinic Group | Retention risk | High-value account; At risk retention risk; At risk customer health; Renewal in 20 days; usage concern | Review customer health and assign the highest leverage owner action. |
| 6 | Orchid Payments | Retention risk | High-value account; At risk retention risk; At risk customer health; Renewal in 17 days; budget concern | Review customer health and assign the highest leverage owner action. |
| 7 | Northstar Analytics | Expansion opportunity | High-value account; Renewal in 38 days; expansion potential; Expansion-ready | Review expansion motion and approve customer-facing ask. |
| 8 | Terrace Construction Tech | Retention risk | Critical retention risk; At risk customer health; Renewal in 58 days; usage concern; renewal risk | Founder or executive sponsor call to reset value and renewal path. |
| 9 | Marigold Marketplace | Retention risk | At risk retention risk; Renewal in 41 days; usage concern; unclear value proof; new evaluator | Review customer health and assign the highest leverage owner action. |
| 10 | Pioneer Data Co | Expansion opportunity | High-value account; expansion potential; Expansion-ready | Review expansion motion and approve customer-facing ask. |

## Renewal risks

| priority_rank | customer_name | renewal_date | risk_reason | founder_action |
| --- | --- | --- | --- | --- |
| 1 | Halcyon Robotics | 2026-06-05 | High-value account; Critical retention risk; Critical customer health; Renewal in 28 days; cancellation threat | Founder or executive sponsor call to reset value and renewal path. |
| 2 | Stonebridge Procurement | 2026-09-30 | High-value account; Critical retention risk; Critical customer health; cancellation threat; churn risk | Founder or executive sponsor call to reset value and renewal path. |
| 3 | Silverline Insurance | 2026-05-20 | High-value account; Critical retention risk; Critical customer health; Renewal in 12 days; competitive evaluation | Founder or executive sponsor call to reset value and renewal path. |
| 4 | Terrace Construction Tech | 2026-07-05 | Critical retention risk; At risk customer health; Renewal in 58 days; usage concern; renewal risk | Founder or executive sponsor call to reset value and renewal path. |
| 5 | Atlas Freight Works | 2026-07-10 | High-value account; Critical retention risk; Critical customer health; Renewal in 63 days; churn risk | Founder or executive sponsor call to reset value and renewal path. |
| 6 | Orchid Payments | 2026-05-25 | High-value account; At risk retention risk; At risk customer health; Renewal in 17 days; budget concern | Review customer health and assign the highest leverage owner action. |
| 7 | Beacon Clinic Group | 2026-05-28 | High-value account; At risk retention risk; At risk customer health; Renewal in 20 days; usage concern | Review customer health and assign the highest leverage owner action. |
| 8 | Marigold Marketplace | 2026-06-18 | At risk retention risk; Renewal in 41 days; usage concern; unclear value proof; new evaluator | Review customer health and assign the highest leverage owner action. |
| 9 | Quartz Retail Systems | 2026-06-25 | At risk retention risk; At risk customer health; Renewal in 48 days; usage concern; unclear value proof | Review customer health and assign the highest leverage owner action. |
| 10 | Granite Wealth Partners | 2026-06-30 | High-value account; Renewal in 53 days; watch; watch; reporting gap | Review customer health and assign the highest leverage owner action. |

## Expansion opportunities

| priority_rank | customer_name | expansion_signal | expansion_readiness_score | suggested_expansion_motion |
| --- | --- | --- | --- | --- |
| 1 | Pioneer Data Co | upsell requested | 89 | Package upgrade proposal with success proof. |
| 2 | Redwood BioWorks | upsell requested | 89 | Package upgrade proposal with success proof. |
| 3 | Helio AI Studio | product-led expansion signal | 88 | Seat expansion discovery with account owner and CS. |
| 4 | Northstar Analytics | more seats requested | 87 | Seat expansion discovery with account owner and CS. |
| 5 | Summit Legal Ops | product-led expansion signal | 87 | Seat expansion discovery with account owner and CS. |
| 6 | Maple Support Cloud | more seats requested | 87 | Seat expansion discovery with account owner and CS. |
| 7 | Willow Health Tech | usage growth | 83 | Map new team use case and quantify incremental value. |
| 8 | BluePeak Manufacturing | usage growth | 82 | Map new team use case and quantify incremental value. |
| 9 | Clearwater Finance | mild interest | 81 | Confirm value proof before starting expansion motion. |
| 10 | Granite Wealth Partners | mild interest | 74 | Confirm value proof before starting expansion motion. |

## Churn drivers

| driver | count | estimated_revenue_at_risk | suggested_fix | owner_role |
| --- | --- | --- | --- | --- |
| Product gap | 12 | $1,292,000 | Create a product gap response with scope, owner, and customer message. | Product Lead |
| Critical support tickets | 9 | $1,106,000 | Escalate critical tickets with owner and customer-facing timeline. | Support Lead |
| Stakeholder change | 8 | $956,000 | Rebuild stakeholder map and confirm executive sponsor. | Account Owner |
| Churn risk signal | 9 | $915,000 | Open save plan with commercial and product owner. | Customer Success |
| Stale touchpoint | 9 | $846,000 | Set customer touchpoint SLA and review stale accounts weekly. | Customer Success |
| Low active user ratio | 9 | $826,000 | Map inactive licensed users and run enablement push. | Customer Success |
| Support ticket load | 7 | $810,000 | Prioritize support closure by renewal and customer value. | Support Lead |
| Declining usage | 8 | $794,000 | Run adoption recovery plan with customer success owner. | Customer Success |
| Renewal value proof unclear | 8 | $794,000 | Run renewal value proof review and document outcomes. | Customer Success |
| Low product adoption | 7 | $723,000 | Identify unused value drivers and rebuild success plan. | Customer Success |

## Customer proof opportunities

| customer_name | reference_potential | case_study_potential | proof_angle |
| --- | --- | --- | --- |
| Pioneer Data Co | high | high | Case study on retained value in Data services. |
| Redwood BioWorks | high | high | Case study on retained value in Biotech. |
| Helio AI Studio | high | high | Case study on retained value in AI software. |
| Northstar Analytics | high | high | Case study on retained value in Data tooling. |
| Maple Support Cloud | high | medium | Reference for Startup customers. |
| Summit Legal Ops | high | medium | Reference for Mid-market customers. |
| Willow Health Tech | high | medium | Reference for Mid-market customers. |
| BluePeak Manufacturing | medium | medium | Expansion story with usage growth proof. |
| Clearwater Finance | medium | medium | Customer proof after next value review. |
| Granite Wealth Partners | medium | low | Customer proof after next value review. |

## Product gaps affecting retention

| customer_name | contract_value | product_gap | recommended_next_action |
| --- | --- | --- | --- |
| Atlas Freight Works | $152,000 | repeated product gap | Founder should contact the executive sponsor and reset the retention plan. |
| Halcyon Robotics | $96,000 | critical missing feature | Founder should contact the executive sponsor and reset the retention plan. |
| Evergreen Energy Labs | $175,000 | integration gap | Run a success plan review around the main churn signal. |
| Silverline Insurance | $142,000 | compliance blocker | Create a save plan with owner, customer sponsor, risk driver, and due date. |
| Cedar Security | $134,000 | data export gap | Run a success plan review around the main churn signal. |
| Stonebridge Procurement | $99,000 | repeated product gap | Founder should contact the executive sponsor and reset the retention plan. |

## Recommended next 7-day actions

1. Review every account in the founder attention queue and confirm owner, customer action, and due date.
2. Build save plans for critical renewal risks before discussing lower-priority expansion.
3. Turn expansion-ready accounts into named discovery or proposal motions.
4. Convert the top churn drivers into product, success, finance, or executive actions.
5. Update CRM or customer success tracker with current health, renewal risk, expansion signal, and next step.