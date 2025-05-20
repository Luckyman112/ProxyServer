from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

@app.route('/v1/models', methods=['GET', 'OPTIONS'])
def get_models():
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "gpt-3.5-turbo",
                "object": "model",
                "created": 0,
                "owned_by": "proxy-server",
                "permission": []
            }
        ]
    })

@app.route('/v1/chat/completions', methods=['POST', 'OPTIONS'])
def save_config():
    if request.method == 'OPTIONS':
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    request_data = request.get_json()
    request_data['timestamp'] = datetime.now().isoformat()
    with open("log.txt", "a", encoding="utf-8") as log_file:
        json.dump(request_data, log_file, ensure_ascii=False, indent=4)
        log_file.write("\n")
    return jsonify(request_data)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
