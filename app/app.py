import os
import time
import logging
import json
from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel

# Prometheus metrics
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from metrics import REQUEST_COUNT, REQUEST_LATENCY

# Rate limiter
from rate_limit import rate_limiter


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "ts": int(time.time() * 1000),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("app")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
logger.addHandler(handler)
logger.propagate = False

app = FastAPI()
PORT = int(os.getenv("PORT", "8000"))
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))


class PredictIn(BaseModel):
    text: str


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict")
@rate_limiter(max_per_min=RATE_LIMIT_PER_MIN)
async def predict(payload: PredictIn, request: Request):
    """Simple sentiment analysis with metrics and rate limiting."""
    start_time = time.time()
    REQUEST_COUNT.inc()

    txt = payload.text.lower()
    label = "positive" if any(k in txt for k in ["good", "great", "love", "awesome"]) else "negative"

    REQUEST_LATENCY.observe(time.time() - start_time)

    logger.info(json.dumps({"path": "/predict", "label": label}))
    return JSONResponse({"label": label})

