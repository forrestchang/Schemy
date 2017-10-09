# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from .eval import evaluate
from .tokenizer import parse
from .types import List


def schemestr(exp):
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)


def repl(prompt='Schemy> '):
    print('Schemy 0.0.1')
    print('Type "help" for more information.')

    while True:
        code = input(prompt)

        if code in ('exit', 'quit'):
            print('Goodbye!')
            break
        elif code == 'help':
            print('Sorry, no help yet.')
        else:
            try:
                val = evaluate(parse(code))
                if val is not None:
                    print(schemestr(val))
            except (SyntaxError, TypeError) as e:
                print(e)
            except KeyError as e:
                print('invalid key', e.args)
