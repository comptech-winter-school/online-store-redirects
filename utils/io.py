import pickle
import anytree


def read_pickle_object(path):
    t = None
    with open(path, 'rb') as f:
        t = pickle.load(f)
    return t
