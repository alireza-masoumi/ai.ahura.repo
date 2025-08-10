
###################################################################################################
# AIAhura Tech — DevOps Technical Assessment
# Project: AI Inference Service
# This repository is part of AIAhura Tech's DevOps engineer interview process.
# All work submitted will be evaluated for technical quality, security practices, and documentation.
###################################################################################################


from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_healthz():
 r = client.get("/healthz")
 assert r.status_code == 200
 assert r.json()["status"] == "ok"

def test_predict():
 r = client.post("/predict", json={"text": "I love this product"})
 assert r.status_code == 200
 assert r.json()["label"] in ["positive", "negative"]
