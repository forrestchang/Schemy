# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
from schemy.buffer import Buffer, InputReader, LineReader
from schemy.tokenizer import tokenize_lines, DELIMITERS
from schemy.types import nil, scnum, scbool, scstr, intern, Pair
from schemy.utils import main


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


# repl
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
