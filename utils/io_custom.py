from pickle import load, dump


def read_pickle_object(path):
    t = None
    with open(path, 'rb') as f:
        t = load(f)
    return t


def dump_pickle_object(path_with_name, obj):
    with open(path_with_name, 'wb') as f:
        dump(obj, f)
