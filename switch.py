import collections

class NoMatchingCases(Exception):
    pass


class _Case:
    def __init__(self, switch, value):
        self._switch = switch
        self._case_value = value

    def is_matching(self):
        return self._switch._value == self._case_value

_MATCH = [True]
_NO_MATCH = []

class Switch:

    def __init__(self, value):
        self._d = collections.OrderedDict()
        self._default_case = None
        self._value = value
        self._has_matched = False
        self._continuation = True
        self._break_order = False

    def case(self, expression):
        if self._break_order:
            return []
        c = _Case(self, expression)
        self._has_matched = self._has_matched or c.is_matching()
        return _MATCH if c.is_matching() or self._continuation else _NO_MATCH

    def case_in(self, expressions):
        for expr in expressions:
            if self.case(expr):
                return _MATCH
        return _NO_MATCH

    def _break(self):
        self._break_order = True
        self._continuation = False

    def default_case(self):
        if not self._has_matched:
            self._has_matched = True
        return _MATCH if self._has_matched else _NO_MATCH
                
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._has_matched:
            raise NoMatchingCases()

