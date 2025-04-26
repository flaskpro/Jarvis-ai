import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ✅ Hardcoded API Key (Ensure this is correct)
API_KEY = "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"

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
