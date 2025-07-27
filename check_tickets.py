import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
PRICE_THRESHOLD = int(os.environ.get("PRICE_THRESHOLD", 2000000))

API_URL = "https://nta.tripodeck.com/api/official/usj/list"
PARAMS = {
    "startTime": "2025-07-27",
    "endTime": "2025-10-31",
    "ticketKind": 3,
    "productId": 10009984
}

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    response = requests.get(API_URL, params=PARAMS)
    response.raise_for_status()
    data = response.json().get("data", [])

    matches = []
    for entry in data:
        price = entry.get("price", 0)
        date = entry.get("travelTime", "")[:10]
        if price and price <= PRICE_THRESHOLD:
            matches.append(f"{date}: ¥{price // 100}")

    if matches:
        body = "\n".join(matches)
        subject = f"[USJ Tickets] 🎟️ Matching tickets found - {datetime.utcnow().isoformat()}"
        send_email(subject, body)

if __name__ == "__main__":
    main()
