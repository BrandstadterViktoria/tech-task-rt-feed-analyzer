# tech-task-rt-feed-analyzer
Python application to analyze real-time feed records, verify data integrity, and validate entity IDs. Includes Docker support for easy setup.

## Problem Statement

This project analyzes a JSON Lines (.jsonl) file containing real-time feed data. Each record belongs to a story (RP_DOCUMENT_ID) and has:

- **DOCUMENT_RECORD_INDEX** — the position of this record within the story  
- **DOCUMENT_RECORD_COUNT** — total expected analytics records for the story  
- **RP_ENTITY_ID** — an entity ID that must follow a valid format  

The goals of this project are to:

1. Count the total number of distinct stories in the feed.  
2. Detect stories that are missing analytics records.  
3. Validate that RP_ENTITY_ID values conform to the expected format.  

## How the Script Works

### Count Distinct Stories
Reads all records and counts unique `RP_DOCUMENT_ID` values.  

### Detect Missing Analytics
Checks if each story has all expected `DOCUMENT_RECORD_INDEX` values.  
✅ The expected number of records is determined directly from **`DOCUMENT_RECORD_COUNT`**, ensuring accurate detection even if the highest index is missing from the data.  

Reports which indices are missing per story.  

### Validate RP_ENTITY_ID Values
Uses a regex pattern (`^[A-Z0-9_]+$`) to validate IDs.  
Reports any invalid IDs.  

## How to Run
Make sure you have Python 3.12 installed.

Place your feed file in the project directory (e.g., `sample.jsonl`).  

Run the script:
```
python analyze_feed.py sample.jsonl
```

If no file is provided, the script defaults to sample.jsonl.

## Run with Docker

Build the Docker image:
```
docker build -t feed-analyzer .
```

Run the container with the default feed file:
```
docker run --rm feed-analyzer
```

To specify a different input file, mount your local folder and provide the filename:
```
docker run --rm -v C:/Users/vikto/Code/tech-task-rt-feed-analyzer:/app feed-analyzer python analyze_feed.py sample.jsonl
```

-v <host_path>:<container_path> mounts your local folder inside the container so you can access your JSONL files without copying them into the image.