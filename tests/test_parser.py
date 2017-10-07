import unittest
from schemy.schemy import tokenize


class TestParser(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(tokenize('(+ 1 2)'), ['(', '+', '1', '2', ')'])


if __name__ == '__main__':
    unittest.main()
