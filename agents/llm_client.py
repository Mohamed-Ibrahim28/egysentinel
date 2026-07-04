# egysentinel/agents/llm_client.py
# TEMPORARY STUB — هيتبدل بالـ real client من AI-1

class LLMClient:
    def __init__(self):
        print("⚠️ Using STUB LLM Client")
    
    def complete(self, system_prompt: str, 
                 user_prompt: str) -> str:
        """
        Stub returns rule-based response.
        Will be replaced by AI-1's real GLM client.
        """
        # Extract score from prompt
        score = 50.0
        pattern = "unknown"
        account = "UNKNOWN"
        
        for line in user_prompt.split("\n"):
            if "final_score" in line:
                try:
                    score = float(
                        line.split(":")[1].strip().rstrip(",")
                    )
                except:
                    pass
            if "pattern_type" in line:
                try:
                    pattern = line.split(":")[1].strip()\
                                  .strip('",')
                except:
                    pass
            if "account_id" in line:
                try:
                    account = line.split(":")[1].strip()\
                                  .strip('",')
                except:
                    pass
        
# Rule-based priority (matches unit tests)
        if score >= 85:
            priority = "critical"
            action = "freeze"
        
        elif score >= 65:
            priority = "high"
            action = "escalate"
        
        elif score >= 40:
            priority = "medium"
            action = "investigate"
        
        else:
            priority = "low"
            action = "monitor"
        import json
        return json.dumps({
            "priority": priority,
            "summary": f"Account {account} flagged with "
                      f"score {score:.0f} and "
                      f"{pattern} pattern.",
            "recommended_action": action
        })