from flask import Flask, jsonify, request
import os
import logging
import time
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.after_request
def log_request(response):
    logger.info(
        "request",
        extra={
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "remote_addr": request.remote_addr,
        },
    )
    return response

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html>
<head>
  <title>Flask App</title>
</head>
<body style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;margin:0;background:#111;color:#fff;font-family:sans-serif;">
  <img src="/static/hal9000.png" style="width:320px;border-radius:50%;margin-bottom:32px;">
  <h1 style="font-size:2rem;letter-spacing:0.05em;">Hello Doron, how can I help you today?</h1>
</body>
</html>""", 200

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/version")
def version():
    return jsonify({"version": os.environ.get("APP_VERSION", "1.0.0")}), 200

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug)
