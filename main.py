__author__ = 'yusaira-khan'

import os
import re

# TODO:handle non declarations
# TODO: check if for/var/function are words inside a string
# TODO: surround in class

func_det_pat = re.compile(r"function\s+([\w$]+)?(\(.*\))\s*\{")


def get_file_contents(path):
    file = open(path, "r")
    contents = file.read()
    file.close()
    return contents  # , (len(contents))


def detect_func_declaration(contents, start=0):
    match = func_det_pat.search(contents, start)
    if match is None:
        return None, start

    l_brance_after = match.end()
    r_brace_index = get_matched_braces_end(contents, l_brance_after)
    if match.group(1) is None:
        return None, r_brace_index
    #
    # if is_inside_function(contents, match.start(), r_brace_index):
    #     return None,r_brace_index
    # TODO: probably don't need to check since top level functions will be skipped over
    return match, r_brace_index


def get_matched_braces_end(content, start, start_tok=None, end_tok=None):
    """
    content: entire file
    start: index of { + 1
    """
    expected_rb_count = 1
    r_b_index = -1
    while expected_rb_count > 0:
        r_b_index = content.find('}', start)
        l_b_count = content.count('{', start, r_b_index)
        expected_rb_count += l_b_count - 1
        start = r_b_index + 1

    """
     base case: simple function with no blocks (functions/loops/cconds) inside
    before loop: count=1, rb=-1
    in loop: rb at con[rb]==}
    no more {, so lb = 0,

    rb found so count--
    start at rb, but not needed
    loop not repeated
    """

    """
    repeated case: many nested or chained blocks
    before loop: count=1, rb=-1
    in loop: rb at end of nested blocks
    check number of { from start to }
    expected rb count+= number of lb
    start at rb, to check for more blocks,
    keep looping till all rb found
    finally, after all nesting is gone through, rb count= 1(function end })

    when last rb found, count ==0, loop not repeated
    return index of rb
    """
    return r_b_index


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
    return ''.join(dec)


def fun_all(contents, start=0):
    match, rb = detect_func_declaration(contents, start)
    if match is None:
        return contents
    info = get_fun_info(contents, match, rb)
    ret = correct_func(info)
    return ret


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
