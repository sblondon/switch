import collections

class NoMatchingCases(Exception):
    pass

class _CaseDoesNotMatch(Exception):
    pass

class _Case:
    def __init__(self, switch, value):
        self._switch = switch
        self._case_value = value

    def is_matching(self):
        return self._switch._value == self._case_value


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
        c = _Case(self, expression) #[1] if expression == self._value else []
        self._has_matched = self._has_matched or c.is_matching()
        return [True] if c.is_matching() or self._continuation else []

    def each_cases_in(self, expressions):
        return [self.case(expr) for expr in expressions]

    def _break(self):
        self._break_order = True
        self._continuation = False

    def default_case(self):
        if not self._has_matched:
            self._has_matched = True
        return [True] if self._has_matched else []
                
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._has_matched:
            raise NoMatchingCases()
