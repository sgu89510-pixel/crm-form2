from flask import Flask, request
import requests
import random
import string
import json

app = Flask(__name__)

API_URL = "https://affs-lead.info/lion/new-lead"
API_TOKEN = "Q9T2A6kM8yJwC0D5F4pN7S1uLRHb"

def generate_password():
    # минимум 10 символов (буквы + цифры)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.route("/")
def index():
    return open("lead_form.html", encoding="utf-8").read()

@app.route("/submit", methods=["POST"])
def submit():

    # ДАННЫЕ ДЛЯ CRM (СТРОГО ПО ДОКУМЕНТАЦИИ)
    payload = {
        "Name": request.form.get("first_name"),
        "LastName": request.form.get("last_name"),
        "Email": request.form.get("email"),
        "Phone": request.form.get("phone"),
        "Password": generate_password(),
        "Country": "RU",
        "Source": "Landing RU",
        "Token": API_TOKEN
    }

    try:
        response = requests.post(API_URL, data=payload, timeout=15)
        try:
            crm_response = response.json()
        except:
            crm_response = response.text

    except Exception as e:
        return f"<pre>Request error:\n{str(e)}</pre>", 500

    # 🔒 Маскируем токен для отображения
    safe_payload = payload.copy()
    safe_payload["Token"] = "********"

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>CRM Debug</title>
        <style>
            body {{
                font-family: monospace;
                background: #0e0e0e;
                color: #00ffcc;
                padding: 20px;
            }}
            pre {{
                background: #000;
                padding: 15px;
                border-radius: 6px;
                border: 1px solid #00ffcc;
            }}
            h2 {{
                color: #ffffff;
            }}
        </style>
    </head>
    <body>

        <h2>📤 REQUEST TO CRM</h2>
        <pre>{json.dumps(safe_payload, indent=2, ensure_ascii=False)}</pre>

        <h2>📥 CRM RESPONSE</h2>
        <pre>{json.dumps(crm_response, indent=2, ensure_ascii=False)}</pre>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)