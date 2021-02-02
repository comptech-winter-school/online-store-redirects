from random import randint

def cousin(node):
    ancestor = node.parent
    while len(ancestor.children) < 2:
        ancestor = ancestor.parent
    n = len(ancestor.children)
    while True:
        child = ancestor.children[randint(0, n - 1)]
        if child != node:
            break
    return child

def cousins(node):
    ancestor = node.parent
    while len(ancestor.children) < 2:
        ancestor = ancestor.parent
    cousins = list(ancestor.children)
    if (node in cousins):
        cousins.remove(node)
    return cousins
