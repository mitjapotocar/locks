from flask import Flask, jsonify
from env import constants
from routes import locks_bp
from flask_cors import CORS
from datetime import timedelta
import logging
from models import db
import os

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}},
     methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin"])

app.register_blueprint(locks_bp, url_prefix='/locks')

@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error), message="Resource not found."), 404


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
