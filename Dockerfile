# Use a slim version of Python
FROM python:3.11-slim

# Create a non-root user for security (Prevents permission errors)
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home appuser

# Set working directory
WORKDIR /app

# Copy requirements and install packages
# --no-cache-dir keeps your image small and fast
# --root-user-action=ignore silences the pip warning
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy the rest of your code and set ownership
COPY . .
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Start the server using your specific file (server.py)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
