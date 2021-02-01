"""
Full Pipeline: A-B-C
Development Pipeline: B-C

A) Making negative examples

B) Offering categories for redirect(Filter)

C) Predict probability for (query, category) (redirects)
"""
from utils.merge_tables import merge_product_external_id_to_categories


class Filter:
    def __init__(self, external_id_to_category):
        """

        :param external_id_to_category: результат работы ф-ии merge_product_external_id_to_categories
        """
        self.external_id_to_category = external_id_to_category

    def filter_multiple(self, ds):
        """
        For list of dicts

        :param ds: list of dicts
        :return: list of dicts(you can get this dict by filter_single)
        Example of "inner dict"
        {
            "query": string,
            "categories": list of int
        }

        ds example:
        [
        {'query': 'гель алое',
         'search_results': ['99730300002', None, '99720100024', '99730300080'],
        'views': [],
        'purchases': []},
        {'query': 'гель алое',
         'search_results': ['99730300002', None, '99720100024', '99730300080'],
        'views': [],
        'purchases': []},
        ]
        """""
        # TODO: refactor
        tmp = []
        for d in ds:
            t = {}
            t['query'] = d['query']
            t['categories'] = self._get_categories(d)
            tmp.append(t)
        return tmp

    def _get_categories(self, d):
        """

        :param d: dict
        :return: список категорий(желательно list, в будущем мб pd.Series)

        d example:
        {'query': 'гель алое',
         'search_results': ['99730300002', None, '99720100024', '99730300080'],
        'views': [],
        'purchases': []}

        """
        pass

    def _get_category_id_for_external_id(self, id):
        """
        Ищет соответствующие категории для каждого id в self.external_id_to_category

        :param id: external_id
        :return: list of category_ids
        """
        pass

    def _get_categories_by_external_ids(self, ids):
        """
        Что делает:
        0) подготовить ids: убрать None, перевести в int
        1) берет external_id из ids
        2) получить категории для каждого отдельного id с помощью _get_category_id_for_external_id
        3) слить списки категорий от каждого отдельного external id в один список(возможно стоит использовать set и использовать .update())
        4) возвращает список категорий

        :param ids: list of strings/None/int(all to int, remove None)
        :return: список категорий(желательно list, в будущем мб pd.Series)
        """
        pass