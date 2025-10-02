import json
from collections import defaultdict
import re
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else "sample.jsonl"

ENTITY_ID_PATTERN = re.compile(r"^[A-Z0-9_]+$")

stories = defaultdict(lambda: {"indices": [], "expected_count": None})
invalid_entity_ids = []

# process data
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        record = json.loads(line)
        doc_id = record.get("RP_DOCUMENT_ID")
        entity_id = record.get("RP_ENTITY_ID")
        record_index = record.get("DOCUMENT_RECORD_INDEX")
        record_count = record.get("DOCUMENT_RECORD_COUNT")

        # analytics
        stories[doc_id]["indices"].append(record_index)
        stories[doc_id]["expected_count"] = record_count

        # validate RP_ENTITY_ID
        if not ENTITY_ID_PATTERN.match(str(entity_id)):
            invalid_entity_ids.append(entity_id)


print(f"📊 Total distinct stories: {len(stories)}\n")

# missing analytics
missing_analytics = {}
for doc_id, data in stories.items():
    indices_set = set(data["indices"])
    expected_count = data["expected_count"]

    if expected_count is not None:
        missing = [i for i in range(expected_count) if i not in indices_set]
        if missing:
            missing_analytics[doc_id] = missing

print("🔍 Stories with missing analytics:")
if missing_analytics:
    print(f" Total with issues: {len(missing_analytics)}")
    for doc, missing in missing_analytics.items():
        print(f" - {doc}: missing {missing}")
else:
    print(" None")

# Invalid RP_ENTITY_IDs
print("\nInvalid RP_ENTITY_ID values:")
if invalid_entity_ids:
    print(f" Total invalid: {len(invalid_entity_ids)}")
    for invalid_id in invalid_entity_ids:
        print(f" - {invalid_id}")
else:
    print(" None")
