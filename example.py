import pandas as pd
from pipeline.predictor import Predictor
from pipeline.training import load_pipeline


categories = pd.read_csv("./data/redir/categories.csv")
pipe = load_pipeline("./models/tfidf_baseline1")
p = Predictor(pipe, categories)
d = [{
    "query": "dior хайлайтер",
    "categories_ids": [3327621, 3327622, 3327619, 3327959, 3328775, 3329045]
}]

result = p.predict(d)
print(result)
# [{'query': 'dior хайлайтер',
# 'category_id': 3327622,
# 'category_name': 'Туши для ресниц',
# 'categories_preds':
# [0.9438322449500943, 0.9859640181629619, 0.9648794970354365, 0.8428305945512996, 0.8514966224563965, 0.8847087510204606]}]