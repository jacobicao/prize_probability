# -*- coding: utf-8 -*-
"""
Prize Probability
1 0.06
2 0.08
3 0.18
4 0.38
5 0.20
6 0.10

Question 1:
Calculate the probability of assemble all prize at x days
Days Probability
1 ?
2 ?
3 ?
...


Question 2:
Calculate the probability of assemble x prize at 7 days
Prizes Probability
1 ?
2 ?
3 ?
...

"""
from itertools import combinations, combinations_with_replacement
from scipy.special import factorial
from collections import Counter
import pandas as pd
import numpy as np


class AssembleGame:
    def __init__(self, p, save=False):
        if not isinstance(p, (list, tuple)):
            raise ValueError('Must input list')
        if not all(map(lambda x: isinstance(x, float), p)):
            raise ValueError('Must input float list')
        if p is None or len(p) == 0:
            raise ValueError('Can not input empty list')
        self.p = p
        self.save = save
        self.max_days = 20

    def _assemble_all_prize_at_d_days(self, p, d):
        if d > self.max_days:
            raise ValueError('The number of days is too large')
        m = len(p)
        if d < m:
            return 0
        if d == m:
            return np.prod(p) * factorial(m)
        re = 0
        for x in combinations(p, 1):
            sec = list(set(p) - set(x))
            for y in combinations_with_replacement(sec, d - m):
                sub = np.append(sec, y)
                cc = filter(lambda z: z > 1, Counter(sub).values())
                num = np.prod([factorial(c) for c in cc])
                re += sub.prod() * factorial(d - 1) / num * x[0]
        return re

    def assemble_all_prize_at_d_days(self, d):
        return self._assemble_all_prize_at_d_days(self.p, d)

    def assemble_all_prize_to_d_days(self, d):
        if d > self.max_days:
            raise ValueError('The number days is too large')
        ds = len(self.p)
        win = [(n, self._assemble_all_prize_at_d_days(self.p, n)) for n in range(ds, ds + d)]
        col = ['Days', 'Probability']
        df = pd.DataFrame(win, columns=col)
        if self.save:
            df.to_csv('total_assemble_prob_to_%d_days.csv' % d, index=False, float_format='%.4f')
        else:
            print(df)

    def assemble_n_prize_at_d_days(self, n, d):
        m = len(self.p)
        if d < 1:
            return 0
        if n > m or n < 1:
            return 0
        if n == 1 and d == 1:
            return 1
        if n == 1 and d > 1:
            return 0
        re = 0
        for x in combinations(self.p, n):
            re += self._assemble_all_prize_at_d_days(x, d)
        return re

    def assemble_1_to_all_prize_at_d_days(self, d):
        m = len(self.p)
        cards = {'C%d' % n: self.assemble_n_prize_at_d_days(n, d) for n in range(1, m + 1)}
        return pd.Series(cards)

    def assemble_1_to_all_prize_to_d_days_acc(self, ds):
        """
        :param ds: It means that the days of calculation is from 1 to ds.
        :return: The result accmulates by days.
        """
        ds = ds + 1
        ll = {'D%02d' % d: self.assemble_1_to_all_prize_at_d_days(d) for d in range(1, ds)}
        df = pd.DataFrame(ll).T.cumsum()
        if self.save:
            df.to_csv('n_assemble_prob_to_%d_acc.csv' % ds, float_format='%.4f')
        else:
            print(df)


def example():
    p = [0.06, 0.08, 0.18, 0.38, 0.2, 0.1]
    game = AssembleGame(p)
    game.assemble_all_prize_to_d_days(10)
    game.assemble_1_to_all_prize_to_d_days_acc(10)


if __name__ == '__main__':
    example()
