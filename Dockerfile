FROM python:3.12.7-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway will use this or set PORT env var)
EXPOSE 8000

# Run the application (Railway will override with startCommand from railway.json)
# This is a fallback - railway.json startCommand takes precedence
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

