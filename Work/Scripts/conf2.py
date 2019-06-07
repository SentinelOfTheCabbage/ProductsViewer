import os


def parent_dir(path):
    return os.path.dirname(path)


ROOT_DIR = parent_dir(parent_dir(__file__))
