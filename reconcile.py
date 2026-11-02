import json
from datetime import datetime

latest = {}

with open("payments.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if not isinstance(event, dict):
            continue

        txn_id = event.get("txn_id")

        if not txn_id:
            continue

        timestamp = datetime.fromisoformat(
            event["ts"].replace("Z", "+00:00")
        )

        previous = latest.get(txn_id)

        if previous is None or timestamp >= previous["_timestamp"]:
            event["_timestamp"] = timestamp
            latest[txn_id] = event

successful = [
    event for event in latest.values()
    if event["status"] == "success"
]

count = len(successful)

total = sum(float(str(event["amount"]).replace(",", "")) for event in successful)

with open("expected.txt", "r") as file:
    expected = int(file.read().strip())

if count != expected:
    print(f"Check failed: counted {count}, expected {expected}.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
