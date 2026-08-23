FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OCR, PDF, and audio
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and datasets
COPY delbot_platform /app/delbot_platform
COPY datasets /app/datasets

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "delbot_platform.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
