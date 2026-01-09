import logging
from src.csv_data import get_total_sales_by_city
from src.send_message import send_message

logger = logging.getLogger(__name__)


def process_message(text: str) -> str:
    text = text.lower().strip()

    if "sales" in text and "in" in text:
        words = text.split()
        try:
            in_index = words.index("in")
            city = " ".join(words[in_index + 1:])
        except ValueError:
            city = ""

        if city:
            total = get_total_sales_by_city(city)
            if total > 0:
                return f"Total sales in {city.title()} are ₹{total:,.2f}."
            else:
                return f"No sales data found for {city.title()}."

    if any(word in text for word in ["help", "hi", "hello", "start"]):
        return (
            "👋 Welcome to Sales Chatbot!\n\n"
            "Try asking:\n"
            "• Total sales in Hyderabad\n"
            "• Sales in Mumbai\n"
            "• Sales data for Bangalore"
        )

    return "I can help with sales queries! Try asking: 'Total sales in [city]'"


def handle_message(message: dict, phone_number_id: str = None) -> None:
    sender_id = message.get("from")
    if not sender_id:
        return

    text = ""
    if isinstance(message.get("text"), dict):
        text = message["text"].get("body", "")

    reply = process_message(text) if text else "Please send a text message."
    send_message(sender_id, reply, phone_number_id)
