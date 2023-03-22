import dataset
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

df = dataset.get_general_dataset()

X = df['message']
y = df['is_spam']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Naive Bayes classifier
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train_vec, y_train)
nb_pred = nb_classifier.predict(X_test_vec)

# Evaluate Naive Bayes classifier
nb_accuracy = accuracy_score(y_test, nb_pred)
nb_f1_score = f1_score(y_test, nb_pred)
nb_cm = confusion_matrix(y_test, nb_pred)

print('Naive Bayes Accuracy:', nb_accuracy)
print('Naive Bayes F1 Score:', nb_f1_score)
print('Naive Bayes Confusion Matrix:', nb_cm)

# Train Logistic Regression classifier
lr_classifier = LogisticRegression(max_iter=10000)
lr_classifier.fit(X_train_vec, y_train)
lr_pred = lr_classifier.predict(X_test_vec)

# Evaluate Logistic Regression classifier
lr_accuracy = accuracy_score(y_test, lr_pred)
lr_f1_score = f1_score(y_test, lr_pred)
lr_cm = confusion_matrix(y_test, lr_pred)

print('Logistic Regression Accuracy:', lr_accuracy)
print('Logistic Regression F1 Score:', lr_f1_score)
print('Logistic Regression Confusion Matrix:', lr_cm)
