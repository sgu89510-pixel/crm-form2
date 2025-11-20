from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="")
CORS(app)

# ОТДАТЬ ФОРМУ
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "lead_form.html")

# ОТПРАВКА ЛИДА
@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    # Получаем IP (необязательно, но можно)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    url = "https://elvioncrm62.pro/api/add_lead"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": "gnG4ILxVgUPdmAtpqjUH2DlUoJKRN0JK"
    }

    payload = {
        "name": f"{data.get('firstname', '')} {data.get('lastname', '')}".strip(),
        "email": data.get("email", ""),
        "phone": data.get("phone", "").replace("+", "").replace(" ", ""),
        "country": "KZ",
        "language": "RU",
        "source": "Kazakhstan Landing",
        "source_url": "https://punk2077.onrender.com",
        "comment": f"Lead from landing. IP: {ip}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
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