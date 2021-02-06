import pandas as pd
from re import sub, findall
from csv import reader
from utils.category_tree import get_names

def delete_orphan_categories(dataFrame):
    return dataFrame.query('(parent_id.isnull()) or (parent_id in id)')

def delete_category_from_csv(id_to_delete):
    categories = pd.read_csv('resourses/category_tree/categories.csv')
    categories = categories.query('id != {0}'.format(id_to_delete))
    categories = delete_orphan_categories(categories)
    categories.to_csv('resourses/category_tree/categories.csv', index=False)

def normalize_string(string):
    return sub("[^а-яА-Яa-zA-Z0-9]", "", string).lower()

def find_CEO_categories():
    res = []
    categories = get_names()
    filter = r"распрод|акци|магаз|подар|клиент|новин|бестс|sale|предложени|эксклюз|рекоменд|пятница|понедельник"
    for key, value in categories.items():
        if findall(filter, normalize_string(value)):
            print(key, value)
            res.append(key)
    return res

def delete_CEO_categories():
    delete_category_from_csv(3480013)
    ids = find_CEO_categories()
    for id in ids:
        delete_category_from_csv(id)
