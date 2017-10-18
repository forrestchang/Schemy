# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
from .utils import main
import itertools
import string
import sys
import tokenize

_NUMERAL_STARTS = set(string.digits) | set('+-.')
_SYMBOL_CHARS = (set('!$%&*/:<=>?@^_~') | set(string.ascii_lowercase) | set(string.ascii_uppercase) | _NUMERAL_STARTS)
_STRING_DELIMS = set('"')
_WHITESPACE = set(' \t\n\r')
_SINGLE_CHAR_TOKENS = set("()'`")
_TOKEN_END = _WHITESPACE | _SINGLE_CHAR_TOKENS | _STRING_DELIMS | {',', ',@'}
DELIMITERS = _SINGLE_CHAR_TOKENS | {'.', ',', ',@'}


def valid_symbol(s):
    """ Return whethre s is not a well-formed value. """
    if len(s) == 0:
        return False
    for c in s:
        if c not in _SYMBOL_CHARS:
            return False
    return True


def next_candidate_token(line, k):
    """
    A tuple (tok, k), where tok is the next substring of line at or after position k that could be a token,
    and k is the position in line following that token.

    Returns (None, len(line)) when there are no more tokens.
    """
    while k < len(line):
        c = line[k]
        if c == ';':
            return None, len(line)
        elif c in _WHITESPACE:
            k += 1
        elif c in _SINGLE_CHAR_TOKENS:
            return c, k+1
        elif c == '#': # Boolean #t or #f
            return line[k:k+2], min(k+2, len(line))
        elif c == ',': # Unquote; check for @
            if k+1 < len(line) and line[k+1] == '@':
                return ',@', k+2
            return c, k+1
        elif c in _STRING_DELIMS:
            if k+1 < len(line) and line[k+1] == c: # No triple quotes in Scheme
                return c+c, k+2
            line_bytes = (bytes(line[k:], encoding='utf-8'),)
            gen = tokenize.tokenize(iter(line_bytes).__next__)
            next(gen) # Throw away encoding token
            token = next(gen)
            if token.type != tokenize.STRING:
                raise ValueError('invalid string: {}'.format(token.string))
            return token.string, token.end[1]+k
        else:
            j = k
            while j < len(line) and line[j] not in _TOKEN_END:
                j += 1
            return line[k:j], min(j, len(line))
    return None, len(line)