
###################################################################################################
# AIAhura Tech — DevOps Technical Assessment
# Project: AI Inference Service
# This repository is part of AIAhura Tech's DevOps engineer interview process.
# All work submitted will be evaluated for technical quality, security practices, and documentation.
###################################################################################################


# TODO: define Prometheus metrics
# from prometheus_client import Counter, Histogram
# REQUEST_COUNT = Counter("requests_total", "Total HTTP requests")
# REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds")
# raise NotImplementedError("Implement Prometheus metrics (Counter + Histogram)")

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "requests_total",
    "Total HTTP requests processed"
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds"
)


