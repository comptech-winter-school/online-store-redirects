from utils.io import read_pickle_object
from anytree import Node


def get_category_tree(path):
    """
    :param path: path to file with category tree
    :return: dict(tree_dict) with int keys and values - anytree.Nodes
    (tree_dict[-1] contains root of category tree)
    """
    return read_pickle_object(path)
