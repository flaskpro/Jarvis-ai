import requests
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ✅ Get API Key securely
API_KEY = os.getenv("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")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-reply", methods=["POST"])
def get_reply():
    """Handles user input and returns AI-generated response."""
    data = request.get_json()
    if not data or "user_input" not in data:
        return jsonify({"error": "Invalid request format"}), 400
    
    user_input = data["user_input"]
    reply = fetch_reply(user_input)
    
    return jsonify({"reply": reply})

def fetch_reply(user_input):
    """Fetch response from OpenRouter AI API."""
    if not API_KEY:
        return "⚠️ API Key is missing!"

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_input}]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  

        response_data = response.json()
        if "choices" in response_data and response_data["choices"]:
            return response_data["choices"][0]["message"]["content"]
        
        return "⚠️ No valid response received!"
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ API Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
