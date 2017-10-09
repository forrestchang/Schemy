# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from schemy.types import Symbol, List, Number


def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


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


def parse(program):
    return read_from_tokens(tokenize(program))
