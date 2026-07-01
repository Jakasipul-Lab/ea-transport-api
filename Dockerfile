# 1. Use a slim version of Python
FROM python:3.11-slim

# 2. Create a non-root user for security
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home appuser

# 3. Set the working directory
WORKDIR /app

# 4. Copy requirements and install packages
# Using --no-cache-dir keeps the image small
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# 5. Copy the rest of your code and set ownership
COPY . .
RUN chown -R appuser:appgroup /app

# 6. Switch to the non-root user
USER appuser

# 7. Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
