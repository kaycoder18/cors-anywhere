import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Server is running, made by Kay Dee", 200

@app.route('/add_contact_getresponse', methods=['POST'])
def add_contact_getresponse():
    # Get parameters from request body
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    astrology = data.get('astrology')
    date_of_birth = data.get('date_of_birth')
    
    # Get the API key and domain from environment variables
    api_key = os.getenv("GETRESPONSE_API_KEY")
    domain = os.getenv("GETRESPONSE_DOMAIN")

    if not api_key or not domain:
        return jsonify({"error": "API key or domain not found in environment variables"}), 500

    # Construct the payload for the GetResponse API
    payload = {
        "name": name,
        "campaign": {
            "campaignId": "k"  # You can replace this with a dynamic campaign ID if needed
        },
        "email": email,
        "customFieldValues": [
            {"customFieldId": "Uv", "value": [astrology]},  # Custom field for astrology
            {"customFieldId": "U5", "value": [date_of_birth]}  # Custom field for date of birth
        ]
    }

    # Set up the headers
    headers = {
        "Content-Type": "application/json",
        "X-Domain": domain,
        "X-Auth-Token": f"api-key {api_key}"
    }

    # Send the request to the GetResponse API
    response = requests.post('https://api3.getresponse360.com/v3/contacts', json=payload, headers=headers)

    print(response)

    # Handle response from GetResponse API
    if response.status_code == 200:
        return jsonify({"message": "Contact added successfully", "data": response.json()}), 200
    else:
        return jsonify({"error": "Failed to add contact", "details": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
