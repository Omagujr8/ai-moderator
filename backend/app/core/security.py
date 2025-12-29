from fastapi import Header, HTTPException
from app.core.config import settings

VALID_KEYS = {"test-key-123"}

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")
