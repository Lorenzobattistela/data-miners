from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import model
import os
import datetime
import pytest

FILENAME = "test.pkl"

def test_model_training():
    classifier, vectorizer = model.train_model()
    assert type(classifier) == MultinomialNB, "Should return multinomial naive bayes"
    assert type(vectorizer) == CountVectorizer, "Should return a count vectorizer"

def test_label_prediction():
    possible_labels = ["spam", "ham"]
    classifier, vectorizer = model.train_model()
    predicted_label = model.predict_label("This is a test.", classifier, vectorizer)
    assert predicted_label in possible_labels, "Should return a string with a possible label"

def test_model_storage():
    trained, vectorizer = model.train_model()
    chosen_model = model.Model(trained, datetime.date.today(), vectorizer)
    model.store_model(chosen_model, FILENAME)
    assert os.path.isfile("test.pkl"), "Should have written a pkl file."
    loaded = model.load_model(FILENAME)
    assert loaded.date_of_creation == datetime.date.today(), "Should have loaded the correct date"
    os.remove(FILENAME)

def test_model_retraining():
    model.re_train_model(FILENAME)
    assert os.path.isfile("test.pkl"), "Should have written a pkl file."
    os.remove(FILENAME)

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def remove_files():
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
    request.addfinalizer(remove_files)