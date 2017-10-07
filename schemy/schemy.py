import math
import operator as op


Symbol = str
List = list
Number = (int, float)


def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program):
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)   # pop off ')'
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


class Env(dict):
    """环境是以 {'var':val} 为键对的字典,它还带着一个纸箱外层环境的引用"""
    def __init__(self, parms=(), args=(), outer=None, **kwargs):
        super().__init__(**kwargs)
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """寻找变量出现的最内层环境"""
        return self if (var in self) else self.outer.find(var)


class Procedure(object):

    def __init__(self, parms, body, env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))


def standard_env():
    env = Env()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'append': op.add,
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()


def eval(x, env=global_env):
    if isinstance(x, Symbol):
        return env[x]
    elif not isinstance(x, List):
        return x
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':
        (_, var, exp) = x
        env[var] = eval(exp, env)
    else:
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)


# repl: read-eval-print-loop
def repl(prompt='schemy>>> '):
    while True:
        try:
            val = eval(parse(input(prompt)))
            if val is not None:
                print(schemestr(val))
        except (SyntaxError, TypeError) as e:
            print(e)
        except KeyError as e:
            print('invalid key', e.args)



def schemestr(exp):
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)


def main():
    repl()


if __name__ == '__main__':
    main()