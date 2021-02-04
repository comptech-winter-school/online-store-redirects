import pandas as pd

def preprocessing_true_redirects(true_redirs):
    """
    Удаляет неиспользуемые колоноки в датафрейме с подлинными редиректами.
    Переименовывает оставшиеся колонки.

    :param true_redirs: pd.DataFrame - датафрейм подлинных редиректов на правильную категорию.
    :returntrue_redirects: pd.DataFrame - обработанный pd.DataFrame.
    """
    true_redirs = true_redirs.drop(columns=['redir_id', 'rule_id', 'start_date', 'parent_id'])
    true_redirs['is_redirect'] = 1
    true_redirs.rename(columns={'category': 'category_name'}, inplace=True)
    return true_redirs


def preprocessing_false_redirects(false_redirs, categories):
    """
    Удаляет неиспользуемые колоноки в датафрейме с ложными редиректами.
    Добавляет необходимую колонку с именем категории.
    Переименовывает оставшиеся колонки.

    :param false_redirs: pd.DataFrame - сгенерированный датафрейм редиректов не на ту категорию.
    :return: обработанный pd.DataFrame 
    """
    false_redirs['category_name'] = false_redirs['category_id_not_redir'].apply(lambda i: categories.query('id == @i')['name'].values[0])

    false_redirs = false_redirs.drop(columns=['external_id', 'product_id', 'category_id'])
    false_redirs.rename(columns={'category_id_not_redir': 'category_id'}, inplace=True)
    false_redirs['is_redirect'] = 0
    return false_redirs


def make_sample(path_to_data):
    """
    Создаёт итоговую выборку из подлинных редиректов на нужную категорию
    и редиректов не на ту категорию. (из файлов 420_redirects.csv, negative_examples.csv)

    :param path_to_data: str - путь к папке, в которой содержатся файлы (example "./data/redir")
    :return sample: pd.DataFrame - итоговая таблица для обучения и тестирования модели
    Состоит из столбцов [query, category_id, category_name, is_redirect]
    """
    true_redirs = pd.read_csv(path_to_data + '/420_redirects.csv', index_col=0)
    false_redirs = pd.read_csv(path_to_data + '/negative_examples.csv')
    categories = pd.read_csv(path_to_data + '/categories.csv', index_col=0)

    true_redirs = preprocessing_true_redirects(true_redirs)
    false_redirs = preprocessing_false_redirects(false_redirs, categories)

    sample = pd.concat([true_redirs, false_redirs], ignore_index=True)

    return sample
