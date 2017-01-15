import unittest

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

    def test_can_not_call_same_case_two_times(self):
        with self.assertRaises(switch.CaseCalledSeveralTimes):
            with switch.Switch("a") as s:
                for c in s.case("a"):
                    pass
                for c in s.case("a"):
                    pass

    def test_default_case(self):
        self.a = 0
        
        with switch.Switch("B") as s:
            for c in s.default_case():
                self.a = 1

        self.assertEqual(1, self.a)

    def test_default_case_does_not_run_if_previous_case_matched(self):
        self.a = 0
        
        with switch.Switch("a") as s:
            for c in s.case("a"):
                self.a = 1
            for c in s.default_case():
                self.a = 2

        self.assertEqual(1, self.a)

    def test_break_or_continue(self):
        self.a = ""
        with switch.Switch("a") as s:
            for c in s.case("0"):
                self.fail("case 0 should not be called.")
            for c in s.case("a"):
                self.a += "F"
            for c in s.case("b"):
                self.a += "G"
            for c in s.case("c"):
                self.a += "H"
                c.BREAK
            for c in s.case("d"):
                self.fail("case d should not be called.")

        self.assertEqual("FGH", self.a)

    def test_several_unmatched_at_begining_cases(self):
        self.a = 0
        with switch.Switch("a") as s:
            for c in s.case("0"):
                self.fail("case 0 should not be called.")
            for c in s.case("1"):
                self.fail("case 1 should not be called.")
            for c in s.case("a"):
                self.a = 1

        self.assertEqual(1, self.a)

    def test_run_once_if_one_case_or_another_matches(self):
        self.a = 0

        with switch.Switch(24) as s:
            for c in s.case_in([24, 24]):
                self.a += 1

        self.assertEqual(1, self.a)



if __name__ == '__main__':
    unittest.main()

