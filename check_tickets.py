import os
import requests
import smtplib
from email.mime.text import MIMEText
import time


EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = 587
DATE = "2025-10-08"

PRODUCT_ID_TO_PASS = {
    10009965: "Universal Express Pass 4: Fun Variety",
    10009981: "Universal Express Pass 4: 4D & Minions",
    10009984: "Universal Express Pass 4: Mine Cart & Fun",
}
API_URL = "https://nta.tripodeck.com/api/official/usj/list"
PARAMS = [
    {
        "startTime": "2025-10-01",
        "endTime": "2025-10-31",
        "ticketKind": 3,
        "productId": 10009984,
    },
    {
        "startTime": "2025-10-01",
        "endTime": "2025-10-31",
        "ticketKind": 3,
        "productId": 10009981,
    },
    {
        "startTime": "2025-10-01",
        "endTime": "2025-10-31",
        "ticketKind": 3,
        "productId": 10009965,
    },
]


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
    for param in PARAMS:
        matches = []
        response = requests.get(API_URL, params=param)
        response.raise_for_status()
        data = response.json().get("data", [])
        data = [
            entry
            for entry in data
            if entry["travelTime"].startswith(DATE) and entry["num"] > 0
        ]
        if data:
            price = data[0].get("price", 0)
            date = data[0].get("travelTime", "")[:10]
            matches.append(f"{date}: ¥{price // 100}")
        else:
            print(f"No matches for {PRODUCT_ID_TO_PASS[param['productId']]} :(")

        time.sleep(5)

        if matches:
            body = "\n".join(matches)
            subject = (
                f"[USJ Tickets] 🎟️ Matching tickets found for {PRODUCT_ID_TO_PASS[param['productId']]}"
            )
            print("success, sending email")
            send_email(subject, body)


if __name__ == "__main__":
    main()
