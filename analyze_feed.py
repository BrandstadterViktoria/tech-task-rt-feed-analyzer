import json
import sys
import re
import os
from collections import defaultdict


class StoryTracker:
    def __init__(self):
        self.stories = defaultdict(lambda: {"expected": None, "seen": set()})

    def add_record(self, record):
        doc_id = record.get("RP_DOCUMENT_ID")
        idx = record.get("DOCUMENT_RECORD_INDEX")
        total = record.get("DOCUMENT_RECORD_COUNT")

        if doc_id is None or idx is None or total is None:
            return

        if self.stories[doc_id]["expected"] is None:
            self.stories[doc_id]["expected"] = total

        self.stories[doc_id]["seen"].add(idx)

    def report_missing(self):
        missing = {}
        for doc_id, info in self.stories.items():
            expected = set(range(info["expected"]))
            seen = info["seen"]
            if seen != expected:
                missing[doc_id] = sorted(expected - seen)
        return missing


class EntityValidator:
    def __init__(self, pattern=r"^[A-Z0-9_-]+$"):
        self.pattern = re.compile(pattern)

    def is_valid(self, entity_id):
        return bool(self.pattern.match(entity_id))


def process_file(filename):
    tracker = StoryTracker()
    validator = EntityValidator()
    invalid_entities = []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue  # skip malformed lines

                tracker.add_record(record)

                entity_id = record.get("RP_ENTITY_ID")
                if entity_id and not validator.is_valid(entity_id):
                    invalid_entities.append(entity_id)
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        sys.exit(1)
    except OSError as e:
        print(f"❌ Error opening file '{filename}': {e}")
        sys.exit(1)

    total_stories = len(tracker.stories)
    missing_analytics = tracker.report_missing()

    return total_stories, missing_analytics, invalid_entities


def print_report(total, missing, invalids):
    print(f"\n📊 Total distinct stories: {total}")

    print("\n🔍 Stories with missing analytics:")
    if missing:
        print(f" Total with issues: {len(missing)}")
        for doc, miss in list(missing.items())[:5]:
            print(f" - {doc}: missing {miss}")
        if len(missing) > 5:
            print(f" ... and {len(missing) - 5} more")
    else:
        print(" None")

    print("\nInvalid RP_ENTITY_ID values:")
    if invalids:
        print(f" Total invalid: {len(invalids)}")
        for val in invalids[:5]:
            print(f" - {val}")
        if len(invalids) > 5:
            print(f" ... and {len(invalids) - 5} more")
    else:
        print(" None")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        file_path = "rt-feed-record"
        print(f"No input file provided, using default: {file_path}")
    else:
        file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    total, missing, invalids = process_file(file_path)
    print_report(total, missing, invalids)
