import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS 

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Server is running, made by Kay Dee", 200

@app.route('/add_contact', methods=['POST'])
def add_contact():
    # Get the API key and domain from the environment variables
    api_key = os.getenv("GETRESPONSE_API_KEY")
    domain = os.getenv("GETRESPONSE_DOMAIN")

    if not api_key or not domain:
        return jsonify({"error": "API key or domain not found in environment variables"}), 500

    # Use the incoming JSON data as the payload
    payload = request.get_json()

    # Set up the headers
    headers = {
        "Content-Type": "application/json",
        "X-Domain": domain,  # Pass the domain from environment variable
        "X-Auth-Token": f"api-key {api_key}"
    }

    # Construct the payload in the exact structure as your example
    data = {
        "name": payload.get("name", ""),
        "campaign": {
            "campaignId": payload.get("campaignId", "")
        },
        "email": payload.get("email", ""),
        "customFieldValues": [
            {"customFieldId": "Uv", "value": [payload.get("customValue1", "")]},
            {"customFieldId": "U5", "value": [payload.get("customValue2", "")]}
        ]
    }

    # Send the request to the GetResponse API
    response = requests.post('https://api3.getresponse360.com/v3/contacts', json=data, headers=headers)

    # Check if the response is not empty
    if response.content:
        try:
            return jsonify(response.json()), response.status_code
        except ValueError:  # Catch JSONDecodeError
            return jsonify({"error": "Failed to decode JSON from response", "response": response.text}), response.status_code
    else:
        return jsonify({"error": "Empty response from GetResponse API"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
