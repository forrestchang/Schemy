# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from schemy.eval import eval
import unittest


class TestEval(unittest.TestCase):

    def test_eval(self):
        self.assertEqual(eval('10'), 10)
        self.assertEqual(eval('(quote 10)'), '10')
        self.assertEqual(eval('(if 10>5 10 5)'), 10)
        self.assertEqual(eval('(define r 10) r'), 10)


if __name__ == '__main__':
    unittest.main()