# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
from .buffer import Buffer, InputReader, LineReader
from .environments import Frame
from .eval import scheme_eval, scheme_apply
from .exception import SchemeError, check_type
from .procedure import PrimitiveProcedure
from .tokenizer import tokenize_lines, DELIMITERS
from .types import nil, scnum, scbool, scstr, intern, Pair, scheme_stringp, scheme_symbolp, okay, \
    get_primitive_bindings, scheme_print
from .utils import main


def scheme_read(src):
    """
    Read the next expression from SRC, a Buffer of tokens.

    >>> lines = ["(+ 1 ", "(+ 23 4)) ("]
    >>> src = Buffer(tokenize_lines(lines))
    >>> print(scheme_read(src))
    (+ 1 (+ 23 4))
    >>> read_line("'hello")
    Pair('quote', Pair('hello', nil))
    >>> print(read_line("(car '(1 2))"))
    (car (quote (1 2)))
    """

    if src.current() is None:
        raise EOFError
    val = src.pop()
    if val == 'nil':
        return nil
    elif type(val) is int or type(val) is float:
        return scnum(val)
    elif type(val) is bool:
        return scbool(val)
    elif val not in DELIMITERS:
        if val[0] == '"':
            return scstr(eval(val))
        else:
            return intern(val)
    elif val == "'":
        return Pair('quote', Pair(scheme_read(src), nil))
    elif val == '(':
        return read_tail(src)
    else:
        raise SyntaxError('unexpected token: {}'.format(val))


def read_tail(src):
    """
    Return the remainder of a list in src, starting before an element or ).

    >>> read_tail(Buffer(tokenize_lines([')'])))
    nil
    >>> read_tail(Buffer(tokenize_lines(["2 3)"])))
    Pair(2, Pair(3, nil))
    >>> read_tail(Buffer(tokenize_lines(["2 (3 4))"])))
    Pair(2, Pair(Pair(3, Pair(4, nil)), nil))
    >>> read_line("(1 . 2)")
    Pair(1, 2)
    >>> read_line("(1 2 . 3)")
    Pair(1, Pair(2, 3))
    >>> read_line("(1 . 2 3)")
    Traceback (most recent call last):
        ...
    SyntaxError: Expected one element after .
    >>> scheme_read(Buffer(tokenize_lines(["(1", "2 .", "'(3 4))", "4"])))
    Pair(1, Pair(2, Pair('quote', Pair(Pair(3, Pair(4, nil)), nil))))
    >>> read_line("((1 1 . 2) . 1)")
    Pair(Pair(1, Pair(1, 2)), 1)
    """
    try:
        if src.current() is None:
            raise SyntaxError('unexpected end of file')
        if src.current() == ')':
            src.pop()
            return nil
        if src.current() == '.':
            src.pop()
            first = scheme_read(src)
            if read_tail(src) is nil:
                return first
            raise SyntaxError('expected one element after .')
        first = scheme_read(src)
        rest = read_tail(src)
        return Pair(first, rest)
    except EOFError:
        raise SyntaxError('unexpected end of file')

# helper methods

def buffer_input(prompt='Schemy> '):
    return Buffer(tokenize_lines(InputReader(prompt)))


def buffer_lines(lines, prompt='Schemy> ', show_prompt=False):
    """Return a Buffer instance iterating through Lines."""
    if show_prompt:
        input_lines = lines
    else:
        input_lines = LineReader(lines, prompt)
    return Buffer(tokenize_lines(input_lines))


def read_line(line):
    """Read a single string line as a Scheme expression."""
    return scheme_read(Buffer(tokenize_lines([line])))


def read_eval_print_loop(next_line, env, quiet=False, startup=False, interactive=False, load_files=()):
    if startup:
        for filename in load_files:
            scheme_load(scstr(filename), True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
            result = scheme_eval(expression, env)
            if not quiet and result is not None:
                scheme_print(result)
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as e:
            if (isinstance(e, RuntimeError) and
                'maximum recursion depth exceeded' not in e.args[0]):
                raise
            print('Error: ', e)
        except KeyboardInterrupt:
            if not startup:
                raise
            print('\nKeboardInterrupt')
            if not interactive:
                return
        except EOFError:
            return


def scheme_load(*args):
    """Load a Scheme source file."""
    if not (2 <= len(args) <= 3):
        vals = args[:-1]
        raise SchemeError('wrong number of arguments to load: {}'.format(vals))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = intern(str(sym))
    check_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(str(sym)) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)
    read_eval_print_loop(next_line, env.global_frame(), quiet=quiet)
    return okay


def scheme_open(filename):
    try:
        return open(filename)
    except IOError as exc:
        if filename.endwith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))


def create_global_frame():
    """Init and return a single frame env with build in names."""
    env = Frame(None)
    env.define('eval', PrimitiveProcedure(scheme_eval, True))
    env.define('apply', PrimitiveProcedure(scheme_apply, True))
    env.define('load', PrimitiveProcedure(scheme_load, True))

    for names, func in get_primitive_bindings():
        for name in names:
            proc = PrimitiveProcedure(func)
            env.define(name, proc)
    return env


@main
def read_print_loop():
    """Run a read-print loop for Scheme expressions."""
    while True:
        try:
            src = buffer_input('Schemy> ')
            while src.more_on_line:
                expression = scheme_read(src)
                print(expression)
                print(repr(expression))
        except (SyntaxError, ValueError) as e:
            print(type(e).__name__ + ':', e)
        except (KeyboardInterrupt, EOFError):
            return
