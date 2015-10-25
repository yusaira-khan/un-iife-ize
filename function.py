__author__ = 'yusaira-khan'

import re


class Stack():
    def __init__(self, num=0):
        self.count = num

    def push(self, num=1):
        self.count += num

    def pop(self, num=1):
        self.count -= num


func_det_pat = re.compile(r"function\s+([\w$]+)?(\(.*\))\s*\{")


class Function():
    def __init__(self, contents='', unmodified=[]):
        self.contents = contents
        self.unmodified = unmodified
        self.all = []
        self.start = 0

    def detect_declaration(self, start=0):

        match = func_det_pat.search(self.contents, start)
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
        """
        content: entire file
        start: index of { + 1
        """
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


    def format(self,info):
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
            return None
        info = self.get_info(match, rb)
        ret = self.format(info)
        return ret


