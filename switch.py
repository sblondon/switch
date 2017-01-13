import collections

class NoMatchingCase(Exception):
    pass

class Switch:
    def __init__(self):
        self._d = collections.OrderedDict()
        self._default_case = None

    def add_case(self, expression, executable):
        self._d[expression] = executable

    def add_default_case(self, executable):
        self._default_case = executable

    def match(self, value):
        if value not in self._d:
            if self._default_case:
                self._default_case()
            else:
                raise NoMatchingCase()
        else:
            self._d[value]()

