import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is running, made by Kay Dee", 200
    
@app.route('/add_contact', methods=['POST'])
def add_contact():
    # Get the API key from the environment variable
    api_key = os.getenv("GETRESPONSE_API_KEY")

    if not api_key:
        return jsonify({"error": "API key not found in environment variables"}), 500

    # Use the incoming JSON data as the payload
    payload = request.get_json()

    # Set up the headers
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": f"api-key {api_key}"
    }

    # Send the request to the GetResponse API
    response = requests.post('https://api.getresponse.com/v3/contacts', json=payload, headers=headers)

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
