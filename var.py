__author__ = 'yusaira-khan'


class Var():
    def __init__(self, contents_list):
        self.contents_list = contents_list
        self.unmodified = []
        self.all = []

    def extract_all(self):
        for content, section_start in self.contents_list:
            search_start = 0
            while True:
                ret, declaration_index, semi_colon_index = self.extract(content, search_start)
                if ret is None:
                    break

                self.all.append((ret, declaration_index + section_start))

                if search_start != declaration_index:
                    self.unmodified.append((content[search_start:declaration_index], section_start + search_start))
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
