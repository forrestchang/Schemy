# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

import unittest

from schemy.eval import evaluate
from schemy.tokenizer import parse


class TestEval(unittest.TestCase):

    def test_eval_number(self):
        self.assertEqual(evaluate(parse('10')), 10)

    def test_eval_quote(self):
        self.assertEqual(evaluate(parse('(quote 10)')), 10)

    def test_eval_if_condition(self):
        self.assertEqual(evaluate(parse('(if (> 10 5) 10 5)')), 10)

    def test_eval_define(self):
        evaluate(parse('(define r 10)'))
        self.assertEqual(evaluate(parse('r')), 10)

    def test_eval_set(self):
        pass

    def test_eval_lambda(self):
        evaluate(parse('(define shit (lambda x (* x x)))'))
        self.assertEqual(evaluate(parse('(shit 10)')), 100)


if __name__ == '__main__':
    unittest.main()