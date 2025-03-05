from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS to allow requests from your frontend

@app.route('/fetch_html', methods=['GET'])
def fetch_html():
    url = request.args.get('url')  # Get the URL from the query parameter
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        return jsonify({'html': response.text})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
