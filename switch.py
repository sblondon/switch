

class NoMatchingCases(Exception):
    pass


class _Case:
    def __init__(self, switch, value):
        self._switch = switch
        self._case_value = value

    def is_matching(self):
        return self._switch._value == self._case_value

    def __getattr__(self, name):
        if name == "BREAK":
            self._switch._break_order = True

_NO_MATCH = []


class Switch:

    def __init__(self, value):
        self._default_case = None
        self._value = value
        self._has_matched = False
        self._continuation = True
        self._break_order = False
        self._first_case = True

    def case(self, expression):
        if self._break_order:
            return _NO_MATCH
        c = _Case(self, expression)
        self._has_matched = self._has_matched or c.is_matching()
        if c.is_matching() or (self._continuation and not self._first_case):
            match = [c]
        else:
            match = _NO_MATCH
        if self._first_case:
            self._first_case = False
        return match

    def case_in(self, expressions):
        for expr in expressions:
            case = self.case(expr)
            if case:
                return case
        return _NO_MATCH

    def _break(self):
        self._break_order = True
        self._continuation = False

    def default_case(self):
        run_default = not self._has_matched
        self._has_matched = True
        return [True] if run_default else _NO_MATCH
                
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._has_matched:
            raise NoMatchingCases()

