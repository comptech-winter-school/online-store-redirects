import Levenshtein
from joblib import dump, load
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score
from sklearn.model_selection import cross_validate, RepeatedStratifiedKFold

SCORING = ['accuracy', 'roc_auc', 'f1', 'precision', 'recall']
STRONG_CV = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=2)


class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, col):
        self.col = col

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None, **fit_params):
        return X[self.col]


class ExampleLevenshtein(BaseEstimator, TransformerMixin):
    def __init__(self, col1, col2):
        self.col1 = col1
        self.col2 = col2

    def fit(self, X, y=None, **fit_params):
        return self

    def distance(self, a, b):
        a = a.strip()
        b = b.strip()
        return Levenshtein.distance(a, b) / len(a) / len(b)

    def transform(self, X, y=None, **fit_params):
        X['lev'] = X.apply(lambda x: self.distance(x[self.col1], x[self.col2]), axis=1)
        return X[['lev']]



def make_tfidf_baseline(n_jobs=1):
    query = Pipeline([
        ('query', ColumnSelector(col='query')),
        ('tfidf', TfidfVectorizer(ngram_range=(2, 3), analyzer='char_wb', max_features=1000))
    ])
    category_name = Pipeline([
        ('category_name', ColumnSelector(col='category_name')),
        ('tfidf', TfidfVectorizer(ngram_range=(2, 3), analyzer='char_wb', max_features=1000))
    ])

    features = FeatureUnion([('query_feats', query), ('category_name', category_name)])

    pipeline = Pipeline([
        ('features', features),
        ('clf', LogisticRegression(n_jobs=n_jobs, random_state=1, class_weight='balanced'))
    ])
    return pipeline


def fit_pipeline(pipeline, X, y):
    return pipeline.fit(X, y)


def cross_validate_pipeline(pipeline, X, y, cv=STRONG_CV, scoring=SCORING, n_jobs=1, verbose=0):
    result = cross_validate(
        pipeline,
        X,
        y,
        scoring=scoring,
        cv=cv,
        n_jobs=n_jobs,
        verbose=verbose
    )
    return result


def save_pipeline(pipeline, path):
    dump(pipeline, path)


def load_pipeline(path):
    return load(path)


def predict_proba_pipeline(pipeline, X):
    return pipeline.predict_proba(X)[:, 1]


def score_pipeline(pipeline, X, y, score=roc_auc_score):
    y_pred = predict_proba_pipeline(pipeline, X)
    return score(y, y_pred)
