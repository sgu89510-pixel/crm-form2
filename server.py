from flask import Flask, request, send_file, jsonify
import requests

app = Flask(__name__)

# ================= НАСТРОЙКИ =================
API_URL = "https://api.fx-bit.org/api/v1/integration/lead/leads"
TOKEN = "WRK1zGPmgjlPmGIv"

GEO = "KZ"
CAMPAIGN = "kazchrome"

# ================= ROUTES =================
@app.route("/", methods=["GET"])
def index():
    return send_file("lead_form.html")

@app.route("/submit", methods=["POST"])
def submit():
    payload = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "campaign": CAMPAIGN,
        "second_phone": None,
        "extra_info": "Lead from landing",
        "geo": GEO
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            API_URL,
            params={"token": TOKEN},   # ⚠️ token В QUERY
            json=payload,
            headers=headers,
            timeout=15
        )

        return jsonify({
            "status_code": response.status_code,
            "request": payload,
            "response": response.json()
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "request": payload
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)