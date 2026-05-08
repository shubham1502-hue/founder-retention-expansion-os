# How to Fork and Use

This guide is written for non-technical founders and operators.

## Step 1: Fork the repo

Click Fork on GitHub. Rename the repo if you want a company-specific internal version.

## Step 2: Replace the sample data

Open `data/sample_customer_accounts.csv`.

Replace it with your own customer health tracker. Keep the same column names. If your internal tracker uses different names, rename the columns before running the workflow.

The sample data is synthetic and fictionalized. Do not put private customer data in a public fork.

## Step 3: Edit company config

Open `config/company_profile.yml`.

Edit:

- company name
- renewal cycle
- high-value threshold
- health thresholds
- owner roles
- escalation rules
- review cadence

## Step 4: Edit scoring rules if needed

Open `config/scoring_rules.yml`.

Change weights if your business model treats some signals as more important than others. For example, a product-led company may increase usage and active user ratio. An enterprise company may increase business review recency and executive sponsor signals.

## Step 5: Run the workflow

```bash
make install
make run
```

Or run the demo:

```bash
make demo
```

## Step 6: Interpret outputs

Open these files in order:

1. `outputs/founder_retention_memo.md`
2. `outputs/founder_attention_queue.csv`
3. `outputs/renewal_risk_queue.csv`
4. `outputs/expansion_opportunity_queue.csv`
5. `outputs/account_score_explanations.csv`

## Step 7: Put outputs into your operating rhythm

Use the memo in a weekly customer health review. Assign owners and due dates in your CRM, customer success tracker, Notion, Airtable, Linear, ClickUp, or spreadsheet.
