import requests
import time

TELEGRAM_BOT_TOKEN = "8858466092:AAF2_YCAukhlvrKgVbBD0levV0i6Gbuag90"
TELEGRAM_CHAT_ID = "1370315348"

def send_alert(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

if __name__ == "__main__":
    print("Raseen Bot Engine Started...")
    send_alert("🤖 *تم تفعيل بوت رصين الآلي بنجاح وجاهز لرصد الصفقات*")
