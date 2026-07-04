# في egysentinel/agents/fallbacks.py
# القسم الخاص بالـ alert

def get_alert_fallback(account_id: str,
                       risk_score: float,
                       pattern_type: str) -> dict:
    """
    Rule-based fallback when GLM fails.
    No LLM needed — pure logic.
    """
    
    # Determine priority by rules
    if risk_score >= 80 or pattern_type == "circular_flow":
        priority = "critical"
        action = "freeze"
    elif risk_score >= 60 or pattern_type in [
        "fan_out", "fan_in"
    ]:
        priority = "high"
        action = "escalate"
    elif risk_score >= 40 or pattern_type == "layering":
        priority = "medium"
        action = "investigate"
    else:
        priority = "low"
        action = "monitor"
    
    return {
        "priority": priority,
        "summary": (
            f"[RULE-BASED] Account {account_id} flagged "
            f"with risk score {risk_score:.0f} and "
            f"{pattern_type} pattern."
        ),
        "recommended_action": action
    }