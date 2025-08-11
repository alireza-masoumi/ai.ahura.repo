# AI Inference Service — DevOps Technical Assessment

## 1. Overview
This project implements a containerized **FastAPI** inference service with the following features:
- Prometheus metrics (Counter + Histogram) to monitor request counts and latencies.
- Redis-backed rate limiting to control request rates per client IP with a fail-open strategy for resiliency.
- Health check endpoint for service availability monitoring.
- Fully automated CI/CD pipeline using GitHub Actions.
- Optimized Docker multi-stage builds for smaller image size and faster build times.
- Grafana dashboards provisioned for rich observability and visualization of metrics.

The base code included TODO placeholders for metrics, rate limiting, and CI setup.  
All these components have been fully implemented, tested, and integrated.

---

## 2. Quickstart

Follow these steps to get the system running locally:

```bash
# 1. Copy environment configuration file and adjust if necessary
cp .env.example .env

# 2. Build and launch all containers
docker compose up --build

# 3. Access the services on localhost:
# API Endpoint:     http://localhost:8000
# Health Check:     http://localhost:8000/healthz
# Prometheus Metrics: http://localhost:8000/metrics
# Prometheus Server: http://localhost:9090
# Grafana Dashboard: http://localhost:3000  (default user/pass: admin/admin)

✅ Prometheus Metrics – Implemented two key metrics:

REQUEST_COUNT: Counter for total HTTP requests, labeled by method and endpoint.

REQUEST_LATENCY: Histogram measuring request processing time.

✅ Redis-backed Rate Limiting – A decorator limiting the number of requests per minute using Redis, with fail-open to avoid service disruption if Redis is down.

✅ Health Check Endpoint – /healthz returns JSON status for monitoring and readiness checks.

✅ Multi-stage Dockerfile – Efficient image building using builder stage and non-root user execution, ensuring smaller image size and enhanced security.

✅ Grafana Dashboards – Pre-configured JSON dashboards are mounted and provisioned for visualizing application metrics.

✅ CI/CD Pipeline with GitHub Actions – Automated linting, testing, building, and conditional Docker image pushing on the main branch.

✅ YAML Syntax Fixes – All YAML configuration files (Grafana, Prometheus, docker-compose) have been verified and fixed for correct indentation and structure.

✅ Non-root User in Docker – Docker image runs under a non-root user to adhere to security best practices.

4. Architecture Diagram
flowchart LR
    client((Client)) --> app[FastAPI App]
    app -->|/metrics scrape| prom[Prometheus]
    prom --> graf[Grafana]
    app -->|rate limit| redis[(Redis)]

This architecture shows the client sending requests to the FastAPI service, which exposes metrics for Prometheus scraping. Prometheus stores these metrics and Grafana visualizes them. Redis is used by the app to store rate limiting counters.

5. Metrics & Observability
The following Prometheus metrics are exposed by the app at /metrics:

requests_total: Counter of all HTTP requests, labeled by HTTP method and endpoint.

request_latency_seconds: Histogram of request processing times to monitor performance.

These metrics are scraped by Prometheus and visualized on Grafana dashboards.

6. Rate Limiting
Implemented as a Python decorator in rate_limit.py:

Uses Redis to count requests per client IP.

The limit is configurable via RATE_LIMIT_PER_MIN environment variable.

If Redis is unreachable, the system falls back to fail-open mode to avoid blocking traffic.

7. Trade-offs
Multi-stage Docker builds and wheel packages: Achieved smaller images and faster build times but added complexity to the Dockerfile.

--no-deps installs: Used to prevent installation of unwanted or incompatible dependencies.

Redis for rate limiting: Provides efficient and persistent request tracking but adds an external dependency.

Prometheus and Grafana: Provide rich observability but increase system complexity and require careful provisioning and configuration.

8. Troubleshooting
Fixed YAML syntax errors across all project files, especially in Grafana provisioning and Prometheus configs.

Ensured proper mounting of Grafana dashboard directory in docker-compose.yml:
./grafana/provisioning/dashboards:/var/lib/grafana/dashboards:ro
Adjusted service addresses and ports in tests and configs.
Added non-root user execution in Dockerfile to avoid permission issues.

9. Health Check
The endpoint GET /healthz returns:

{
  "status": "ok"
}

10. Testing & CI
Local commands:
make lint    # Run code linting
make test    # Run unit tests
CI Pipeline includes:
Linting (using ruff or pyflakes)

Running tests (pytest)

Docker image build

Conditional image push to Docker Hub on the main branch

