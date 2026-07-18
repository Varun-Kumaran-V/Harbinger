# -----------------------------------------------------------------------------
# Harbinger Research Repository
#
# Docker Image
# -----------------------------------------------------------------------------

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "backend/harbinger_pipeline.py"]