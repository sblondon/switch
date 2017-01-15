import unittest
import unittest.mock

import switch

class Test(unittest.TestCase):

    def test_basic(self):
        self.a = 0

        with switch.Switch("a") as s:
            for c in s.case("a"):
                self.a = 1

        self.assertEqual(1, self.a)

    def test_no_case_found(self):
        with self.assertRaises(switch.NoMatchingCases):
            with switch.Switch("a") as s:
                pass

    def test_default_case(self):
        self.a = 0
        
        with switch.Switch("B") as s:
            for c in s.default_case():
                self.a = 1

        self.assertEqual(1, self.a)

    def test_break_or_continue(self):
        self.a = ""
        with switch.Switch("a") as s:
            for c in s.case("a"):
                self.a += "F"
            for c in s.case("b"):
                self.a += "G"
            for c in s.case("c"):
                self.a += "H"
                s._break()
            for c in s.case("d"):
                self.fail("case d should not be called.")

        self.assertEqual("FGH", self.a)

    def test_run_once_if_one_case_or_another_matches(self):
        self.a = 0

        with switch.Switch(24) as s:
            for c in s.case_in([24, 24]):
                self.a += 1

        self.assertEqual(1, self.a)



if __name__ == '__main__':
    unittest.main()

