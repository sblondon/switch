import unittest
import unittest.mock

import switch

class Test(unittest.TestCase):

    def test_basic(self):
        self.a = 0
        def f():
            self.a = 1
        s = switch.Switch()
        s.add_case("a", f)
        
        s.match('a')

        self.assertEqual(1, self.a)

    def test_no_case_found(self):
        s = switch.Switch()
        
        with self.assertRaises(switch.NoMatchingCase):
            s.match('a')

    def test_default_case(self):
        self.a = 0
        def f():
            self.a = 1
        s = switch.Switch()
        s.add_default_case(f)
        
        s.match('B')

        self.assertEqual(1, self.a)

    def test_break_or_continue(self):
        self.a = ""
        def f():
            self.a += "F"
        def g():
            self.a += "G"
        def h():
            self.a += "H"
        def i():
            self.fail("Function i() should not be called.")

        s = switch.Switch()
        s.add_case("a", f, False)
        s.add_case("b", g, False)
        s.add_case("c", h)
        s.add_case("d", i)
        
        s.match('a')

        self.assertEqual("FGH", self.a)

    def test_several_cases_at_same_time(self):
        self.a = 0
        def f():
            self.a += 1
        s = switch.Switch()
        s.add_cases([24, 42], f)

        s.match(24)
        s.match(42)

        self.assertEqual(2, self.a)

    def test_several_cases_at_same_time_with_break_disabled(self):
        self.a = 0
        def f():
            self.a += 1
        s = switch.Switch()
        s.add_cases([24, 42], f, False)

        s.match(24)

        self.assertEqual(2, self.a)


if __name__ == '__main__':
    unittest.main()

