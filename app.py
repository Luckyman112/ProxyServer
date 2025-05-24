# app.py
from flask import Flask, Response, request, make_response, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import time

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

def _cors_prelight():
    """Общий preflight для всех эндпойнтов."""
    r = make_response("", 204)
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    r.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return r

@app.route("/v1/models", methods=["GET", "OPTIONS"])
def models():
    if request.method == "OPTIONS":
        return _cors_prelight()
    # возвращаем список моделей
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

@app.route("/v1/chat/completions", methods=["POST", "OPTIONS"])
def completions():
    if request.method == "OPTIONS":
        return _cors_prelight()

    payload = request.get_json() or {}
    payload.setdefault("timestamp", datetime.now().replace(microsecond=0).isoformat())
    # логим в файл
    with open("log.txt", "a", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    def gen():
        # начальный SSE-чанк с ролевой информацией
        chunk0 = {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": int(datetime.now().replace(microsecond=0).timestamp()),
            "model": "gpt-3.5-turbo",
            "choices": [
                {"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}
            ]
        }
        yield f"data: {json.dumps(chunk0)}\n\n"
        time.sleep(0.1)

        # фактический контент
        chunk1 = {
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": "Это тестовый ответ от прокси."},
                    "finish_reason": "stop"
                }
            ]
        }
        yield f"data: {json.dumps(chunk1)}\n\n"
        time.sleep(0.1)

        # закрывающий маркер
        yield "data: [DONE]\n\n"

    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Access-Control-Allow-Origin": "*"
    }
    return Response(gen(), headers=headers)

if __name__ == "__main__":
    # для локальной отладки; в докере запускаем через gunicorn
    app.run(host="0.0.0.0", port=5000, debug=False)
