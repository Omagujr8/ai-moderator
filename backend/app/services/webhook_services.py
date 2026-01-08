import requests
import logging

logger = logging.getLogger(__name__)

def send_webhook(url: str, payload: dict):
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        logger.info(f"Webhook sent successfully to {url}")
    except Exception as e:
        logger.error(f"Webhook failed: {e}")
