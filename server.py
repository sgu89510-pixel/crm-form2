from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


@app.route("/send_lead", methods=["POST"])
def send_lead():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "Нет данных"}), 400

        payload = {
            "name": data.get("name"),
            "country": data.get("country"),
            "phone": data.get("phone"),
            "car_year": data.get("car_year"),
            "comment": data.get("comment")
        }

        CRM_URL = "http://144.124.251.253/lead_capture.php"

        headers = {"Content-Type": "application/json"}

        response = requests.post(CRM_URL, json=payload, headers=headers, timeout=20)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text,
            "sent_payload": payload
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)