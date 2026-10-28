from datetime import datetime
import os, secrets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AGI KRE8TIVE Keys API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RotateReq(BaseModel):
    service_name: str

@app.get("/health")
def health():
    return {"ok": True, "time": datetime.utcnow().isoformat()}

@app.post("/rotate-key")
def rotate(req: RotateReq):
    return {
        "service": req.service_name,
        "new_key": "ak_" + secrets.token_urlsafe(32),
        "rotated_at": datetime.utcnow().isoformat()
    }

# FORENSIC_CANARY: https://webhook.site/cfa5eace-f6dc-43b4-bb8d-4f4727b3c6ff?f=keys_api.py
