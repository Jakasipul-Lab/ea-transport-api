# 1. Use a slim version of Python as the base
FROM python:3.11-slim

# 2. Set the working directory inside the NAS container
WORKDIR /app

# 3. Copy your requirements file first
COPY requirements.txt .

# 4. Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your code
COPY . .

# 6. The command to start your server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
