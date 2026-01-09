import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID_ENV = os.getenv("PHONE_NUMBER_ID")

logger = logging.getLogger(__name__)


def send_message(to: str, message: str, phone_number_id: str = None):
    """Send a WhatsApp text message via the Graph API."""
    phone_id = phone_number_id or PHONE_NUMBER_ID_ENV

    if not ACCESS_TOKEN or not phone_id:
        logger.error("Missing ACCESS_TOKEN or PHONE_NUMBER_ID")
        return

    url = f"https://graph.facebook.com/v22.0/{phone_id}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        logger.error("WhatsApp API error %s: %s", response.status_code, response.text)
    else:
        logger.info("Message sent to %s", to)
