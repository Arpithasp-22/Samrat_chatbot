from .csv_data import get_total_sales_by_city


def process_message(text: str) -> str:
    """
    Takes user text and returns a response string
    """
    text = text.lower().strip()

    # Very simple rule-based logic for now
    if "sales" in text and "in" in text:
        city = text.split()[-1]
        total = get_total_sales_by_city(city)

        if total == 0:
            return f"No sales data found for {city.title()}."

        return f"Total sales in {city.title()} are ₹{total:,.2f}."

    return "I can help with questions like: 'Total sales in Hyderabad'."


if __name__ == "__main__":
    print(process_message("Total sales in Hyderabad"))
    print(process_message("Total sales in Mumbai"))
    print(process_message("hello"))
