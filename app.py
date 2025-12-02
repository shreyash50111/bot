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
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403

    if request.method == "POST":
        data = request.json
        # Example: check for messages
        if "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
            messages = data["entry"][0]["changes"][0]["value"]["messages"]
            for msg in messages:
                from_number = msg.get("from")
                body = msg.get("text", {}).get("body")
                group_id = msg.get("group_id", None)
                
                if not ALLOWED_GROUPS or group_id in ALLOWED_GROUPS:
                    twilio_client.messages.create(
                        from_=twilio_whatsapp_number,
                        body=f"From {from_number}: {body}",
                        to=recipient_number
                    )
        return "EVENT_RECEIVED", 200

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
