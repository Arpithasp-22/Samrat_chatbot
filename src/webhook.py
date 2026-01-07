from fastapi import FastAPI, Request
from .engine import process_text
from .send_messages import send_message
import os

app = FastAPI()
@app.get("/samrat_chatbot")
def health_check():
    return {"status": "samrat-chatbot server is running"}



@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            phone_number_id = value.get("metadata", {}).get("phone_number_id")

            for message in value.get("messages", []):
                sender = message["from"]
                text = message["text"]["body"]

                reply = process_text(text)
                send_message(phone_number_id, sender, reply)

    return {"status": "ok"}
