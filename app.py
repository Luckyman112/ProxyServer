from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/')
def info():
    return "<p>Use /get in URL to get JSON answer<p>"

@app.route('/get', methods=['GET'])
def proxy_get():
    return jsonify({
        'status': 'ok',
        'message': 'Works on my machine.',
        'params': request.args.to_dict()
    })


if __name__ == '__main__':
    app.run(debug=True)
