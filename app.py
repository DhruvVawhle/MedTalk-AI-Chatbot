from flask import Flask, render_template, request, jsonify  # ✅ Removed duplicate Flask import
from flask_cors import CORS
import google.generativeai as genai
import logging
import time
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

logging.basicConfig(level=logging.DEBUG)

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCPiNTKaXzCGG7XZheRum65hV1IStb-o0M")
genai.configure(api_key=API_KEY)

last_quota_error_time = 0
quota_wait_seconds = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favicon.ico")
def favicon():
    return "", 204

@app.route("/chat", methods=["POST"])
def chat():
    global last_quota_error_time, quota_wait_seconds

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    current_time = time.time()
    if current_time < last_quota_error_time + quota_wait_seconds:
        wait_time = int(last_quota_error_time + quota_wait_seconds - current_time)
        return jsonify({"error": f"Quota cooldown. Wait {wait_time}s."}), 429

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # ✅ Higher free quota than 2.0-flash
        response = model.generate_content(user_message)

        bot_reply = response.text if (response and hasattr(response, "text")) else "No response generated."
        logging.info(f"Reply: {bot_reply}")
        return jsonify({"reply": bot_reply})

    except Exception as e:
        error_msg = str(e)
        logging.error(f"Gemini error: {error_msg}")

        if "429" in error_msg or "quota" in error_msg.lower() or "ResourceExhausted" in error_msg:
            quota_wait_seconds = 60
            try:
                if "retry in" in error_msg.lower():
                    wait_str = error_msg.split("retry in ")[-1].split("s")[0]
                    quota_wait_seconds = int(float(wait_str)) + 5
            except:
                pass
            last_quota_error_time = time.time()
            return jsonify({"error": f"Quota exceeded. Retry in {quota_wait_seconds}s."}), 429

        elif "401" in error_msg or "invalid" in error_msg.lower():
            return jsonify({"error": "Invalid API key."}), 401

        return jsonify({"error": "Server error: " + error_msg}), 500

if __name__ == "__main__":
    app.run(debug=True)