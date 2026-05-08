# Churn Driver Analysis Prompt

Use this prompt manually with the generated outputs. No API integration is required.

```text
You are helping a founder identify recurring churn drivers.

Use the churn driver summary, customer health scorecard, and account score explanations.

Focus on:
- Which churn drivers affect the most revenue
- Which churn drivers affect the most accounts
- Which churn drivers are product issues
- Which churn drivers are customer success issues
- Which churn drivers are payment or RevOps issues

Return:
1. Top churn drivers by revenue at risk
2. Top churn drivers by count
3. Suggested fix for each driver
4. Owner role for each fix
5. What the founder should inspect next week

Do not invent customer details. Use only the provided rows.
```
