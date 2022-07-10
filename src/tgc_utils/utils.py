""" Utilities generic to most Python code
"""
import os


def list_files_at_path(path):
    """List files at a path
    :param path: a file path
    :return: list of files with absolute path names
    """
    abs_path = os.path.abspath(path)
    return [entry.path for entry in os.scandir(abs_path) if entry.is_file()]
