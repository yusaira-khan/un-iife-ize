__author__ = 'yusaira-khan'

import os
import function
import var


# TODO:handle non declarations
# TODO: check if for/var/function are words inside a string
# TODO: surround in class

def handle_file(rpath, wpath=None):
    rfile = open(rpath, "r")
    contents = rfile.read()
    rfile.close()
    stuff = handle_contents(contents)

    if wpath is None:
        wpath = rpath + '__no__iife'
    wfile = open(wpath, "w+")
    wfile.write(stuff)
    wfile.close()


def merge_parts(functions, vars, unmodified):
    all_parts = functions + vars + unmodified
    all_parts.sort(key=lambda tup: tup[1])

    return all_parts


def handle_contents(contents):
    function_extractor = function.Function(contents)
    function_extractor.extract_from_contents()
    print('c',contents)
    all_functions = function_extractor.all
    print('f',all_functions)
    non_functions = function_extractor.unmodified
    print('n',non_functions)
    var_extractor = var.Var(non_functions)
    var_extractor.extract_all()

    all_vars = var_extractor.all
    print('v',all_vars)
    not_modified = var_extractor.unmodified
    print('u',not_modified)
    parts = merge_parts(all_functions, all_vars, not_modified)
    parts = [string for string, index in parts]
    return ''.join(parts)
