from random import randint
from pickle import load
from anytree.search import find
from utils.category_tree import get_category_tree

def get_cousins(node):
    ancestor = node.parent
    node_branch = node
    while len(ancestor.children) < 2:
        node_branch = ancestor
        ancestor = ancestor.parent
    cousins = list(ancestor.children)
    cousins.remove(node_branch)
    return cousins

def get_cousin(node):
    cousins = get_cousins(node)
    n = len(cousins)
    return cousins[randint(0, n - 1)]

def get_cousin_id(id):
    root = get_category_tree()
    node = find(root, lambda node: node.name == id)
    return int(get_cousin(node).name)
