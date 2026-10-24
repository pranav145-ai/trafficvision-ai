from flask import Flask
from flask_cors import CORS
from routes.detect import detect_bp

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.register_blueprint(detect_bp, url_prefix="/api")

@app.get("/")
def home():
    return {"project": "TrafficVision AI", "status": "backend online", "mode": "mock"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
