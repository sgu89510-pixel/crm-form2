from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="")
CORS(app)

# === СТАТИЧЕСКИЙ ФАЙЛ (ФОРМА) ===
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "lead_form.html")


# === ОТПРАВКА ЛИДА В CRM ===
@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    # IP клиента
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip in ["127.0.0.1", "0.0.0.0", "::1"]:
        ip = "8.8.8.8"

    # === НОВАЯ CRM: данные, которые ты дал ===
    crm_url = "https://elvioncrm62.pro/api/add_lead"
    headers = {
        "Content-Type": "application/json",
        "api-key": "gnG4ILxVgUPdmAtpqjUH2DlUoJKRN0JK"
    }

    # === Формируем payload ===
    payload = {
        "first_name": data.get("name", ""),
        "last_name": data.get("lastname", ""),
        "email": data.get("email", ""),
        "phone": data.get("phone", "").replace("+", "").replace(" ", "").replace("-", ""),
        "geo": "KZ",
        "ip": ip,
        "landing_url": "https://punk2077.onrender.com",
        "sub_id": None
    }

    try:
        response = requests.post(crm_url, headers=headers, json=payload, timeout=30)
        return jsonify({
            "crm_response": response.text,
            "crm_status": response.status_code,
            "success": response.ok
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)