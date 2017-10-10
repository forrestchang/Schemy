# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

import unittest
from schemy.tokenizer import tokenize, parse, atom
from schemy.types import Symbol


class TestTokenizer(unittest.TestCase):

    def test_tokenize_number(self):
        self.assertEqual(tokenize('1'), ['1'])

    def test_tokenize_nil(self):
        self.assertEqual(tokenize('()'), ['(', ')'])

    def test_tokenize_base_calc(self):
        self.assertEqual(tokenize('(+ 1 2)'), ['(', '+', '1', '2', ')'])
        self.assertEqual(
            tokenize('(* (+ 1 2) (- 3 4))'),
            ['(', '*', '(', '+', '1', '2', ')', '(', '-', '3', '4', ')', ')']
        )

    def test_atom(self):
        self.assertEqual(atom('10'), int('10'))
        self.assertEqual(atom('10.123'), float('10.123'))
        self.assertEqual(atom('define'), Symbol('define'))

    def test_parse(self):
        program = "(begin (define r 10) (* pi (* r r)))"
        result = ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]
        self.assertEqual(parse(program), result)


if __name__ == '__main__':
    unittest.main()
