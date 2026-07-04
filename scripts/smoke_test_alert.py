# scripts/smoke_test_alert.py

import sys
import json
sys.path.append(".")

from egysentinel.agents.alert_agent import (
    generate_alert,
    generate_alert_from_risk_output
)

def run_smoke_test():
    print("🔥 Alert Agent Smoke Test\n")
    print("=" * 40)
    
    # Test 1: Known fraud account
    print("\nTest 1: Known fraud account")
    result = generate_alert(
        account_id="C999999",
        risk_score=88.0,
        pattern_type="circular_flow",
        total_amount=75000.0
    )
    
    assert result is not None, "❌ Result is None"
    assert "priority" in result, "❌ Missing priority"
    assert "summary" in result, "❌ Missing summary"
    assert "recommended_action" in result, \
        "❌ Missing recommended_action"
    assert result["priority"] in [
        "low", "medium", "high", "critical"
    ], f"❌ Invalid priority: {result['priority']}"
    
    print(f"✅ Test 1 passed: priority={result['priority']}")
    print(f"   Summary: {result['summary']}")
    
    # Test 2: Full pipeline with DS-3 format
    print("\nTest 2: DS-3 risk scorer format")
    risk_output = {
        "account_id": "C888888",
        "rule_score": 75.0,
        "ml_prob": 0.82,
        "final_score": 78.5,
        "risk_band": "high",
        "pattern_type": "fan_out",
        "total_amount": 32000.0
    }
    
    result2 = generate_alert_from_risk_output(risk_output)
    assert result2 is not None, "❌ Result2 is None"
    assert result2["priority"] in ["high", "critical"], \
        f"❌ Expected high/critical, got {result2['priority']}"
    
    print(f"✅ Test 2 passed: priority={result2['priority']}")
    
    # Test 3: Fallback test
    print("\nTest 3: Fallback (simulated GLM failure)")
    from egysentinel.agents.fallbacks import get_alert_fallback
    fallback = get_alert_fallback("C777777", 85.0, 
                                   "circular_flow")
    assert fallback["priority"] == "critical", \
        f"❌ Fallback priority wrong: {fallback['priority']}"
    print(f"✅ Test 3 passed: fallback fired correctly")
    
    print("\n" + "=" * 40)
    print("✅ All smoke tests passed!")
    return True


if __name__ == "__main__":
    success = run_smoke_test()
    sys.exit(0 if success else 1)