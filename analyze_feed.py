import json
import sys
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


def process_file(filename):
    tracker = StoryTracker()

    with open(filename, "r") as f:
        for line in f:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            tracker.add_record(record)

    total_stories = len(tracker.stories)
    missing_analytics = tracker.report_missing()

    return total_stories, missing_analytics


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_feed.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    total, missing = process_file(file_path)

    print(f"Total distinct stories: {total}")
    print("\nStories with missing analytics:")
    if missing:
        for doc, miss in missing.items():
            print(f" - {doc}: missing {miss}")
    else:
        print(" None")