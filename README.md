# tech-task-rt-feed-analyzer
Python application to analyze real-time feed records, verify data integrity, and validate entity IDs. Includes Docker support for easy setup.


## Problem Statement

This project analyzes a JSON lines file containing real-time feed data. Each record belongs to a story (RP_DOCUMENT_ID) and has an index (DOCUMENT_RECORD_INDEX) along with the total expected count (DOCUMENT_RECORD_COUNT).

The goal is to:

- Count how many distinct stories appear in the feed.

- Spot stories that are missing analytics records.

- Check that RP_ENTITY_ID values follow the correct format.

## How the Script Works

1.Count distinct stories
2.Find missing analytics
3.Validation