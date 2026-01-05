# import requests
#
# def send_webhook(url: str, payload: dict):
#     try:
#         requests.post(url, json=payload, timeout=5)
#     except Exception:
#         pass
import requests
from app.core.logging import logger

def send_webhook(url: str, payload: dict):
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        logger.info(f"Webhook sent to {url}")
    except Exception as e:
        logger.error(f"Webhook failed: {e}")
