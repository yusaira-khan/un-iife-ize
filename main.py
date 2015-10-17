__author__ = 'yusaira-khan'

import os
import re
import string


# TODO: handle anonymous functions
# TODO:handle non declarations
# TODO: check if for/var/function are words inside a string


def get_file_contents(path):
    file = open(path, "r")
    contents = file.read()
    file.close()
    return contents  # , (len(contents))


def detect_func_declaration(contents, start=0):
    func_det_pat = re.compile(r"function\s+([\w$]+)(\(.*\))\s*\{")
    match = func_det_pat.search(contents, start)
    if match is None:
        return None
    l_brance_after = match.end()
    r_brace_index = get_matched_braces_end(contents, l_brance_after)

    if is_inside_function(contents, match.start(), r_brace_index):
        return None
    return match, r_brace_index


def get_fun_info(contents, match, rbrace):
    ret = {
        'name': match.group(1),
        'args': match.group(2),
        'statement_start': match.start(),
        'lbrace_index': match.end() - 1,
        'rbrace_index': rbrace,

    }
    ret['body'] = contents[ret['lbrace_index']:ret['rbrace_index'] + 1]
    return ret


def correct_func(info):
    dec = [
        info['name'],
        '=function',
        info['args'],
        info['body'],
        ';']
    print(dec)
    return ''.join(dec)


def fun_all(contents, start=0):
    match, rb = detect_func_declaration(contents, start)
    info = get_fun_info(contents, match, rb)
    ret = correct_func(info)
    return ret


def handle_func(contents, start=0):
    match, end_fun = detect_func_declaration(contents)
    # fun_start = match.start()
    # fun_name =


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

    # TODO: check for blocks inside function
    fun_index = contents.rfind('function', 0, start)
    if fun_index == -1:
        return False
    fun_start = contents.find('{', fun_index)
    fun_end = get_matched_braces_end(contents, fun_start + 1)
    # for loop ends before var declaration
    if fun_end < start:
        return False
    return True


def is_inside_for_loop(contents, start, end):
    len_for_loop = 4
    if start < 4:
        return False
    for_index = contents.rfind('for', 0, start)
    for_end = contents.find(')', for_index)

    # no for loop exists before var declaration
    if for_index == -1:
        return False
    # for loop ends before var declaration
    if for_end < start:
        return False

    return True


def handle_file(contents):
    parts = []
    parts[0] = "var declarations"
    parts[1] = "function declartions"
    parts[2] = "parts inside functions"
    parts[3] = "parts that don't need modification"

    return ''.join(parts)


#####
# THIS IS ANNOYING
#####

def get_matched_braces_end(content, start, start_tok=None, end_tok=None):
    """
    content: entire file
    start: index of { + 1
    """
    # FIXME: contains infinite loop
    tries = 5
    count = 1
    r_b_index = -1
    while count != 0 and tries != 0:
        tries -= 1
        r_b_index = content.find('}', start)

        l_b_count = content.count('{', start, r_b_index)
        count += l_b_count - 1
        start = r_b_index +1
    return r_b_index
