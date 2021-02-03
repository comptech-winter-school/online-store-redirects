from random import randint

def get_cousin(node):
    cousins = get_cousins(node)
    n = len(cousins)
    return cousins[randint(0, n - 1)]

def get_cousins(node):
    ancestor = node.parent
    node_branch = node
    while len(ancestor.children) < 2:
        node_branch = ancestor
        ancestor = ancestor.parent
    cousins = list(ancestor.children)
    cousins.remove(node_branch)
    return cousins
