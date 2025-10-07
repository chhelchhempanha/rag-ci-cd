# ---------- Base image ----------
FROM python:3.13-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PATH="/root/.local/bin:$PATH"

# ---------- Working directory ----------
WORKDIR /app

# ---------- Install dependencies ----------
# Install system packages required by some Python libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Copy app source ----------
COPY . .

# ---------- Expose FastAPI port ----------
EXPOSE 8000

# ---------- Health check (optional) ----------
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# ---------- Start FastAPI ----------
# Using uvicorn as the ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
