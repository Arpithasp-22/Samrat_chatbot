from fastapi import FastAPI, Request
import uvicorn
from .engine import process_message

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "server is running"}


@app.get("/test")
def test_message():
    return {
        "response": process_message("Total sales in Hyderabad")
    }

from fastapi import Query

VERIFY_TOKEN = "samrat_verify_token"  # you can change this later


@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    return {"error": "Verification failed"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    user_text = data.get("message", "")
    reply = process_message(user_text)
    return {"reply": reply}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
