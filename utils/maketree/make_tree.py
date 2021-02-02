from anytree import Node
from csv import reader
from pickle import dump

def create_category_tree():
    parents = {}
    nodes = {}

    with open('utils/maketree/categories.csv', newline='') as csvfile:
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

    with open('utils/maketree/category_tree.obj', 'wb') as category_tree:
        dump(root, category_tree)

create_category_tree()
