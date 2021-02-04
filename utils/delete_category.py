import pandas as pd

def delete_orphan_categories_from_csv(dataFrame):
    return dataFrame.query('(parent_id.isnull()) or (parent_id in id)')

def delete_category(id_to_delete):
    categories = pd.read_csv('../resourses/category_tree/categories.csv')
    categories = categories.query('id != {0}'.format(id_to_delete))
    categories = delete_orphan_categories_from_csv(categories)
    categories.to_csv('../resourses/category_tree/categories.csv', index=False)
