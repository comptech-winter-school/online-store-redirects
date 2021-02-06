"""
Full Pipeline: A-B-C
Development Pipeline: B-C
A) Making negative examples
B) Offering categories for redirect(Filter)
C) Predict probability for (query, category) (redirects)
"""
import pandas as pd
import re
from json import load
from utils.merge_tables import merge_product_external_id_to_categories
from utils.cousins import get_cousin_id
import random
random.seed(0)


def make_negative_examples_from_searches(json_path, path_to_data):
    """
    Using file "420_searches.json"
    1) Взять для каждого продукта категории и найти дальнюю категорию
    2) Для каждого продукта сохранить продукт + неподходящая категория
    3) Сформировать DataFrame
    :param json_path: list of dicts
    :param external_id_to_category: результат работы ф-ии merge_product_external_id_to_categories
    :param category_tree: anytree.Node(идея использования дерева - брать не прямого предка/потомка, а "брата-сестру"/"кузенов"/"тетю-дядю")
    :return: pd.DataFrame with columns = [query: str, category_id: int]
    Example of dict:
    {'query': '0 70',
    'amount': 1,
    'products': {
    '89072600018': '1',
    '89072600022': '1',
    '89072600015': '42',}}
    """

    with open(json_path) as ff:
        data = load(ff)
    products = pd.read_csv(path_to_data + '/products.csv')
    products_categories = pd.read_csv(path_to_data + '/products_categories.csv')

    def query_function(df):
        query = []
        product_external_id = []
        for i in range(len(df)):
            product_external_id.append(list(df[i]['products'].keys())[0])
            query.append(df[i]['query'])
            i+=1
        data_query = pd.DataFrame({'query': query, 'external_id': product_external_id})
        data_query['external_id'] = pd.to_numeric(data_query['external_id'])
        return data_query

    dd = query_function(data)
    dd = pd.merge(dd, products, on='external_id')
    dd = dd[['query', 'external_id', 'name']]
    list_of_query = []
    count = 0
    for i in range(len(dd)):
        if (re.sub("[^а-яА-Яa-zA-Z0-9]", "", dd.loc[i, 'query'].lower()) ==
            re.sub("[^а-яА-Яa-zA-Z0-9]", "", dd.loc[i, 'name'].lower())):
            list_of_query.append(dd.loc[i, 'query'])
            count += 1
    dd = dd[dd['query'].isin(list_of_query)]
    del dd['name']

    searches = query_function(data[:1500])
    searches = pd.concat([searches, dd])

    searches = pd.merge(searches, merge_product_external_id_to_categories(products, products_categories), on='external_id')
    searches.drop_duplicates(subset=['query'], inplace=True, ignore_index=True)
    searches['category_id_not_redir'] = searches['category_id'].apply(lambda x: get_cousin_id(x))

    return searches


def get_queries_from_sessions(json_path):
    with open(json_path) as ff:
        data = load(ff)
    queries = set()
    for x in data:
        queries.add(x['query'])
    queries = list(queries)
    return queries


def make_positive_examples(path, columns=['query', 'category_id', 'category'],
                           to_columns=['query', 'category_id', 'category_name']):
    df = pd.read_csv(path)
    df = df[columns]
    df.columns = to_columns
    df['is_redirect'] = 1
    return df


def make_negative_examples(queries, positive_categories):
    df = pd.DataFrame()
    df['query'] = queries

    tmp = []
    for _ in range(len(queries)):
        tmp.append(random.choice(positive_categories))
    df['category_id'] = [x[0] for x in tmp]
    df['category_name'] = [x[1] for x in tmp]
    return df


def make_dataset(positive_path, sessions_path, neg_fract=1., neg_size=None):
    positive = make_positive_examples(positive_path)
    queries = get_queries_from_sessions(sessions_path)
    positive_categories = list(set(zip(positive['category_id'].tolist(), positive['category_name'].tolist())))
    negative = make_negative_examples(queries, positive_categories)
    negative = negative.sample(frac=1).reset_index(drop=True)
    negative['is_redirect'] = 0
    if neg_size:
        negative_tmp = negative.iloc[:neg_size]
    else:
        negative_tmp = negative.iloc[:int(neg_fract * len(positive))]
    data = pd.concat([positive, negative_tmp], ignore_index=True)
    data = data.sample(frac=1).reset_index(drop=True)
    return data, positive, negative
