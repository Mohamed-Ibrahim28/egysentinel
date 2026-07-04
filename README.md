# EGY-Sentinel AML 🛡️

> AI-powered Anti-Money Laundering surveillance system  
> Graph + ML + Agentic AI — 10-day capstone sprint

---

## 📋 Project Overview

EGY-Sentinel detects money-laundering patterns in mobile-money
transactions using a 3-layer pipeline:

1. **Graph Analysis** — NetworkX + Neo4j detect suspicious patterns
2. **ML Risk Scoring** — XGBoost ranks every account low/medium/high
3. **AI Agents** — 3 GLM-powered agents investigate high-risk accounts

Dataset: PaySim synthetic dataset (6.3M transactions, 50K sample)

---

## 👥 Team Structure

| ID | Role | Responsibility |
|----|------|----------------|
| DS-1 | Data Engineer | PaySim pipeline, sampling, EDA, schemas |
| DS-2 | Graph Engineer | NetworkX graph, 5 detectors, Neo4j |
| DS-3 | ML Engineer | Rule scorer, XGBoost, risk combination |
| AI-1 | LLM Infrastructure | GLM client, caching, fallbacks |
| **AI-2** | **Alert Agent** | **Priority classification, alert generation** |
| AI-3 | Case Builder Agent | SAR investigation report |
| AI-4 | Explanation Agent | Plain-English justification |
| AI-5 | Orchestrator + Backend | FastAPI, Streamlit, Docker |

---

## 📁 Repository Structure
egysentinel/
├── agents/
│   ├── init.py
│   ├── alert_agent.py          ✅ AI-2 (Done)
│   ├── llm_client.py           ⚠️  STUB — AI-1 replaces this
│   ├── fallbacks.py            ✅ AI-2 (Done)
│   ├── case_builder_agent.py   ❌ AI-3 (Pending)
│   ├── explanation_agent.py    ❌ AI-4 (Pending)
│   ├── orchestrator.py         ❌ AI-1 (Pending)
│   ├── evidence.py             ❌ AI-3 (Pending)
│   └── prompts/
│       ├── alert.txt           ✅ AI-2 (Done)
│       ├── case_builder.txt    ❌ AI-3 (Pending)
│       └── explanation.txt     ❌ AI-4 (Pending)
├── schemas/
│   ├── alert.json              ✅ AI-2 (Done)
│   ├── account.json            ❌ DS-1 (Pending)
│   ├── transaction.json        ❌ DS-1 (Pending)
│   ├── case_report.json        ❌ AI-3 (Pending)
│   └── features.json           ❌ DS-3 (Pending)
├── score/
│   ├── rule_scorer.py          ❌ DS-3 (Pending)
│   ├── ml_scorer.py            ❌ DS-3 (Pending)
│   └── combine.py              ❌ DS-3 (Pending)
├── graph/
│   ├── build.py                ❌ DS-2 (Pending)
│   └── inspect.py              ❌ DS-2 (Pending)
├── detect/
│   ├── circular.py             ❌ DS-2 (Pending)
│   ├── fan_out.py              ❌ DS-2 (Pending)
│   ├── fan_in.py               ❌ DS-2 (Pending)
│   ├── layering.py             ❌ DS-2 (Pending)
│   └── dense_cluster.py        ❌ DS-2 (Pending)
├── api/
│   ├── main.py                 ❌ AI-5 (Pending)
│   └── models.py               ❌ AI-5 (Pending)
├── data/
│   └── llm_cache/              ❌ AI-1 (Pending)
├── docs/
│   └── alert_contract.md       ✅ AI-2 (Done)
├── scripts/
│   └── smoke_test_alert.py     ✅ AI-2 (Done)
└── tests/
├── test_alert_agent.py     ✅ AI-2 (Done)
└── test_prompt_v2.py       ✅ AI-2 (Done)

---

## ✅ What's Done (AI-2 — Alert Agent)

### `agents/alert_agent.py`
- `generate_alert(account_id, risk_score, pattern_type, total_amount)` 
- `generate_alert_from_risk_output(risk_output)` — consumes DS-3 format
- Full error handling — JSON errors, schema errors, GLM timeouts
- Auto-fallback to rule-based template on any failure

### `agents/prompts/alert.txt`
- System prompt v2 with 4 few-shot examples
- Covers all 4 priorities: low / medium / high / critical
- Priority logic documented inside prompt

### `agents/fallbacks.py`
- `get_alert_fallback(account_id, risk_score, pattern_type)`
- Pure rule-based — no GLM needed
- Returns schema-valid alert always

### `schemas/alert.json`
- JSON Schema draft-07
- Required fields: `priority`, `summary`, `recommended_action`
- Enum validation on all fields

### `agents/llm_client.py` ⚠️
- **THIS IS A STUB** — rule-based simulation only
- **AI-1 must replace this file** with real GLM client
- Interface is fixed: `LLMClient().complete(system_prompt, user_prompt)`

---

## ⚠️ What Needs To Be Done By Other Members

### AI-1 — LLM Infrastructure
**Must replace:** `egysentinel/agents/llm_client.py`

Your file must have this exact interface:
```python
class LLMClient:
    def __init__(self):
        # setup caching, retry logic
        pass
    
    def complete(self, system_prompt: str, 
                 user_prompt: str) -> str:
        # returns raw string response from GLM
        pass
```

---

### DS-3 — ML Engineer
**Must produce:** risk scorer output in this exact format:
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
Alert agent consumes this via `generate_alert_from_risk_output()`

---

### AI-3 — Case Builder Agent
**Must consume:** alert output in this format:
```json
{
  "priority": "low | medium | high | critical",
  "summary": "string",
  "recommended_action": "investigate | monitor | escalate | freeze"
}
```
Full contract in `docs/alert_contract.md`

---

### AI-5 — Orchestrator + Backend
**Must expose:** FastAPI endpoint that calls alert agent:
POST /investigate
→ calls alert_agent.generate_alert()
→ returns alert JSON

---

## 🔄 Pipeline Flow
PaySim CSV
↓
DS-1: 50K Sample + Schemas
↓
DS-2: Graph + 5 Pattern Detectors
↓
DS-3: Risk Scorer (rule + XGBoost)
↓
AI-2: Alert Agent ← YOU ARE HERE
↓
AI-3: Case Builder Agent
↓
AI-4: Explanation Agent
↓
AI-5: FastAPI + Streamlit + Docker

---

## 📊 Alert Agent — Priority Logic

| Priority | Condition |
|----------|-----------|
| critical | score ≥ 80 OR pattern = circular_flow |
| high | score ≥ 60 OR pattern = fan_out/fan_in |
| medium | score ≥ 40 OR pattern = layering |
| low | score < 40 |

| Priority | Recommended Action |
|----------|--------------------|
| critical | freeze |
| high | escalate |
| medium | investigate |
| low | monitor |

---

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/Mohamed-Ibrahim28/egysentinel.git
cd egysentinel

# Install dependencies
pip install jsonschema

# Run alert agent
python egysentinel/agents/alert_agent.py

# Run smoke test
python egysentinel/scripts/smoke_test_alert.py

# Run unit tests
python egysentinel/tests/test_alert_agent.py
```

---

## 📈 KPIs — Alert Agent

| Metric | Target | Status |
|--------|--------|--------|
| Schema validity | 100% | ✅ |
| Alert latency p95 | ≤ 5s | ✅ |
| Fallback coverage | 100% | ✅ |
| Priority accuracy | ≥ 4/5 | ✅ |

---

## 🔑 Key Rules

- **Scope freeze Day 8 at 13:00** — no prompt changes after
- **Every GLM call has a fallback** — demo never blocks
- **Schema must be valid always** — jsonschema validates every output
- **Escalate blockers within 1 hour** — don't go dark

---

## 📞 Handoff Map

| From | To | What | When |
|------|----|------|------|
| DS-1 | AI-1 | JSON schemas locked | Day 1 17:00 |
| DS-3 | AI-2 | Risk scorer output | Day 4 EOD |
| AI-1 | AI-2 | Real llm_client.py | Day 2 EOD |
| AI-2 | AI-3 | Alert JSON | Day 5 EOD |

---

*EGY-Sentinel AML — Capstone Project · 10-Day Sprint · v1.0*