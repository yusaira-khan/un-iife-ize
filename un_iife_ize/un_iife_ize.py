__author__ = 'yusaira-khan'

import re
import argparse
import signal
import sys
import os


class Stack():
    def __init__(self, num=0):
        self.count = num

    def push(self, num=1):
        self.count += num

    def pop(self, num=1):
        self.count -= num


fun = "_FUN"
nonfun = "_OUT"
var = "_VAR"
unmodified = "_UNMOD"


class Function():
    def __init__(self, contents='', h='.__temp__'):
        self.contents = contents
        self.unmodified = []
        self.all = []
        self.dir = h

    detection_pattern = re.compile(r"function\s+([\w$]+)?(\(.*\))\s*\{")

    def write(self, content, type, index):
        if self.dir is None:
            if type is fun:
                self.all.append((content, index))
            else:
                self.unmodified.append((content, index))
            return
        fname = os.path.join(self.dir, str(index) + type)
        with open(fname, "w+") as tfile:
            tfile.write(content)

    def extract_all(self):
        search_start = 0
        content_end = len(self.contents)

        while True:
            ret, declaration_start_index, right_brace_index = self.extract(search_start)

            if ret is None:
                last = self.contents[search_start:content_end]
                self.write(last, nonfun, search_start)
                return

            self.write(ret, fun, declaration_start_index)
            if search_start != declaration_start_index:
                non_function = self.contents[search_start:declaration_start_index]
                self.write(non_function, nonfun, search_start)

            search_start = right_brace_index + 1

    def detect_declaration(self, start=0):
        match = self.detection_pattern.search(self.contents, start)
        if match is None:
            return None, start
        l_brance_after = match.end()
        r_brace_index = self.get_matched_braces_end(l_brance_after)
        if match.group(1) is None:
            return None, r_brace_index
        #
        # if is_inside_function(contents, match.start(), r_brace_index):
        #     return None,r_brace_index
        # TODO: probably don't need to check since top level functions will be skipped over
        return match, r_brace_index

    def get_matched_braces_end(self, start):
        """start: index of { + 1"""
        content = self.contents
        r_b_index = -1
        bracesStack = Stack(1)
        while bracesStack.count > 0:
            r_b_index = content.find('}', start)
            l_b_count = content.count('{', start, r_b_index)
            bracesStack.pop()  # } found
            bracesStack.push(l_b_count)  # num { found
            start = r_b_index + 1

        return r_b_index  # last } found

    def get_info(self, match, rbrace):
        ret = {
            'name': match.group(1),
            'args': match.group(2),
            'statement_start': match.start(),
            'lbrace_index': match.end() - 1,
            'rbrace_index': rbrace,

        }
        ret['body'] = self.contents[ret['lbrace_index']:ret['rbrace_index'] + 1]
        return ret

    def format(self, info):
        dec = [
            info['name'],
            '=function',
            info['args'],
            info['body'],
            ';']
        return ''.join(dec)

    def extract(self, start=0):
        match, rb = self.detect_declaration(start)
        if match is None:
            return None, None, rb
        info = self.get_info(match, rb)
        ret = self.format(info)
        return ret, info['statement_start'], rb


class Var():
    def __init__(self, contents_list,temp):
        self.contents_list = contents_list
        self.unmodified = []
        self.all = []

    def extract_all(self):
        for content, section_start in self.contents_list:
            content_end = len(content)
            search_start = 0
            while True:
                ret, declaration_index, semi_colon_index = self.extract(content, search_start)
                if ret is None:
                    non_var = content[search_start:content_end]
                    self.unmodified.append((non_var, section_start + search_start))
                    break

                self.all.append((ret, declaration_index + section_start))

                if search_start != declaration_index:
                    non_var = content[search_start:declaration_index]
                    self.unmodified.append((non_var, section_start + search_start))
                search_start = semi_colon_index + 1

    def extract(self, contents, start=0):
        # find var
        var_index = contents.find('var ', start)
        if var_index == -1:
            return None, -1, -1
        end_var = contents.find(';', var_index)
        return self.format(contents, var_index, end_var), var_index, end_var

    def format(self, contents, var_index, end_var):
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


# TODO: check if for/var/function are words inside a string


def handle_file(rpath, wpath=None, temp=None):
    rfile = open(rpath, "r")
    contents = rfile.read()
    rfile.close()
    stuff = handle_contents(contents, temp)

    if wpath is None:
        wpath = rpath + '__no__iife'
    wfile = open(wpath, "w+")
    if stuff is not None:
        wfile.write(stuff)
    wfile.close()


def make_temp_directory(temp, wpath):
    t='.__temp__'
    if temp is None:
        temp = os.path.dirname(wpath)
        t = os.path.join(temp, '.__temp__')
        try:
            os.mkdir(t)
        except OSError as e:
            print(e.strerror)
            os.rmdir(t)
            make_temp_directory(t,wpath)


    else : t = temp
    return t


def merge_parts(functions, vars, unmodified):
    all_parts = functions + vars + unmodified
    all_parts.sort(key=lambda tup: tup[1])

    return all_parts


def handle_contents(contents, temp):
    function_extractor = Function(contents, temp)
    function_extractor.extract_all()

    all_functions = function_extractor.all
    non_functions = function_extractor.unmodified

    # var_extractor = Var(non_functions)
    # var_extractor.extract_all()
    #
    # all_vars = var_extractor.all
    # not_modified = var_extractor.unmodified

    #parts = merge_parts(all_functions, all_vars, not_modified)
    #parts = [string for string, index in parts]
    #return ''.join(parts)


def signal_handler(signal, frame):
    print('Exiting!')
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('read_path')
    p.add_argument('write_path')
    p.add_argument('--temp', help="temporary directory path", type=str, default=None)
    args = p.parse_args()
    t = make_temp_directory(args.temp, args.write_path)
    handle_file(args.read_path, args.write_path, t)
    print('Press Ctrl+C to exit')
