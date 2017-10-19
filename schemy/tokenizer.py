# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import itertools
import string
import sys
import tokenize

from .utils import main

_NUMERAL_STARTS = set(string.digits) | set('+-.')
_SYMBOL_CHARS = (set('!$%&*/:<=>?@^_~') | set(string.ascii_lowercase) | set(string.ascii_uppercase) | _NUMERAL_STARTS)
_STRING_DELIMS = set('"')
_WHITESPACE = set(' \t\n\r')
_SINGLE_CHAR_TOKENS = set("()'`")
_TOKEN_END = _WHITESPACE | _SINGLE_CHAR_TOKENS | _STRING_DELIMS | {',', ',@'}
DELIMITERS = _SINGLE_CHAR_TOKENS | {'.', ',', ',@'}


def valid_symbol(s):
    """ Return whether s is not a well-formed value. """
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


def tokenize_line(line):
    """ The list of Scheme tokens on line. Excludes comments and whitespace. """
    result = []
    text, i = next_candidate_token(line, 0)
    while text is not None:
        if text in DELIMITERS:
            result.append(text)
        elif text == '#t' or text.lower() == 'true':
            result.append(True)
        elif text == '#f' or text.lower() == 'false':
            result.append(False)
        elif text == 'nil':
            result.append(text)
        elif text[0] in _SYMBOL_CHARS:
            number = False
            if text[0] in _NUMERAL_STARTS:
                try:
                    result.append(int(text))
                    number = True
                except ValueError:
                    try:
                        result.append(float(text))
                        number = True
                    except ValueError:
                        pass
            if not number:
                if valid_symbol(text):
                    result.append(text.lower())
                else:
                    raise ValueError('invalid numeral or symbol: {}'.format(text))
        elif text[0] in _STRING_DELIMS:
            result.append(text)
        else:
            print('warning: invalid token: {}'.format(text), file=sys.stderr)
            print('    ', line, file=sys.stderr)
            print(' ' * (i+3), '^', file=sys.stderr)
        text, i = next_candidate_token(line, i)
    return result


def tokenize_lines(input):
    """ An iterator that returns list of tokens, one for each line of the iterable input sequence. """
    return [tokenize_line(line) for line in input]


def count_tokens(input):
    """ Count the number of no-delimiter tokens in input. """
    return len(list(filter(lambda x: x not in DELIMITERS, itertools.chain(*tokenize_lines(input)))))


@main
def run(*args):
    file = sys.stdin
    if args:
        file = open(args[0], 'r')
    print('counted ', count_tokens(file), ' non-delimiter tokens')
