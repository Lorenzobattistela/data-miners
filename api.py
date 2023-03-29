
from flask import Flask, request, jsonify, render_template, redirect, url_for
import jwt
from functools import wraps
from model import load_model, predict_label
from msg_queue import Database
from website import ContactMessage, load_messages

SPAM = 0
HAM = 1

app = Flask(__name__)


def get_model():
    return load_model()


def delete_message(msg_id: str):
    db = Database("msg_queue.sqlite")
    db.connect()
    db.delete_message_by_id(msg_id)


def get_messages():
    db = Database("msg_queue.sqlite")
    db.connect()
    return db.get_all_messages()


def store_message_in_queue(message: str, prediction: str):
    db = Database("msg_queue.sqlite")
    db.connect()
    is_spam = SPAM if prediction == "spam" else HAM
    db.insert_message(message=message, is_spam=is_spam)
    db.close()


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


@app.route("/form/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        contact_messages = load_messages()
        return render_template("contact.html", messages=contact_messages)

    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    contact_message = ContactMessage(name, email, message)
    saved = contact_message.save_to_csv()
    return jsonify({"status": 201}) if saved else jsonify({"status": 500})


@app.route("/admin/queue", methods=['GET', 'POST'])
def msg_queue():
    if request.method == 'GET':
        messages = get_messages()
        return render_template("messages.html", messages=messages)

    msg_id = request.form.get("msg_id")
    print(msg_id)
    delete_message(msg_id=msg_id)
    return redirect(url_for('msg_queue'))


@app.route("/predict", methods=['POST'])
def predict_route():
    ai_model = get_model()
    json = request.get_json()
    prediction = predict_label(prompt=json["prompt"], classifier=ai_model.model, vectorizer=ai_model.vectorizer)
    store_message_in_queue(message=json["prompt"], prediction=prediction)
    return jsonify({"prediction": prediction})
