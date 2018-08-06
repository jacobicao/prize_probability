import unittest
import numpy as np
from prize_probability import AssembleGame


class TestAssembleGame(unittest.TestCase):
    def test_init(self):
        p = [0.06, 0.08, 0.18, 0.38, 0.2, 0.1]
        g = AssembleGame(p)
        self.assertEqual(g.p, p)

    def test_value_at_day_6(self):
        def assemble_at_6(x):
            return np.prod(x) * np.math.factorial(6)

        p = [0.06, 0.08, 0.18, 0.38, 0.2, 0.1]
        g = AssembleGame(p)
        self.assertAlmostEqual(assemble_at_6(p), g.assemble_all_prize_at_d_days(6))

    def test_value_at_day_7(self):
        def assemble_at_7(pp):
            re = 0
            for x in pp:
                sec = list(set(pp) - set([x]))
                re += np.sum(sec) * np.prod(sec) * np.math.factorial(6) * x / 2
            return re

        p = [0.06, 0.08, 0.18, 0.38, 0.2, 0.1]
        g = AssembleGame(p)
        self.assertAlmostEqual(assemble_at_7(p), g.assemble_all_prize_at_d_days(7))

    def test_input(self):
        p = ['la', 'a', 'b', 'c', 'd', 'e']
        with self.assertRaises(ValueError):
            AssembleGame(p)
        p = 'la'
        with self.assertRaises(ValueError):
            AssembleGame(p)
        p = []
        with self.assertRaises(ValueError):
            AssembleGame(p)
        p = None
        with self.assertRaises(ValueError):
            AssembleGame(p)

    def test_extreme_value(self):
        p = [0.06, 0.08, 0.18, 0.38, 0.2, 0.1]
        g = AssembleGame(p)
        with self.assertRaises(ValueError):
            g.assemble_all_prize_to_d_days(99)
        self.assertEqual(0, g.assemble_all_prize_at_d_days(len(p) - 1))
        self.assertEqual(1, g.assemble_n_prize_at_d_days(1, 1))
        self.assertEqual(0, g.assemble_n_prize_at_d_days(1, 10))
        self.assertEqual(0, g.assemble_n_prize_at_d_days(1, -10))
        self.assertEqual(0, g.assemble_n_prize_at_d_days(len(p) + 1, 10))


if __name__ == '__main__':
    unittest.main()
