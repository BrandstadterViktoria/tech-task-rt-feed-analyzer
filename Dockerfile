# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only the script (don't include feed files here if you prefer mounting)
COPY analyze_feed.py .

# Default command
CMD ["python", "analyze_feed.py"]
