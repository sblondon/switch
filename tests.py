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



if __name__ == '__main__':
    unittest.main()

