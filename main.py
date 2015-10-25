__author__ = 'yusaira-khan'

import os
import re


# TODO:handle non declarations
# TODO: check if for/var/function are words inside a string
# TODO: surround in class

def get_file_contents(path):
    file = open(path, "r")
    contents = file.read()
    file.close()
    return contents  # , (len(contents))


def handle_file(contents):
    parts = []
    parts[0] = "var declarations"
    parts[1] = "function declartions"
    parts[2] = "parts inside functions"
    parts[3] = "parts that don't need modification"

    return ''.join(parts)
