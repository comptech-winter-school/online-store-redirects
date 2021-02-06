from anytree import Node
from csv import reader
from pickle import dump

def make_category_tree(path_to_data):
    parents = {}
    nodes = {}

    with open(path_to_data + '/categories.csv', newline='') as csvfile:
        rdr = reader(csvfile, delimiter=',')
        for row in rdr:
            if (row[1] == 'id'):
                continue
            if (not row[2]):
                row[2] = 0
            parents[int(row[1])] = int(float(row[2]))

    parents = {k: v for k, v in sorted(parents.items(),
        key = lambda item: item[1])}

    root = Node("root")
    nodes[0] = root

    for key, value in parents.items():
        nodes[key] = Node(key, parent=root)

    for key, value in parents.items():
        nodes[key].parent = nodes[value]

    with open(path_to_data + '/category_tree.obj', 'wb') as category_tree:
        dump(root, category_tree)

from utils.io_custom import read_pickle_object

def get_category_tree(path_to_data):
    """
    :param path: path to file with category tree
    :return: dict(tree_dict) with int keys and values - anytree.Nodes
    (tree_dict[-1] contains root of category tree)
    """
    return read_pickle_object(path_to_data + '/category_tree.obj')

from anytree.search import find

def get_node(id, path_to_data):
    root = get_category_tree(path_to_data)
    return find(root, lambda node: node.name == id)

def get_names(path_to_data):
    categories = {}
    with open(path_to_data + '/categories.csv', "r") as f:
        rdr = reader(f, delimiter=',')
        for row in rdr:
            if row[1] == "id":
                continue
            categories[int(row[1])] = row[5]
    categories["root"] = "root"
    return categories
