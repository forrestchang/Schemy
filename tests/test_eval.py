# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

import unittest

from schemy.eval import evaluate, run
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

    def test_fact_function(self):
        evaluate(parse('(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))'))
        self.assertEqual(evaluate(parse('(fact 10)')), 3628800)
        fact_100_rst = 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000
        self.assertEqual(evaluate(parse('(fact 100)')), fact_100_rst)

    def test_count_function(self):
        run('(define first car)')
        run('(define rest cdr)')
        run('(define count (lambda (item L) (if L (+ (equal? item (first L)) (count item (rest L))) 0)))')
        self.assertEqual(run('(count 0 (list 0 1 2 0 3 4 5))'), 2)
        self.assertEqual(run('(count (quote the) (quote (the more the merrier the bigger the better)))'), 4)

    def test_inner_function(self):
        self.assertEqual(run('(pow 2 16)'), 65536.0)

    def test_fib(self):
        run('(define fib (lambda (n) (if (< n 2) 1 (+ (fib (- n 1)) (fib (- n 2))))))')
        run('(define range (lambda (a b) (if (= a b) (quote ()) (cons a (range (+ a 1) b)))))')
        self.assertEqual(run('(range 0 10)'), list(range(0, 10)))
        self.assertEqual(list(run('(map fib (range 0 10))')), [1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
        self.assertEqual(list(run('(map fib (range 0 20))')),
                         [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765])


if __name__ == '__main__':
    unittest.main()
