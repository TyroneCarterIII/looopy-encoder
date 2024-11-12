# app.py
from flask import Flask, request, jsonify
import jwt
import time
import os

app = Flask(__name__)

# Load your API key from environment variable or hardcode for testing
API_KEY = os.getenv("SERVICE_API_KEY", "your-secure-api-key")

@app.route('/generate-token', methods=['POST'])
def generate_token():
    # Verify API key
    request_api_key = request.headers.get("X-API-KEY")
    if request_api_key != API_KEY:
        return jsonify({"error": "Invalid API key"}), 403

    # Fetch parameters from JSON request body
    data = request.json
    api_key = data.get("api_key")
    api_secret = data.get("api_secret")
    username = data.get("username")

    if not api_key or not api_secret or not username:
        return jsonify({"error": "API key, API secret, and username are required"}), 400

    # Create payload
    payload = {
        "uid": api_key,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,  # Expires in 1 hour
        "username": username,
        "pid": api_key
    }

    # Encode JWT
    token = jwt.encode(payload, api_secret, algorithm="HS256")
    
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
