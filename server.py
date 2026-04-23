FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files
COPY . .

# Setting the command and the port as the final instructions
EXPOSE 8000
ENV PORT=8000
CMD ["python", "server.py"]
