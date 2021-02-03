from anytree import Node
from csv import reader
from pickle import dump

def make_category_tree():
    parents = {}
    nodes = {}

    with open('resourses/category_tree/categories.csv', newline='') as csvfile:
        rdr = reader(csvfile, delimiter=',')
        for row in rdr:
            if (not row[2]):
                row[2] = 0
            parents[int(row[1])] = int(row[2])

    parents = {k: v for k, v in sorted(parents.items(),
        key = lambda item: item[1])}

    root = Node("root")
    nodes[0] = root

    for key, value in parents.items():
        nodes[key] = Node(key, parent=root)

    for key, value in parents.items():
        nodes[key].parent = nodes[value]

    with open('resourses/category_tree/category_tree.obj', 'wb') as category_tree:
        dump(root, category_tree)

from io_custom import read_pickle_object

def get_category_tree():
    """
    :param path: path to file with category tree
    :return: dict(tree_dict) with int keys and values - anytree.Nodes
    (tree_dict[-1] contains root of category tree)
    """
    return read_pickle_object('resourses/category_tree/category_tree.obj')
