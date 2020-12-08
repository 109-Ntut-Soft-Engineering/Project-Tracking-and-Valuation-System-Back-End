from itertools import tee

def is_iter_empty(src_iter):
    it1, it2 = tee(src_iter)
    if next(it1, None) is None:
        return True, it2
    else:
        return False, it2

# def parse_project_name(name):
#     return name.replace('%20', ' ')