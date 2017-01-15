

class NoMatchingCases(Exception):
    pass


class CaseCalledSeveralTimes(Exception):
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
        self._one_case_has_matched = False
        self._previous_case_has_matched = False
        self._break_order = False
        self._passed_cases = set()

    def case(self, expression):
        if self._break_order:
            return _NO_MATCH
        if expression in self._passed_cases:
            raise CaseCalledSeveralTimes()
        c = _Case(self, expression)
        self._one_case_has_matched |= c.is_matching()
        self._passed_cases.add(expression)
        if c.is_matching() or (not self._break_order and  self._previous_case_has_matched):
            match = [c]
            self._previous_case_has_matched = True
        else:
            match = _NO_MATCH
            self._previous_case_has_matched = False
        return match

    def case_in(self, expressions):
        for expr in expressions:
            case = self.case(expr)
            if case:
                return case
        return _NO_MATCH

    def default_case(self):
        run_default = not self._one_case_has_matched
        self._one_case_has_matched = True
        return [True] if run_default else _NO_MATCH
                
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if not self._one_case_has_matched:
            raise NoMatchingCases()

