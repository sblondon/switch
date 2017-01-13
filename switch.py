import collections

class NoMatchingCase(Exception):
    pass

class Switch:
    def __init__(self):
        self._d = collections.OrderedDict()
        self._default_case = None

    def add_case(self, expression, executable, end_break=True):
        self._d[expression] = {"executable": executable, "break": end_break}

    def add_default_case(self, executable):
        self._default_case = executable

    def match(self, value):
        if value not in self._d:
            if self._default_case:
                self._default_case()
            else:
                raise NoMatchingCase()
        else:
            self._exec_match(value)

    def _exec_match(self, value):
        match = self._d[value]
        match["executable"]()
        if not match["break"]:
            use_next = False
            for key in self._d:
                if use_next:
                    self._exec_match(key)
                    break
                if key == value:
                    use_next = True
                

