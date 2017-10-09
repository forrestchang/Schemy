# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from schemy.tokenizer import parse
from schemy.types import List


def repl(prompt='schemy>>> '):
    while True:
        try:
            val = eval(parse(input(prompt)))
            if val is not None:
                print(schemestr(val))
        except (SyntaxError, TypeError) as e:
            print(e)
        # except KeyError as e:
        #     print('invalid key', e.args)


def schemestr(exp):
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)