# tech-task-rt-feed-analyzer
Python application to analyze real-time feed records, verify data integrity, and validate entity IDs. Includes Docker support for easy setup.


## Problem Statement

This project analyzes a JSON Lines (.jsonl) file containing real-time feed data. Each record belongs to a story (RP_DOCUMENT_ID) and has:

DOCUMENT_RECORD_INDEX — the position of this record within the story

DOCUMENT_RECORD_COUNT — total expected analytics records for the story

RP_ENTITY_ID — an entity ID that must follow a valid format

The goals of this project are to:

Count the total number of distinct stories in the feed.

Detect stories that are missing analytics records.

Validate that RP_ENTITY_ID values conform to the expected format.

## How the Script Works
The script performs the following:

Count Distinct Stories

Reads all records and counts unique RP_DOCUMENT_ID values.

Detect Missing Analytics

Checks if each story has all expected DOCUMENT_RECORD_INDEX values based on DOCUMENT_RECORD_COUNT.

Reports which indices are missing per story.

Validate RP_ENTITY_ID Values

Uses a regex pattern (alphanumeric + underscores) to validate IDs.

Reports any invalid IDs.

## How to run 
Make sure you have Python 3.12 installed.

Place your feed file in the project directory (e.g., sample.jsonl).

Run the script:
```
python analyze_feed.py sample.jsonl
```

If no file is provided, the script defaults to sample.jsonl.