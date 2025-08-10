
###################################################################################################
# AIAhura Tech — DevOps Technical Assessment
# Project: AI Inference Service
# This repository is part of AIAhura Tech's DevOps engineer interview process.
# All work submitted will be evaluated for technical quality, security practices, and documentation.
###################################################################################################


# TODO: Create a multi-stage Dockerfile
# - Builder stage to cache deps
# - Final slim image, non-root user
# - Expose 8000 and run uvicorn
# Hints provided, but intentionally incomplete.

FROM python:3.11-slim AS builder
WORKDIR /app
COPY app/requirements.txt .
# TODO: build wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*
# RUN pip install --upgrade pip && pip wheel -r requirements.txt -w /wheels
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

FROM python:3.11-slim
# TODO: add non-root user
RUN useradd --create-home appuser
WORKDIR /app
# TODO: copy wheels and install without cache
# COPY --from=builder /wheels /wheelis
COPY --from=builder /wheels /wheels
# RUN pip install --no-cache-dir /wheels/*
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY app/ ./
ENV PYTHONUNBUFFERED=1 \
 PORT=8000 \
 LOG_LEVEL=INFO
USER appuser
EXPOSE 8000
# TODO: set a secure, explicit CMD to run uvicorn app:app
# CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
