import dataset
import logging
import datetime
import dill
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class Model():
    def __init__(self, model: MultinomialNB, date_of_creation: datetime.date, vectorizer: CountVectorizer) -> None:
        self.model = model
        self.date_of_creation = date_of_creation
        self.vectorizer = vectorizer


def store_model(model: Model, filepath: str = 'model.pkl'):
    try:
        with open(file=filepath, mode="wb") as f:
            dill.dump(model, f)
    except IOError as e:
        logging.error(f"IOError: {e.with_traceback}")


def load_model(filepath: str = 'model.pkl') -> Model:
    try:
        with open(file=filepath, mode="rb") as f:
            model = dill.load(f)
        return model
    except IOError as e:
        logging.error(f"IOError: {e.with_traceback}")


def predict_label(prompt: str, classifier: MultinomialNB, vectorizer: CountVectorizer):
    # Preprocess input string using the same steps as training data
    input_vec = vectorizer.transform([prompt])

    # Predict label using trained classifier
    pred = classifier.predict(input_vec)
    return 'spam' if pred[0] == 0 else 'ham'


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
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vec, y_train)
    nb_pred = nb_classifier.predict(X_test_vec)

    # Evaluate Logistic Regression classifier
    nb_accuracy = accuracy_score(y_test, nb_pred)
    nb_f1_score = f1_score(y_test, nb_pred)
    nb_cm = confusion_matrix(y_test, nb_pred)
    logging.info(f"Accuracy: {nb_accuracy}\nF1 Score: {nb_f1_score}\nConfusion Matrix: {nb_cm}")
    return nb_classifier, vectorizer


def re_train_model(filepath: str = "model.pkl"):
    trained, vectorizer = train_model()
    chosen_model = Model(model=trained, date_of_creation=datetime.date.today(), vectorizer=vectorizer)
    store_model(model=chosen_model, filepath=filepath)
