"""
Full Pipeline: A-B-C
Development Pipeline: B-C

A) Making negative examples

B) Offering categories for redirect(Filter)

C) Predict probability for (query, category) (redirects)
"""
from utils.merge_tables import merge_product_external_id_to_categories
import pandas as pd
import numpy as np


class Filter:
    def __init__(self, external_id_to_category):
        """
        Конструктор класса.

        :param external_id_to_category: pd.DataFrame -  результат работы функции merge_product_external_id_to_categories.
        """

        self.external_id_to_category = external_id_to_category

    def filter_multiple(self, sessions):
        """
        Фильтр для списка всех словарей (сессий из json файла [и нового, и старого])

        :param sessions: list of dicts from json files.
        :return: list of dicts - с определенной внутренней структурой.

        Пример структуры одного из словарей, содержащихся в возвращаемом списке:
        {
            "query": string,
            "categories": list of int
        }

        Пример списка словарей sessions:
        [{
            'query': 'гель алое',
            'search_results': ['99730300002', None, '99720100024', '99730300080'],
            'views': [],
            'purchases': []
        },
        {
            'query': 'гель алое',
            'search_results': ['99730300002', None, '99720100024', '99730300080'],
            'views': [],
            'purchases': []
        }]
        """

        queries_with_categories = []

        for session in sessions:
            current_pair_query_categories = {
                'query': self._get_query_text_from_session(session),
                'categories_ids': self._get_categories_for_session(session)
            }
            queries_with_categories.append(current_pair_query_categories)

        return queries_with_categories

    def _get_query_text_from_session(self, session):
        """
        Извлекает тест запроса из сессии.

        :param session: dict - сессия из json файла.
        :return: str - текст запроса.
        """

        return session['query']

    def _get_categories_for_session(self, session):
        """
        Получает список уникальных идентификаторов категорий для конкретной сессии.

        :param session: dict - сессия из json файла.
        :return: list of int - список уникальных категорий. (в будущем мб pd.Series)

        Пример входного словаря session:
        {
            'query': 'гель алое',
            'search_results': ['99730300002', None, '99720100024', '99730300080'],
            'views': [],
            'purchases': []
        }

        """

        return self._get_categories_by_external_ids(session['search_results'])

    def _get_categories_by_external_ids(self, external_ids):
        """
        Получает список уникальных идентификаторов категорий для конкретного списка внешних идентификаторов продуктов.

        :param external_ids: list of strings/int (may contain None) - список внешних идентификаторов продуктов из сессии.
        :return: list of int - список уникальных идентификаторов категорий. (будущем мб pd.Series)
        """

        unique_category_ids = set()

        for external_id in external_ids:
            if external_id is not None:
                list_of_category_ids_for_external_id = self._get_category_ids_for_external_id(
                    int(external_id))
                if len(list_of_category_ids_for_external_id) > 0:
                    unique_category_ids.update(
                        list_of_category_ids_for_external_id)

        return list(unique_category_ids)

    def _get_category_ids_for_external_id(self, external_id):
        """
        Ищет соответствующие идентификаторы категорий для конкретного внешнего идентификатора продукта в self.external_id_to_category.
        Чаще всего таких идентификаторов категорий несколько.

        :param external_id: int - внешний идентификатор продукта.
        :return: list of int - список идентификаторов категорий.
        """

        return list(self.external_id_to_category.query('external_id == @external_id')['category_id'].values)
