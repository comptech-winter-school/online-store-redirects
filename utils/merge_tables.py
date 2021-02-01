import pandas as pd


def merge_product_external_id_to_categories(products, products_categories):
    """
    Using products.csv and products_categories.csv
    Что делает:
    мержит продукты с категориями продуктов по product_id(в products обычный id)

    :param products: pd.DataFrame
    :param products_categories: pd.DataFrame

    :return pd.DataFrame with columns [external_id: int, product_id: int, category_id: int]
    """
    pass