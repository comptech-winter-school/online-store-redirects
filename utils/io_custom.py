from pickle import load

def read_pickle_object(path):
    t = None
    with open(path, 'rb') as f:
        t = load(f)
    return t
