import os
import secrets
import requests
from flask import Flask, request, jsonify, session
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever']

def load_creds():
    creds = None
    token_file = 'token.json'
    client_secrets_file = 'client_secret.json'

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds

@app.before_request
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

@app.route('/generate', methods=['POST'])
def generate():
    # Verify the CSRF token
    csrf_token = session.get('csrf_token')
    if csrf_token != request.form.get('csrf_token'):
        return jsonify({'error': 'CSRF token mismatch'}), 403

    try:
        user_input = request.form.get('input', '')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        creds = load_creds()
        access_token = creds.token

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