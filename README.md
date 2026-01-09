# WhatsApp Sales Chatbot

A FastAPI-based WhatsApp chatbot that provides sales data queries from a CSV file.

## Features

✅ Receives messages from WhatsApp Business API  
✅ Processes natural language queries about sales by city  
✅ Sends responses back via WhatsApp  
✅ Webhook verification for WhatsApp integration  
✅ CSV-based sales data lookup  

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your WhatsApp credentials:

```bash
cp .env.example .env
```

Edit `.env` with:
- `WHATSAPP_ACCESS_TOKEN`: Your WhatsApp Business API token
- `PHONE_NUMBER_ID`: Your WhatsApp Business Phone Number ID

### 3. Add Your Sales Data

Place your CSV file at: `data/All_combined_22-25.csv`

Required columns:
- `City` (or similar)
- `Basic Amount` (or sales amount column)

### 4. Start the Server

```bash
uvicorn src.webhook:app --host 0.0.0.0 --port 8000
```

### 5. Expose Locally with ngrok (for testing)

```bash
ngrok http 8000
```

### 6. Configure WhatsApp Webhook

In Meta Business Suite:
1. Go to WhatsApp > Configuration
2. Set Webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
3. Set Verify Token: `samrat_verify_token` (or your custom token)
4. Subscribe to messages and message_template_status_update webhooks

## API Endpoints

- `GET /` - Health check
- `GET /test` - Test message processing
- `GET /webhook` - Webhook verification (WhatsApp)
- `POST /webhook` - Receive and process messages from WhatsApp

## Usage

Users can send messages to your WhatsApp number like:
- "Total sales in Hyderabad"
- "What are sales in Mumbai?"
- "Sales data for Bangalore"
- "Hello" (for help)

## File Structure

```
├── data/
│   └── All_combined_22-25.csv      # Sales data
├── src/
│   ├── __init__.py
│   ├── csv_data.py                 # CSV loading & queries
│   ├── engine.py                   # Message processing logic
│   ├── webhook.py                  # FastAPI webhook endpoints
│   └── send_messages.py            # WhatsApp API integration
├── requirements.txt                # Dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## Troubleshooting

### "Missing WHATSAPP_ACCESS_TOKEN or PHONE_NUMBER_ID"
- Ensure `.env` file exists with correct credentials
- Restart the server after updating `.env`

### Webhook verification fails
- Check that VERIFY_TOKEN in `.env` matches the one in your WhatsApp settings
- Ensure server is accessible via ngrok URL

### No CSV data found
- Verify CSV file exists at `data/All_combined_22-25.csv`
- Check that column names match exactly (case-sensitive)

## Next Steps

- Add more query types (monthly sales, top cities, etc.)
- Implement conversation history
- Add authentication/authorization
- Deploy to production (AWS, Heroku, etc.)
