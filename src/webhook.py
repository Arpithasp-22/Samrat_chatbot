from fastapi import FastAPI, Request, HTTPException, Query
import os
from dotenv import load_dotenv
from src.engine import handle_message

load_dotenv()

# ✅ app MUST be defined before decorators
app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


# Health check
@app.get("/")
async def home():
    return {"message": "API is up"}


# Webhook verification (GET)
@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Forbidden")


# Webhook receiver (POST)
@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    print("Received webhook:", data)

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})

            messages = value.get("messages")
            if not messages:
                return {"status": "ignored"}

            metadata = value.get("metadata", {})
            phone_number_id = metadata.get("phone_number_id")
            bot_phone_number = metadata.get("display_phone_number")

            for message in messages:
                # 🚫 Ignore bot's own messages
                if message.get("from") == bot_phone_number:
                    continue

                # ✅ Only text messages
                if message.get("type") != "text":
                    continue

                handle_message(message, phone_number_id)

    return {"status": "EVENT_RECEIVED"}
