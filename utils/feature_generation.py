import pandas as pd
import Levenshtein
import numpy as np
from make_sample import make_sample


def preprocessing_text(s):
    """
    Предобработка текста.
    Пояснение работы:
    - замена некорректного символа
    - удаление знаков препинания 
    - приведени всех символов к нижнему регистру
    - удаление лишних пробелов

    :param s: str - входная строка.
    :return: str - обработанная строка. 
    """
    s = s.replace("&#039;", "'")
    s = s.translate(str.maketrans(
        '', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))
    s = s.lower()
    s = ' '.join(s.split())
    return s


def get_levenshtein_distance_between(first_line, second_line):
    """
    Получает расстояние Левенштейна между двумя строками.

    :param first_line: str - первая строка.
    :param second_line: str - вторая строка.
    :return: int - расстояние левеншейна между этими строками.

    """
    return Levenshtein.distance(first_line, second_line)


def get_brands_and_products_lists(path_to_data):
    """
    Получаем и преобразовываем списки брендов и продуктов из файлов.
    """
    brands = pd.read_csv(path_to_data + "/unique_brands.csv")
    brands = [str(brand) for brand in brands.iloc[:, 0]]

    categories = pd.read_csv(path_to_data + "/unique_products.csv")
    categories = [str(category) for category in categories.iloc[:, 0]]

    return brands, categories


def get_features_for_data(path_to_data):
    """
    Генерирует новые признаки для датафрейма.

    :param data: pd.DataFrame - данные для обучения с колонками [query, category_id, category_name]
    :return data: pd.DataFrame - датафрейм с кучей признаков
    """
    data = make_sample(path_to_data)
    brands, products = get_brands_and_products(path_to_data)

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
        sum([True for product in products if query.find(brand) != -1])
    )
    data['lev_dist_bw_query_category'] = \
        get_levenshtein_distance_between(data['query'], data['category_name'])
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
    # TODO добавить генерацию признаков с дерева категорий (3 штуки)

    data = data.drop(columns=['category_id', 'query', 'category_name'])

    return data
