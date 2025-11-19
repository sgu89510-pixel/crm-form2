from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="")
CORS(app)

# === ОТДАЧА ФОРМЫ ===
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "lead_form.html")

# === ОТПРАВКА ЛИДА В CRM ===
@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    # Получение IP клиента
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if ip is None or ip.strip() == "":
        ip = "127.0.0.1"

    crm_url = "https://stormchg.biz/api/external/integration/lead"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": "a9e96a13-9d82-465c-a111-085b94756b81"
    }

    payload = {
        "affc": "AFF-7HXBU5456B",
        "bxc": "BX-6MWDHF8F519II",
        "vtc": "VT-HP8XSRMKVS6E7",

        "profile": {
            "firstName": data.get("name", ""),
            "lastName": data.get("lastname", ""),
            "email": data.get("email", ""),
            "password": "AutoGen123!",
            "phone": data.get("phone", "").replace("+", "").replace(" ", "").replace("-", "")
        },

        "ip": ip,
        "funnel": "kaz_atom",
        "landingURL": "https://walloram.onrender.com",
        "geo": "KZ",
        "lang": "ru",
        "landingLang": "ru",
        "userAgent": request.headers.get("User-Agent", "")
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
    app.run(host="0.0.0.0", port=port, debug=False)