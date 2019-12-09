import os

def current_path(name):
    return os.path.abspath(name)

def parent_path(name):
    parent = os.path.abspath(os.path.dirname(current_path(name)) + os.path.sep + ".")
    return parent

def grandparent_path(path):
    return parent_path(parent_path(path))

def file_name(path):
    return path.split('\\')[-1]

if __name__=='__main__':
    c=current_path(__file__)
    print(c)
    print(file_name(c))
    print(parent_path(c))
    print(file_name(parent_path(c)))
    print(grandparent_path(c))
    print(file_name(grandparent_path(c)))