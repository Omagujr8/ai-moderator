import requests

def send_webhook(url: str, payload: dict):
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass
