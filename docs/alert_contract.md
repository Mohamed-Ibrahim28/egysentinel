# Alert Agent — Input/Output Contract

## Input (from DS-3 Risk Scorer)
```json
{
  "account_id": "string",
  "rule_score": "float (0-100)",
  "ml_prob": "float (0-1)",
  "final_score": "float (0-100)",
  "risk_band": "low | medium | high",
  "pattern_type": "string",
  "total_amount": "float"
}
```

## Output (to AI-3 Case Builder)
```json
{
  "priority": "low | medium | high | critical",
  "summary": "string (max 200 chars)",
  "recommended_action": "investigate | monitor | escalate | freeze"
}
```

## Latency Target
- p95 < 5 seconds

## Fallback
- If GLM fails → rule-based template fires automatically