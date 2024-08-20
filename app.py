import os
import requests
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever']

# Load OAuth 2.0 credentials from the credentials.json file
def load_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get user input from request JSON
        user_input = request.json.get('input', '')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        creds = load_creds()
        access_token = creds.token

        # Define the API URL and headers for generating content
        generate_url = 'https://generativelanguage.googleapis.com/v1beta/tunedModels/make-house-plan-of-plan-house-model-q0h8:generateContent'
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        request_payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"input: {user_input}"}, {"text": "output: "}]}
            ],
            "generation_config": generation_config
        }
        
        # Make the API request
        response = requests.post(
            generate_url,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            json=request_payload
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error generating content: {response.status_code} - {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/token', methods=['GET', 'POST'])
def delete_token():
    try:
        token_file = 'token.json'
        if os.path.exists(token_file):
            os.remove(token_file)
            # Simulate a request to the /generate route to create a new token
            load_creds()
            return jsonify({"message": "Token file deleted successfully"}), 200
        else:
            load_creds()
            return jsonify({"error": "Token file does not exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
