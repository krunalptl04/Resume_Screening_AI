import pandas as pd

from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB

def train_model():

    data = pd.read_csv("dataset.csv")

    X = data["resume_text"]

    y = data["label"]

    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])

    model.fit(X, y)

    return model