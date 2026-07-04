# egysentinel/tests/test_alert_agent.py

import pytest
import json
import sys
sys.path.append(".")

from egysentinel.agents.alert_agent import generate_alert
from egysentinel.agents.fallbacks import get_alert_fallback
import jsonschema
from pathlib import Path

# Load schema for validation
SCHEMA_PATH = Path("egysentinel/schemas/alert.json")
with open(SCHEMA_PATH) as f:
    ALERT_SCHEMA = json.load(f)


def validate_alert(alert: dict):
    """Helper to validate alert schema"""
    jsonschema.validate(alert, ALERT_SCHEMA)
    return True


# Test 1: Low priority account
def test_low_priority_alert():
    result = generate_alert(
        account_id="C_LOW_001",
        risk_score=15.0,
        pattern_type="layering",
        total_amount=500.0
    )
    assert validate_alert(result)
    assert result["priority"] == "low"
    assert result["recommended_action"] == "monitor"
    print("✅ Test 1 (low priority) passed")


# Test 2: Medium priority account  
def test_medium_priority_alert():
    result = generate_alert(
        account_id="C_MED_002",
        risk_score=50.0,
        pattern_type="fan_in",
        total_amount=15000.0
    )
    assert validate_alert(result)
    assert result["priority"] == "medium"
    print("✅ Test 2 (medium priority) passed")


# Test 3: High priority account
def test_high_priority_alert():
    result = generate_alert(
        account_id="C_HIGH_003",
        risk_score=70.0,
        pattern_type="fan_out",
        total_amount=40000.0
    )
    assert validate_alert(result)
    assert result["priority"] == "high"
    print("✅ Test 3 (high priority) passed")


# Test 4: Critical priority account
def test_critical_priority_alert():
    result = generate_alert(
        account_id="C_CRIT_004",
        risk_score=90.0,
        pattern_type="circular_flow",
        total_amount=80000.0
    )
    assert validate_alert(result)
    assert result["priority"] == "critical"
    assert result["recommended_action"] == "freeze"
    print("✅ Test 4 (critical priority) passed")


# Test 5: Fallback test
def test_fallback_alert():
    # Test fallback directly
    result = get_alert_fallback(
        account_id="C_FALL_005",
        risk_score=85.0,
        pattern_type="circular_flow"
    )
    assert validate_alert(result)
    assert result["priority"] == "critical"
    assert "[RULE-BASED]" in result["summary"]
    print("✅ Test 5 (fallback) passed")


if __name__ == "__main__":
    print("Running Alert Agent Unit Tests\n")
    print("=" * 40)
    
    tests = [
        test_low_priority_alert,
        test_medium_priority_alert,
        test_high_priority_alert,
        test_critical_priority_alert,
        test_fallback_alert
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{len(tests)} passed")