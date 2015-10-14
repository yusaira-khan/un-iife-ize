__author__ = 'yusaira-khan'

import os
import re
import string



#TODO: check if for/var/function are words inside a string
# print(os.path.dirname(os.path.realpath(__file__)))
current_dir=os.path.dirname(os.path.realpath(__file__))
speex_path = os.path.join(current_dir,'speex/speex.min.js')

def get_file_contents(path):
    file = open(path,"r")
    contents = file.read()
    file.close()
    return contents#, (len(contents))

def examine_var_statement(contents):
    start = 0
    #find var
    var_index = contents.find('var',start)
    end_var = contents.find(';',var_index)
    if is_inside_function(contents,var_index,end_var):
        return None
    statement = contents[var_index:end_var]

    #removing var
    decs =statement[3:].split(',')
    for d in decs:
        if '=' in d:
            continue
            #do nothing
        d+='=undefined'
    ret=','.join(decs)
    ret+=';'

def is_inside_function(contents,start, end):
    len_function_declaration = 11
    if start < len_function_declaration:
        return False

    #TODO: check for blocks inside function
    fun_index = contents.rfind('function',0,start)
    if fun_index == -1:
        return False
    fun_start = contents.find('{',fun_index)
    fun_end = get_matched_braces_end(contents,fun_start + 1)
    #for loop ends before var declaration
    if fun_end < start:
        return False
    return True

def is_inside_for_loop(contents, start, end):
    len_for_loop= 4
    if start< 4:
        return False
    for_index = contents.rfind('for',0,start)
    for_end = contents.find(')',for_index)

    #no for loop exists before var declaration
    if for_index == -1 :
        return False
    #for loop ends before var declaration
    if for_end < start:
        return False

    return True
def handle_file(contents):
    parts=[]
    parts[0] = "var declarations"
    parts[1] = "function declartions"
    parts[2] = "parts inside functions"
    parts[3] = "parts that don't need modification"

    return ''.join(parts)
#####
#THIS IS ANNOYING
#####

def get_matched_braces_end(content,start,start_tok= None,end_tok = None):
    """
    content: entire file
    start: index of { + 1
    """
    count = 1
    r_b_index = -1
    while count != 0:
        r_b_index = content.find('}',start)
        count -= 1
        l_b_count = content.count('{',start, r_b_index)
        count+= l_b_count
    return  r_b_index





def examine_function(contents):
    pass






