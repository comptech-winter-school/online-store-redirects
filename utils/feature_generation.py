import pandas as pd
import Levenshtein
import numpy as np


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
    s = str(' '.join(s.split()))
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
    # TODO добавить расстояние левенштейна
    # TODO добавить косинусное расстояние через обученный посимвольный векторайзер
    data = data.drop(columns=['category_id', 'query', 'category_name'])

    return data
