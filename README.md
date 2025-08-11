## Trade-offs and Troubleshooting

### Trade-offs
- **Multi-stage build** + **wheels** → smaller image, faster builds (`--no-cache-dir` to skip cache).
- **`--no-deps`** → avoid installing incompatible dependencies.
- **Redis rate limiting** → fast, persistent storage with **fail-open** if Redis is down.
- **Prometheus metrics** (`REQUEST_COUNT`, `REQUEST_LATENCY`) → monitor request volume and latency.
- **Prometheus + Grafana** → strong observability, with extra setup complexity.
- **Non-root user** in container → improved security and isolation.

**CI Pipeline:**
- Defined in `.github/workflows/ci.yml`.
- Steps include:
  - Linting with ruff or pyflakes.
  - Testing with pytest.
  - Building Docker image.
  - Conditional push to container registry on main branch.

---

### Troubleshooting
- Fixed **YAML syntax errors** across the project (mostly indentation issues and formatting).
- Mounted Grafana dashboards correctly in `docker-compose.yml`:

  ```yaml
  ./grafana/provisioning/dashboards:/var/lib/grafana/dashboards:ro
