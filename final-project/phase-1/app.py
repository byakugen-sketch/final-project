from flask import Flask, jsonify
import os
app = Flask(__name__)
@app.route("/")
def home():
    return jsonify({"message": "Hello, Doron!"}), 200

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/version")
def version():
    return jsonify({"version": os.environ.get("APP_VERSION", "1.0.0")}), 200

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug)