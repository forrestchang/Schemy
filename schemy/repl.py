# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from .tokenizer import parse
from .types import List
from .eval import evaluate


def schemestr(exp):
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)


def repl(prompt='Schemy >>> '):
    while True:
        try:
            val = evaluate(parse(input(prompt)))
            if val is not None:
                print(schemestr(val))
        except (SyntaxError, TypeError) as e:
            print(e)
        # except KeyError as e:
        #     print('invalid key', e.args)
