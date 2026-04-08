import re
import time
import requests

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ===== ДАННЫЕ ИНТЕГРАЦИИ =====
AFFILIATE_BASE_URL = "https://YOUR-DOMAIN.COM"   # сюда вставь реальный домен API
AFFILIATE_API_TOKEN = "TRybIRvfXsjaCfBfVCe2HF5NcZxIo4VHRAAW0PhuRZ3ArcG6SHl2fowRdYc8"
LINK_ID = "14"
FUNNEL = "Test"
DEFAULT_COUNTRY = "RU"
DEFAULT_LANGUAGE = "ru"
DEFAULT_SOURCE = "RenderForm"
AFFILIATE_PASSWORD = r")=mu^@4%r1n=w>8*PB$P"
FORM_DOMAIN = "YOUR-DOMAIN.COM"
# =============================

def get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.headers.get("X-Real-IP", "") or request.remote_addr or ""

def normalize_phone(phone: str) -> str:
    return (phone or "").strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

def is_valid_phone(phone: str) -> bool:
    return bool(re.fullmatch(r"^\+[1-9]\d{7,14}$", phone))

def generate_email_from_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if not digits:
        digits = str(int(time.time()))
    return f"lead_{digits}_{int(time.time())}@example.com"

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(".", "lead_form.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "config": {
            "AFFILIATE_BASE_URL": AFFILIATE_BASE_URL,
            "LINK_ID": LINK_ID,
            "FUNNEL": FUNNEL
        }
    })

@app.route("/submit-lead", methods=["POST"])
def submit_lead():
    incoming = request.get_json(silent=True) or {}

    fname = (incoming.get("fname") or "").strip()
    lname = (incoming.get("lname") or "").strip()
    fullphone = normalize_phone(incoming.get("fullphone") or "")
    ip = get_client_ip()

    if not fname:
        return jsonify({"success": False, "message": "Имя обязательно"}), 400

    if not lname:
        return jsonify({"success": False, "message": "Фамилия обязательна"}), 400

    if not fullphone:
        return jsonify({"success": False, "message": "Телефон обязателен"}), 400

    if not is_valid_phone(fullphone):
        return jsonify({
            "success": False,
            "message": "Телефон должен быть в формате E.164, например +79991234567"
        }), 400

    email = generate_email_from_phone(fullphone)

    payload = {
        "link_id": LINK_ID,
        "fname": fname,
        "lname": lname,
        "email": email,
        "fullphone": fullphone,
        "ip": ip,
        "country": DEFAULT_COUNTRY,
        "language": DEFAULT_LANGUAGE,
        "source": DEFAULT_SOURCE,
        "funnel": FUNNEL,
        "pass": AFFILIATE_PASSWORD,
        "domain": FORM_DOMAIN
    }

    api_url = f"{AFFILIATE_BASE_URL}/api/v3/integration"

    try:
        response = requests.post(
            api_url,
            params={"api_token": AFFILIATE_API_TOKEN},
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=20
        )

        try:
            result = response.json()
        except Exception:
            return jsonify({
                "success": False,
                "message": f"Affiliate API вернул не JSON: {response.text[:300]}"
            }), 502

        if response.ok and result.get("success") is True:
            return jsonify({
                "success": True,
                "message": "Лид успешно создан",
                "lead_id": result.get("id"),
                "autologin": result.get("autologin"),
                "password": result.get("password")
            }), 200

        return jsonify({
            "success": False,
            "message": result.get("message", "Ошибка affiliate API"),
            "api_response": result
        }), 400

    except requests.RequestException as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка запроса: {str(e)}"
        }), 502

@app.route("/api/leads", methods=["GET"])
def get_leads():
    params = {
        "api_token": AFFILIATE_API_TOKEN,
        "limit": request.args.get("limit", "100"),
        "page": request.args.get("page", "1"),
        "link_id": request.args.get("link_id", LINK_ID)
    }

    acq = request.args.get("acq")
    if acq in ("0", "1"):
        params["acq"] = acq

    api_url = f"{AFFILIATE_BASE_URL}/api/v3/get-leads"

    try:
        response = requests.get(api_url, params=params, timeout=20)

        try:
            result = response.json()
        except Exception:
            return jsonify({
                "success": False,
                "message": f"Affiliate API вернул не JSON: {response.text[:300]}"
            }), 502

        return jsonify(result), response.status_code

    except requests.RequestException as e:
        return jsonify({
            "success": False,
            "message": f"Ошибка запроса: {str(e)}"
        }), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)