import unittest
from schemy.schemy import tokenize, parse, eval


class TestSchemy(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(tokenize('(+ 1 2)'), ['(', '+', '1', '2', ')'])

    def test_parser(self):
        program = "(begin (define r 10) (* pi (* r r)))"
        result = ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]
        self.assertEqual(parse(program), result)

    def test_eval(self):
        program = "(begin (define r 10) (* 3.14 (* r r)))"
        self.assertEqual(eval(parse(program)), 3.14*10*10)


if __name__ == '__main__':
    unittest.main()
