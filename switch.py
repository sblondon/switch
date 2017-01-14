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

    def add_case(self, expression, executable, end_break=True):
        self._d[expression] = {"executable": executable, "break": end_break}

    def case(self, expression):
        if self._break_order:
            return []
        c = _Case(self, expression) #[1] if expression == self._value else []
        self._has_matched = self._has_matched or c.is_matching()
        return [True] if c.is_matching() or self._continuation else []

    def _break(self):
        self._break_order = True
        self._continuation = False

    def default_case(self):
        if not self._has_matched:
            self._has_matched = True
        return [True] if self._has_matched else []

    def add_cases(self, expressions, executable, end_break=True):
        for expression in expressions:
            self.add_case(expression, executable, end_break)

    def add_default_case(self, executable):
        self._default_case = executable

    def _match(self, value):
        if value not in self._d:
            if self._default_case:
                self._default_case()
            elif not self._has_matched:
                raise NoMatchingCases()
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
                
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._match(self._value)

