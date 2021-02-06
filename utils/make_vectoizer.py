from pickle import dump
from sklearn.feature_extraction.text import TfidfVectorizer


def make_vectorizer(train_data, ngram_range, max_features):
    """
    Создать и обучить vectorizer на обучающих данных.

    :param train_data: pd.DataFrame - обучающие данные ['query', 'category_name', 'cayegory_id']
    :ngram_range: tuple(int, int) - ngram_range.
    :max_features: int - количество используемый ngram_range грам. 
    :return vectorizer: sklearn.feature_extraction.text.TfidfVectorizer - обученный символьный vectorizer.
    """
    all_text = (train_data['query'] + " " + train_data['category_name']).values
    vectorizer = TfidfVectorizer(ngram_range=ngram_range,
                                 max_features=max_features,
                                 analyzer='char_wb')
    vectorizer.fit(all_text)

    return vectorizer
