"""
Full Pipeline: A-B-C
Development Pipeline: B-C

A) Making negative examples

B) Offering categories for redirect(Filter)

C) Predict probability for (query, category) (redirects)
"""

class Preprocessor:
    pass

class Predictor:
    def __init__(self, model):
        """

        :param model: sklearn-like model
        """
        self.model = model

    def preprocess(self):
        # TODO
        pass

    def predict_for_one_category(self, atom):
        """

        :param atom: [query: str, category_id: int]
        :return: float score
        """

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
        """
        # TODO: get probabilities/scores from self.model and then postprocess it
        # pred = self.model.predict_proba()
