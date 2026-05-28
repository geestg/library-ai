FROM python:3.11-slim

# =========================================
# SYSTEM DEPENDENCIES
# =========================================

RUN apt-get update && apt-get install -y \

    build-essential \
    gcc \
    curl \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \

    && rm -rf /var/lib/apt/lists/*

# =========================================
# WORKDIR
# =========================================

WORKDIR /app

# =========================================
# COPY REQUIREMENTS
# =========================================

COPY requirements.txt .

# =========================================
# INSTALL PYTHON PACKAGES
# =========================================

RUN pip install --no-cache-dir -r requirements.txt

# =========================================
# COPY PROJECT
# =========================================

COPY . .

# =========================================
# EXPOSE
# =========================================

EXPOSE 8000

# =========================================
# START SERVER
# =========================================

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]