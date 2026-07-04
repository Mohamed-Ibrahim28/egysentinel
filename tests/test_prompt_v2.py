# egysentinel/tests/test_prompt_v2.py

# 5 test cases هنختبر بيهم الـ prompt
# دي بيانات اصطناعية عشان نشوف منطق الـ priority صح

test_accounts = [
    {
        "account_id": "C100001",
        "final_score": 15,
        "pattern_type": "layering",
        "total_amount": 500,
        "expected_priority": "low"
    },
    {
        "account_id": "C100002", 
        "final_score": 55,
        "pattern_type": "fan_in",
        "total_amount": 20000,
        "expected_priority": "medium"
    },
    {
        "account_id": "C100003",
        "final_score": 72,
        "pattern_type": "fan_out", 
        "total_amount": 45000,
        "expected_priority": "high"
    },
    {
        "account_id": "C100004",
        "final_score": 88,
        "pattern_type": "circular_flow",
        "total_amount": 90000,
        "expected_priority": "critical"
    },
    {
        "account_id": "C100005",
        "final_score": 35,
        "pattern_type": "dense_cluster",
        "total_amount": 8000,
        "expected_priority": "low"
    }
]

def check_results(results):
    """Check if priority matches expected"""
    passed = 0
    for i, (result, test) in enumerate(
        zip(results, test_accounts)
    ):
        expected = test["expected_priority"]
        actual = result.get("priority", "unknown")
        
        if actual == expected:
            print(f"✅ Test {i+1} PASSED — "
                  f"{test['account_id']}: {actual}")
            passed += 1
        else:
            print(f"❌ Test {i+1} FAILED — "
                  f"{test['account_id']}: "
                  f"expected {expected}, got {actual}")
    
    print(f"\n📊 Results: {passed}/5 passed")
    return passed >= 4  # نجاح لو 4 من 5 صح


if __name__ == "__main__":
    print("Test accounts loaded:")
    for t in test_accounts:
        print(f"  {t['account_id']}: "
              f"score={t['final_score']}, "
              f"pattern={t['pattern_type']}, "
              f"expected={t['expected_priority']}")