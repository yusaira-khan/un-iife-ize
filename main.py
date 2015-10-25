__author__ = 'yusaira-khan'

import os
import function
import var
import argparse


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
    function_extractor.extract_all()
    all_functions = function_extractor.all
    non_functions = function_extractor.unmodified
    var_extractor = var.Var(non_functions)
    var_extractor.extract_all()

    all_vars = var_extractor.all
    not_modified = var_extractor.unmodified
    parts = merge_parts(all_functions, all_vars, not_modified)
    parts = [string for string, index in parts]
    return ''.join(parts)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('read_path')
    p.add_argument('write_path')
    args = p.parse_args()
    handle_file(args.read_path, args.write_path)
