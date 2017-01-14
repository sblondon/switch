import unittest
import unittest.mock

import switch

class Test(unittest.TestCase):

    def test_basic(self):
        self.a = 0
        def f():
            self.a = 1

        with switch.Switch("a") as s:
            s.add_case("a", f)
        
        self.assertEqual(1, self.a)

    def test_no_case_found(self):
        with self.assertRaises(switch.NoMatchingCases):
            with switch.Switch("a") as s:
                pass

    def test_default_case(self):
        self.a = 0
        def f():
            self.a = 1
        
        with switch.Switch("B") as s:
            s.add_default_case(f)

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

        with switch.Switch("a") as s:
            s.add_case("a", f, False)
            s.add_case("b", g, False)
            s.add_case("c", h)
            s.add_case("d", i)

        self.assertEqual("FGH", self.a)

    def test_several_cases_at_same_time_with_break_disabled(self):
        self.a = 0
        def f():
            self.a += 1

        with switch.Switch(24) as s:
            s.add_cases([24, 42], f, False)

        self.assertEqual(2, self.a)

    def test_use_context_managers_for_case(self):
        self.a = 0
        with switch.Switch("a") as s:
            with s.case("a"):
                self.a = 1

            self.assertEqual(1, self.a)



if __name__ == '__main__':
    unittest.main()

