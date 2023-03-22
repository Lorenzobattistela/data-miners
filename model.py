import dataset
import logging
import datetime
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class Model():
    def __init__(self, model, date_of_creation) -> None:
        self.model = model
        self.date_of_creation = date_of_creation

def store_model(model: Model, filepath: str = 'model.pkl'):
    try:
        with open(file=filepath, mode="wb") as f:
            pickle.dump(model, f)
    except IOError as e:
        logging.error(f"IOError: {e.with_traceback}")

def load_model(filepath: str = 'model.pickle') -> Model:
    try:
        with open(file=filepath, mode="rb") as f:
            model = pickle.load(f)
        return model
    except IOError as e:
        logging.error(f"IOError: {e.with_traceback}")

def train_model():
    df = dataset.get_general_dataset()
    df = df.sample(frac=1, random_state=1).reset_index(drop=True)

    X = df['message']
    y = df['is_spam']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train Logistic Regression classifier
    lr_classifier = LogisticRegression(max_iter=10000)
    lr_classifier.fit(X_train_vec, y_train)
    lr_pred = lr_classifier.predict(X_test_vec)

    # Evaluate Logistic Regression classifier
    lr_accuracy = accuracy_score(y_test, lr_pred)
    lr_f1_score = f1_score(y_test, lr_pred)
    lr_cm = confusion_matrix(y_test, lr_pred)
    logging.info(f"Accuracy: {lr_accuracy}\nF1 Score: {lr_f1_score}\nConfusion Matrix: {lr_cm}")
    return lr_classifier

def re_train_model():
    trained = train_model()
    chosen_model = Model(model=trained, date_of_creation=datetime.date.today())
    store_model(model=chosen_model)
