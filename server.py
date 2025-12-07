from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form.to_dict()

        firstname = data.get("firstname", "")
        lastname = data.get("lastname", "")
        email = data.get("email", "")
        phone = data.get("phone", "")

        # Определяем IP клиента
        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.remote_addr

        # Параметры Trackbox
        payload = {
            "ai": "2958294",
            "ci": "1",
            "gi": "292",
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phone": phone.replace("+", ""),  
            "funnel": "Education 365",
            "ip": ip,
            "username": "Neuro",
            "password": "hF7{koC1)p"
        }

        TRACK_URL = "https://track.fintechgurus.org/api/v2/lead/create"

        response = requests.post(TRACK_URL, data=payload, timeout=20)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text,
            "sent_payload": payload
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
