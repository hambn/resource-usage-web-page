# Python 3.9 slim as the base image
FROM python:3.9-slim

# working directory
WORKDIR /app

# dependencies required for psutil
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port 5000 
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]