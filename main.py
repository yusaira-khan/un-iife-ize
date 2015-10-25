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

def detect_var_statement(contents, start=0):
    # find var
    var_index = contents.find('var ', start)
    end_var = contents.find(';', var_index)
    if is_inside_function(contents, var_index, end_var):
        return None
    return correct_var(contents, var_index, end_var)


def correct_var(contents, var_index, end_var):
    statement = contents[var_index:end_var]
    # removing var
    decs = statement[3:].split(',')
    for i in range(len(decs)):
        d = decs[i]

        if '=' in d:
            decs[i] = d.strip()
            continue
        # do nothing
        decs[i] = d.strip() + '=undefined'
    ret = ','.join(decs)
    ret += ';'
    return ret


def is_inside_function(contents, start, end):
    len_function_declaration = 11
    if start < len_function_declaration:
        return False

    # TODO: use function detection  function from above
    fun_index = contents.rfind('function', 0, start)
    if fun_index == -1:
        return False
    fun_start = contents.find('{', fun_index)
    fun_end = get_matched_braces_end(contents, fun_start + 1)
    # for loop ends before
    # var declaration
    if fun_end < start:
        print("no function")
        return False
    print("it's inside a function", fun_index, fun_end)
    return True



def handle_file(contents):
    parts = []
    parts[0] = "var declarations"
    parts[1] = "function declartions"
    parts[2] = "parts inside functions"
    parts[3] = "parts that don't need modification"

    return ''.join(parts)
