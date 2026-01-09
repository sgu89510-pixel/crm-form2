from flask import Flask, request
import requests
import random
import string
import json

app = Flask(__name__)

API_BASE_URL = "https://void-handler.top/api"
API_ENDPOINT = "/leads"   # стандартный endpoint LeadRouter
API_TOKEN = "53|MLBozB6YD3C63mP8hNarOUI1dVdssXhTKiJjmg2f586921b1"

OFFER_ID = 6
CAMPAIGN_ID = "tbank"

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.route("/")
def index():
    return open("lead_form.html", encoding="utf-8").read()

@app.route("/submit", methods=["POST"])
def submit():

    payload = {
        "offer_id": OFFER_ID,
        "campaign_id": CAMPAIGN_ID,
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "country": "RU",
        "password": generate_password()
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }

    try:
        response = requests.post(
            API_BASE_URL + API_ENDPOINT,
            data=payload,
            headers=headers,
            timeout=15
        )

        try:
            crm_response = response.json()
        except:
            crm_response = response.text

    except Exception as e:
        return f"<pre>Request error:\n{str(e)}</pre>", 500

    safe_payload = payload.copy()
    safe_headers = {"Authorization": "Bearer ********"}

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>CRM Debug</title>
        <style>
            body {{
                background:#0e0e0e;
                color:#00ffcc;
                font-family: monospace;
                padding:20px;
            }}
            pre {{
                background:#000;
                padding:15px;
                border-radius:6px;
                border:1px solid #00ffcc;
            }}
            h2 {{ color:#fff; }}
        </style>
    </head>
    <body>

        <h2>📤 REQUEST</h2>
        <pre>{json.dumps(safe_payload, indent=2, ensure_ascii=False)}</pre>

        <h2>🔐 HEADERS</h2>
        <pre>{json.dumps(safe_headers, indent=2)}</pre>

        <h2>📥 CRM RESPONSE</h2>
        <pre>{json.dumps(crm_response, indent=2, ensure_ascii=False)}</pre>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)