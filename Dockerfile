# Copy requirements and install packages
COPY requirements.txt .
# --no-cache-dir ensures we don't store temp files that cause permission/metadata issues
# --upgrade ensures we get the latest stable pip before installing your list
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
