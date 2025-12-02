from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ===== Configuration =====
ACCESS_TOKEN = "EAALmRlE0bPoBQFkVNlHGgZBQVtySzae6PQcAqoRfq8fMUGF6ZAW84xUO7glanFVL7TSAAFKmt7aAJTbB9bdZAjqTNc1ZA0QKJ2fRhS7ItXMq1ZBvn8Q1bh1s52ZB1T1NzoLv0ePBvZAN1drHW1ZCnNtZBzpZCyyCYFm76pCKXGvnn7uXqrYf7ZAn1t1X38lCZB2eClPHTOaVFLboOomJjkZA9MWftRwhd12B8LsTPpNmlW7nWAEjCglJfxjcHuZBIkyyvbKfyxABuiOKVAQsDUjrQF9HK80LCg"
PHONE_NUMBER_ID = "924586984065346"
FORWARD_TO = "whatsapp:+918971244533"  # Your forwarding number

WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# Optional: forward only from specific groups
ALLOWED_GROUPS = []  # Empty = forward all incoming messages


# ===== Helper functions =====
def send_text_message(to, text):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    r = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    return r.json()


def send_media_message(to, media_id, media_type):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": media_type,
        media_type: {"id": media_id}
    }
    r = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    return r.json()


# ===== Webhook Route =====
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    sender = msg.get("from")
                    msg_type = msg.get("type")

                    if ALLOWED_GROUPS and sender not in ALLOWED_GROUPS:
                        continue

                    if msg_type == "text":
                        text = msg["text"]["body"]
                        send_text_message(FORWARD_TO, f"Forwarded: {text}")
                    elif msg_type in ["image", "video", "document"]:
                        media_id = msg[msg_type]["id"]
                        send_media_message(FORWARD_TO, media_id, msg_type)
    return jsonify(status="ok")


# ===== Verification Route =====
@app.route("/webhook", methods=["GET"])
def verify():
    VERIFY_TOKEN = "691252665011111"  # You can set any string
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


if __name__ == "__main__":
    app.run(port=5000, debug=True)
