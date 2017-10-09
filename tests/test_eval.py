# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from schemy.eval import evaluate
from schemy.tokenizer import parse
import unittest


class TestEval(unittest.TestCase):

    def test_eval(self):
        # self.assertEqual(evaluate(parse('10')), 10)
        # self.assertEqual(evaluate(parse('(quote 10)')), 10)
        # self.assertEqual(evaluate(parse('(if (> 10 5) 10 5)')), 10)
        self.assertEqual(evaluate(parse('(define r 10) (r)')), 10)


if __name__ == '__main__':
    unittest.main()