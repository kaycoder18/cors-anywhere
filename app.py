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
        "dayOfCycle": "0",
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
    try:
        response = requests.post('https://api3.getresponse360.com/v3/contacts', json=payload, headers=headers)

        # Check if the response status code is 409 (Conflict)
        if response.status_code == 409:
            return jsonify({
                "error": "Conflict: The contact may already exist.",
                "details": response.text,
                "status_code": response.status_code
            }), 409

        # Try to parse the JSON response
        if response.content:
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({
                "error": "Empty response from GetResponse API",
                "status_code": response.status_code
            }), response.status_code

    except requests.exceptions.JSONDecodeError as e:
        return jsonify({
            "error": "Failed to decode JSON from response",
            "details": str(e),
            "response_text": response.text if response else "No response content"
        }), 500



@app.route('/add_contact_sender_net', methods=['POST'])
def add_contact_sender_net():
    # Get parameters from request body
    data = request.get_json()
    email = data.get('email')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

    # Get the Bearer token from environment variables
    bearer_token = os.getenv("SENDER_NET_BEARER_TOKEN")

    if not bearer_token:
        return jsonify({"error": "Bearer token not found in environment variables"}), 500

    # Construct the payload for the sender.net API
    payload = {
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
        "groups": ["e1QDl0"],  # You can change this as per your needs
        "trigger_automation": True
    }

    # Set up the headers
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Send the request to the sender.net API
    try:
        response = requests.post('https://api.sender.net/v2/subscribers', json=payload, headers=headers)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({
                "error": f"Error: {response.status_code}",
                "details": response.text
            }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to send request to sender.net API",
            "details": str(e)
        }), 500



if __name__ == '__main__':
    app.run(debug=True)
