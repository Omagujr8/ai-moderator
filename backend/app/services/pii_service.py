import re
import hashlib

def mask_email(text: str) -> str:
    """Replace emails with [REDACTED]"""
    return re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[REDACTED]", text)

def hash_username(username: str) -> str:
    """Return a SHA256 hash of the username"""
    return hashlib.sha256(username.encode()).hexdigest()
