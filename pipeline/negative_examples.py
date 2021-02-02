"""
Full Pipeline: A-B-C
Development Pipeline: B-C

A) Making negative examples

B) Offering categories for redirect(Filter)

C) Predict probability for (query, category) (redirects)
"""
from utils.category_tree import get_category_tree
from utils.merge_tables import merge_product_external_id_to_categories
from utils.cousins import cousin

# (A)
def make_negative_examples_from_searches(json_data, external_id_to_category, category_tree):
    """
    Using file "420_searches.json"

    1) Взять для каждого продукта категории и найти дальнюю категорию
    2) Для каждого продукта сохранить продукт + неподходящая категория
    3) Сформировать DataFrame

    :param json_data: list of dicts
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


    pass
