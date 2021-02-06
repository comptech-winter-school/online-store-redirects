import pandas as pd
import Levenshtein
import numpy as np
from anytree.search import find
from utils.io_custom import read_pickle_object
from scipy.spatial.distance import cosine
import re


def get_relative_depth(id, tree):
    pass


def count_children(id, tree):
    pass


def count_descendants(id, tree):
    pass


def preprocessing_text(s):
    """
    Предобработка текста.

    :param s: str - входная строка.
    :return: str - обработанная строка.
    """
    return str(" ".join(re.findall("[a-zA-Zа-яА-Я0-9]+", s)).lower())


def get_levenshtein_distance_between(first_line, second_line):
    """
    Получает расстояние Левенштейна между двумя строками.

    :param first_line: str - первая строка.
    :param second_line: str - вторая строка.
    :return: int - расстояние левеншейна между этими строками.

    """
    return Levenshtein.distance(first_line, second_line)


def get_lev_dist_between_query_category(query, category):
    """
    Получает расстояние Левенштейна между двумя сериями.

    :param query: pd.Series - запрос.
    :param second_line: pd.Series - категория.
    :return: np.array, int - расстояние левеншейна между соответствующими элементами серий.
    """
    levenshtein_distances = []

    for query, category in zip(query.values, category.values):
        current_distance = get_levenshtein_distance_between(query, category)
        levenshtein_distances.append(current_distance)

    return np.array(levenshtein_distances)


def get_brands_and_products_lists(path_to_data):
    """
    Получаем и преобразовываем списки брендов и продуктов из файлов.
    """
    brands = pd.read_csv(path_to_data + "/unique_brands.csv")
    brands = [str(brand) for brand in brands.iloc[:, 0]]

    products = pd.read_csv(path_to_data + "/unique_products.csv")
    products = [str(product) for product in products.iloc[:, 0]]

    return brands, products


def create_data_with_features(path_to_data):
    """
    Загружает данные для обучения и генерирует для них.

    :param path_to_data: str - относительный путь к данным для обучения.
    :return data: pd.DataFrame - датафрейм с кучей признаков
    Оставлено для обратной совместимости с двумя блокнотами.
    """
    data = pd.read_csv(path_to_data + "/data_for_model.csv")
    return get_data_with_feature(data, path_to_data)


def get_cosine_dist_between_query_category(query, category, vectorizer):
    """
    Получает косинусное расстояние между двумя колонками датафрейма.

    :param query: pd.Series - запрос.
    :param second_line: pd.Series - категория.
    :param vectorizer: sklearn.feature_extraction.text.TfidfVectorizer - предобученный векторайзер на запросах и категориях из трейн выборки.
    :return: np.array, int - косинусное расстояние между соответствующими элементами серий.
    """
    query_sparse_matrix = vectorizer.transform(query.values)
    category_sparse_matrix = vectorizer.transform(category.values)

    distances = []
    for query_vec, category_vec in zip(query_sparse_matrix, category_sparse_matrix):
        current_distance = cosine(query_vec.toarray(), category_vec.toarray())
        distances.append(current_distance)

    return np.array(distances)


def get_data_with_feature(data, path_to_data):
    """
    Генерирует признаки для обучающих и валидационных данных.

    :param data: pd.DataFrame - обучающие или валидационные данные с колонками [query, category_id, category_name, is_redirect]
    :param path_to_data: str - относительный путь к данным о брендах и продуктах.
    :return data: pd.DataFrame - датафрейм с кучей признаков
    """
    brands, products = get_brands_and_products_lists(path_to_data)

    data['query'] = data['query'].apply(preprocessing_text)
    data['category_name'] = data['category_name'].apply(preprocessing_text)

    data['len_of_query'] = data['query'].apply(lambda query: len(query))
    data['num_of_word_in_query'] = data['query'].apply(
        lambda query:
        len(query.split(' '))
    )
    data['category_name'] = data['category_name'].apply(preprocessing_text)
    data['len_of_category'] = data['category_name'].apply(
        lambda category:
        len(category)
    )
    data['num_of_word_in_category'] = data['category_name'].apply(
        lambda category:
        len(category.split(' '))
    )
    data['how_match_brands_name_in_query'] = data['query'].apply(
        lambda query:
        sum([True for brand in brands if query.find(brand) != -1])
    )
    data['how_match_products_name_in_query'] = data['query'].apply(
        lambda query:
        sum([True for product in products if query.find(product) != -1])
    )
    data['mean_word_len_in_category'] = data['category_name'].apply(
        lambda category_name:
        np.mean([len(word) for word in category_name.split(' ')])
    )
    data['mean_word_len_in_query'] = data['query'].apply(
        lambda query:
        np.mean([len(word) for word in query.split(' ')])
    )
    data['max_word_len_in_category'] = data['category_name'].apply(
        lambda category_name:
        np.max([len(word) for word in category_name.split(' ')])
    )
    data['max_word_len_in_query'] = data['query'].apply(
        lambda query:
        np.max([len(word) for word in query.split(' ')])
    )
    data['min_word_len_in_category'] = data['category_name'].apply(
        lambda category_name:
        np.min([len(word) for word in category_name.split(' ')])
    )
    data['min_word_len_in_query'] = data['query'].apply(
        lambda query:
        np.min([len(word) for word in query.split(' ')])
    )
    data['is_query_long'] = data['len_of_query'].apply(lambda l: int(l > 50))

    # TODO добавить генерацию признаков с дерева категорий (3 штуки)

    data['lev_dist'] = get_lev_dist_between_query_category(data['query'],
                                                           data['category_name'])

    vectorizer = read_pickle_object(path_to_data + '/vectorizer.obj')
    data['cosine_dist'] = get_cosine_dist_between_query_category(data['query'],
                                                                 data['category_name'],
                                                                 vectorizer)

    # data['number_of_children_category'] = get_relative_depth(data['category_id'])
    # data['number_of_descendants_category'] = count_descendants(data['category_id'])
    # data['category_depth'] = get_relative_depth(data['category_id'])

    data = data.drop(columns=['category_id', 'query', 'category_name'])

    return data
