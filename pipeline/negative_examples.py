"""
Full Pipeline: A-B-C
Development Pipeline: B-C
A) Making negative examples
B) Offering categories for redirect(Filter)
C) Predict probability for (query, category) (redirects)
"""
import sys
sys.path.append('utils')

import pandas as pd
import re
from json import load
from merge_tables import merge_product_external_id_to_categories
from cousins import get_cousin_id

def make_negative_examples_from_searches(json_path):
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
    products = pd.read_csv('resourses/products.csv')
    products_categories = pd.read_csv('resourses/products_categories.csv')

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
