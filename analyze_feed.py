import json
import sys


def process_file(filename):
    # logic will be added in the next commit
    return 0, {}


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
