from fastapi import Header, HTTPException
from app.core.config import settings

API_KEYS = {
    "test-key-123": {"role": "client"},
    "admin-key-456": {"role": "admin"},
}

def verify_api_key(api_key: str = Security(APIKeyHeader(name="X-API-KEY"))):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return API_KEYS[api_key]

