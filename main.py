__author__ = 'yusaira-khan'

import os
import re

# TODO:handle non declarations
# TODO: check if for/var/function are words inside a string
# TODO: surround in class

func_det_pat = re.compile(r"function\s+([\w$]+)?(\(.*\))\s*\{")
class Stack():
    def __init__(self,num=0):
        self.count = num

    def push(self,num=1):
        self.count+=num

    def pop(self,num=1):
        self.count-=num


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
    r_b_index = -1
    bracesStack =Stack(1)
    while bracesStack.count > 0:
        r_b_index = content.find('}', start)
        l_b_count = content.count('{', start, r_b_index)
        bracesStack.pop() #} found
        bracesStack.push(l_b_count) #num { found
        start = r_b_index + 1

    return r_b_index #last } found


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
