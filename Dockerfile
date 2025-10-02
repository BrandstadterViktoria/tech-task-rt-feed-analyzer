# Use Python 3.12 slim image
FROM python:3.12-slim

WORKDIR /app

# add data
COPY analyze_feed.py .
COPY sample.jsonl .

CMD ["python", "analyze_feed.py", "sample.jsonl"]
