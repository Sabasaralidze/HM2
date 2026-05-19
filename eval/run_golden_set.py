import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import run_agent


def evaluate_answer(answer, expected_keywords):
    answer_lower = answer.lower()
    matched = [word for word in expected_keywords if word.lower() in answer_lower]
    return len(matched) >= 1


def main():
    with open("eval/golden_set.json", "r") as f:
        tests = json.load(f)

    results = []
    passed = 0

    for item in tests:
        answer = run_agent("eval_user", item["question"])
        is_pass = evaluate_answer(answer, item["expected_keywords"])

        if is_pass:
            passed += 1

        results.append({
            "question": item["question"],
            "answer": answer,
            "expected_keywords": item["expected_keywords"],
            "passed": is_pass
        })

    final_result = {
        "timestamp": datetime.utcnow().isoformat(),
        "total": len(tests),
        "passed": passed,
        "failed": len(tests) - passed,
        "results": results
    }

    with open("eval/results/results.json", "w") as f:
        json.dump(final_result, f, indent=2)

    print(f"Golden evaluation completed: {passed}/{len(tests)} passed")


if __name__ == "__main__":
    main()