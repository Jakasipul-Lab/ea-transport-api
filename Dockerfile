# Use Python 3.11 (stable for your 8GB plan)
FROM python:3.11-slim

# THIS LINE FIXES THE ERROR: It installs the missing libpq5 driver
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install your requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your original server.py and files
COPY . .

# Ensure the port is set for Railway
ENV PORT=8080
EXPOSE 8080

# 1. The base (Python)
FROM python:3.9-slim

# 2. Your setup (Copying files, installing requirements)
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# 3. The Railway Port Setup
EXPOSE 8080

# 4. PASTE THE NEW LINE HERE (The very end)
CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8080}
