# Retention Risk Review Prompt

Use this prompt manually with the generated outputs. No API integration is required.

```text
You are helping a seed-stage founder review customer retention risk.

Use the attached or pasted customer health scorecard, renewal risk queue, founder attention queue, churn driver summary, and account score explanations.

Focus on:
- Which activated customers are becoming unhealthy
- Which renewals need action this week
- Which churn drivers are most repeated
- Which accounts need founder or executive touch
- Which owners need to act in the next 7 days

Return:
1. Top 5 retention risks
2. One-sentence reason for each risk
3. Recommended founder action
4. Owner and due date recommendation
5. One process improvement to reduce future renewal risk

Do not invent data. If a field is missing, say what is missing.
```
