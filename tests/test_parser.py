import unittest
from schemy.schemy import tokenize, parse


class TestParser(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(tokenize('(+ 1 2)'), ['(', '+', '1', '2', ')'])

    def test_parser(self):
        program = "(begin (define r 10) (* pi (* r r)))"
        result = ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]
        self.assertEqual(parse(program), result)


if __name__ == '__main__':
    unittest.main()
