import json
from flask import Flask, request, jsonify, make_response
import jwt
from functools import wraps
from model import load_model, predict_label

app = Flask(__name__)

def get_model():
    return load_model()

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['RS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Signature expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(data, *args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    return "OK"

@app.route("/predict", methods=['POST'])
def predict_route():
    ai_model = get_model()
    json = request.get_json()
    print(json)
    prediction = predict_label(prompt=json["prompt"], classifier=ai_model.model, vectorizer=ai_model.vectorizer)
    return jsonify({"prediction": prediction})

app.run()