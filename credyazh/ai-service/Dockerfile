# ─── CredYazh AI Service — Dockerfile ───────────────────────────────────────
# Python 3.12 FastAPI service (Port 8000)
# Serves: /draft/audio  /draft/text  /health  /whatsapp-message

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system deps (needed for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (layer caching — only re-run when requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start uvicorn (single worker; add --workers N for production scale)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

