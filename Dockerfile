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

# Start your FastAPI/Uvicorn server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
