# egysentinel/agents/alert_agent.py

import json
import jsonschema
from pathlib import Path
from .llm_client import LLMClient
from .fallbacks import get_alert_fallback


# أضف في أول الـ file

import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Timeout للـ GLM calls
GLM_TIMEOUT_SECONDS = 5.0


def generate_alert(account_id: str,
                   risk_score: float,
                   pattern_type: str,
                   total_amount: float = 0.0) -> dict:
    
    start_time = time.time()
    
    user_prompt = f"""
Analyze this high-risk account and generate an alert:

{{
  "account_id": "{account_id}",
  "final_score": {risk_score},
  "pattern_type": "{pattern_type}",
  "total_amount": {total_amount}
}}
"""
    
    try:
        response = client.complete(
            system_prompt=ALERT_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        
        # Check latency
        elapsed = time.time() - start_time
        if elapsed > GLM_TIMEOUT_SECONDS:
            logger.warning(
                f"GLM slow response: {elapsed:.2f}s "
                f"for {account_id}"
            )
        
        # Clean response (remove markdown if any)
        response = response.strip()
        if response.startswith("```"):
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        
        alert = json.loads(response)
        jsonschema.validate(alert, ALERT_SCHEMA)
        
        logger.info(
            f"Alert generated: {account_id} → "
            f"{alert['priority']} ({elapsed:.2f}s)"
        )
        return alert
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error for {account_id}: {e}")
        return get_alert_fallback(
            account_id, risk_score, pattern_type
        )
        
    except jsonschema.ValidationError as e:
        logger.error(f"Schema error for {account_id}: {e.message}")
        return get_alert_fallback(
            account_id, risk_score, pattern_type
        )
        
    except TimeoutError:
        logger.error(f"GLM timeout for {account_id}")
        return get_alert_fallback(
            account_id, risk_score, pattern_type
        )
        
    except Exception as e:
        logger.error(f"Unexpected error for {account_id}: {e}")
        return get_alert_fallback(
            account_id, risk_score, pattern_type
        )





# Load schema
SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "alert.json"
with open(SCHEMA_PATH) as f:
    ALERT_SCHEMA = json.load(f)

# Load prompt
PROMPT_PATH = Path(__file__).parent / "prompts" / "alert.txt"
with open(PROMPT_PATH) as f:
    ALERT_SYSTEM_PROMPT = f.read()

# Initialize LLM client
client = LLMClient()


if __name__ == "__main__":
    # Test with 5 accounts
    test_cases = [
        {
            "account_id": "C100001",
            "risk_score": 15.0,
            "pattern_type": "layering",
            "total_amount": 500.0
        },
        {
            "account_id": "C100002",
            "risk_score": 55.0,
            "pattern_type": "fan_in",
            "total_amount": 20000.0
        },
        {
            "account_id": "C100003",
            "risk_score": 72.0,
            "pattern_type": "fan_out",
            "total_amount": 45000.0
        },
        {
            "account_id": "C100004",
            "risk_score": 88.0,
            "pattern_type": "circular_flow",
            "total_amount": 90000.0
        },
        {
            "account_id": "C100005",
            "risk_score": 35.0,
            "pattern_type": "dense_cluster",
            "total_amount": 8000.0
        }
    ]
    
    results = []
    for case in test_cases:
        print(f"\n--- Testing {case['account_id']} ---")
        result = generate_alert(**case)
        results.append(result)
        print(json.dumps(result, indent=2))
    
    # Check results
    passed = sum(1 for r in results 
                 if r.get("priority") != "high")
    print(f"\n📊 {passed}/5 non-placeholder results")


    # أضف الـ function دي في alert_agent.py

def generate_alert_from_risk_output(risk_output: dict) -> dict:
    """
    Generate alert from DS-3's risk scorer output.
    
    Args:
        risk_output: {
            "account_id": str,
            "rule_score": float,
            "ml_prob": float,
            "final_score": float,
            "risk_band": str
        }
    
    Returns:
        dict: Schema-valid alert
    """
    
    # Extract fields from DS-3 output
    account_id = risk_output["account_id"]
    final_score = risk_output["final_score"]
    risk_band = risk_output.get("risk_band", "medium")
    
    # Get pattern type if available
    pattern_type = risk_output.get(
        "pattern_type", "unknown"
    )
    
    # Get total amount if available
    total_amount = risk_output.get("total_amount", 0.0)
    
    # Only process high-risk accounts
    if risk_band not in ["high"] and final_score < 60:
        print(f"⏭️ Skipping {account_id} — "
              f"risk_band={risk_band}, "
              f"score={final_score}")
        return None
    
    return generate_alert(
        account_id=account_id,
        risk_score=final_score,
        pattern_type=pattern_type,
        total_amount=total_amount
    )


if __name__ == "__main__":
    # Simulate DS-3 output
    simulated_risk_outputs = [
        {
            "account_id": "C100003",
            "rule_score": 65.0,
            "ml_prob": 0.78,
            "final_score": 71.5,
            "risk_band": "high",
            "pattern_type": "fan_out",
            "total_amount": 45000.0
        },
        {
            "account_id": "C100004",
            "rule_score": 90.0,
            "ml_prob": 0.95,
            "final_score": 92.5,
            "risk_band": "high",
            "pattern_type": "circular_flow",
            "total_amount": 90000.0
        }
    ]
    
    print("Testing with DS-3 risk output format:\n")
    for risk_output in simulated_risk_outputs:
        print(f"--- {risk_output['account_id']} ---")
        result = generate_alert_from_risk_output(risk_output)
        if result:
            print(json.dumps(result, indent=2))
        print()