"""
Full Pipeline: A-B-C
Development Pipeline: B-C

A) Making negative examples

B) Offering categories for redirect(Filter)

C) Predict probability for (query, category) (redirects)
"""
import pandas as pd


class Preprocessor:
    pass


class Predictor:
    def __init__(self, model, categories):
        """

        :param model: sklearn-like model
        """
        self.model = model
        self.categories = categories

    def preprocess(self):
        # TODO
        pass

    def prepare_data(self, data):
        cats = pd.DataFrame()
        cats['id'] = data['categories_ids']

        df = pd.DataFrame()
        df['category_id'] = cats['id']
        df['category_name'] = cats.merge(self.categories)['name']
        df['query'] = [data['query']] * len(df)
        return df


    def predict_for_one_category(self, atom):
        """

        :param atom: [query: str, category_id: int]
        :return: float score
        """
        pass

    def predict_scores(self, data):
        """
        Метод для получения скоров для каждой категории
        (т.е. список скоров соответствует списку категорий)


        :param data: list/pd.DataFrame of query + category_id
        :return: list of float
        """
        pass

    def predict(self, data):
        """

        :param data:
        :return:

        Example of data:
        [{"query": "айфон X", "categories_ids": [1, 42, 142]}]

        Пример возвращаемого значения:
        [{"query": "айфон X", "category_id": 42, "category_name": "Техника Apple", "categories_preds": [0.99]}]
        """
        result = []
        for d in data:
            tmp = self.prepare_data(d)
            pred_old = self.model.predict_proba(tmp)[:, 1]
            pred = tmp.iloc[pred_old.argmax()]
            res = {
                'query': d['query'],
                'category_id': pred['category_id'],
                'category_name': pred['category_name'],
                'categories_preds': list(pred_old)
            }
            result.append(res)
        return result
