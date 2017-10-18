# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import numbers

import math

import re

from schemy.exception import bad_type, SchemeError, check_type


class SchemeValue:
    """
    The parent class of all Scheme values manipulated by the interpreter.
    The methods here give default implementations, and are overridden in the
    subclasses of SchemeValue.
    """

    def __bool__(self):
        """
        This is the method used by Python's conditionals (if, and, or, not, while)
        to determine whether some value is to be treated as meaning 'true'.

        True if I am supposed to count as a 'True value' in Python.
        """
        return True

    def print_repr(self):
        """The string printed for me by the Scheme 'print' procedure."""
        return str(self)

    # The following methods return SchemeValue.
    #
    # Those ending in 'p'(predicate) return scheme_false to mean false, and some other SchemeValue
    # (often scheme_true) to mean 'true'.

    def booleanp(self):
        return scheme_false

    def notp(self):
        return scbool(not self)

    def eqp(self, y):
        return scbool(self is y)

    def eqvp(self, y):
        """
        True if self equivalent to y (同一个对象).
        """
        return scbool(self is y)

    def equalp(self, y):
        """
        True if self equal in value to y (值相同).
        """
        return scbool(self == y)

    def tomp(self):
        return scheme_true

    def pairp(self):
        return scheme_false

    def nullp(self):
        return scheme_false

    def listp(self):
        return scheme_false

    def length(self):
        bad_type(self, 0, 'length')

    def neg(self):
        """Unary negation (as in -x)"""
        bad_type(self, 0, 'sub')

    def quo(self, y):
        bad_type(self, 0, 'quotient')

    def modulo(self, y):
        bad_type(self, 0, 'modulo')

    def rem(self, y):
        bad_type(self, 0, 'remainder')

    def floor(self):
        bad_type(self, 0, 'floor')

    def ceil(self):
        bad_type(self, 0, 'ceil')

    def eq(self, y):
        bad_type(self, 0, '=')

    def ltp(self, y):
        bad_type(self, 0, '<')

    def gtp(self, y):
        bad_type(self, 0, '>')

    def lep(self, y):
        bad_type(self, 0, "<=")

    def gep(self, y):
        bad_type(self, 0, ">=")

    def evenp(self):
        bad_type(self, 0, "even?")

    def oddp(self):
        bad_type(self, 0, "odd?")

    def zerop(self):
        bad_type(self, 0, "zero?")

    def cons(self, y):
        return Pair(self, y)

    def append(self, y):
        bad_type(self, 0, "append")

    def car(self):
        bad_type(self, 0, "car")

    def cdr(self):
        bad_type(self, 0, "cdr")

    def stringp(self):
        return scheme_false

    def symbolp(self):
        return scheme_false

    def numberp(self):
        return scheme_false

    def integerp(self):
        return scheme_false

    def evaluate_arguments(self, arg_list, env):
        """
        Evaluate the expression in ARG_LIST in env to produce arguments for this procedure.

        Returns an iterable of the results.
        """
        msg = 'attempt to call something of non-function type ({})'
        raise SchemeError(msg.format(type(self).__name__))

    def apply(self, args, env):
        """
        Apply self to a Scheme list of args in environment ENV. Returns either
            A. A tuple (val, None), where val is the value this procedure
                returns when given args and called in env.
            B. A tuple (expr1, env1), where env1 will yield the same result
                and the same effects as evaluating args in env.
        """
        msg = "attempt to call something of non-function type ({0})"
        raise SchemeError(msg.format(type(self).__name__))

    def get_actual_value(self):
        """
        Returns any desired transformation of a value newly fetched from a
        symbol before it is used.
        """
        return self


def scheme_coerce(x):
    """
    Returns the Scheme value corresponding to X. Converts numbers to
    SchemeNumbers and strings to interned symbols.
    SchemeValue are unchanged, other values raise a TypeError.
    """
    if isinstance(x, SchemeValue):
        return x
    elif isinstance(x, numbers.Number):
        return scnum(x)
    elif isinstance(x, str):
        return intern(x)
    else:
        raise TypeError('cannot covert type {} to a SchemeValue').format(type(x))


class okay(SchemeValue):
    """Signifies an undefined value."""
    def __repr__(self):
        return 'okay'

okay = okay() # there is only one instance

# -------
# Booleans
# -------

class scheme_true(SchemeValue):

    def booleanp(self):
        return scheme_true

    def __repr__(self):
        return 'scheme_true'

    def __str__(self):
        return '#t'


class scheme_false(SchemeValue):

    def __bool__(self):
        return False

    def booleanp(self):
        return scheme_true

    def __repr__(self):
        return 'scheme_false'

    def __str__(self):
        return '#f'

scheme_true = scheme_true()
scheme_false = scheme_false()


def scbool(x):
    """
    The Scheme boolean value that corresponds to the Python value x.
    True Python values yield scheme_true, and false values yield scheme_false.
    """
    return scheme_true if x else scheme_false


# ------
# Numbers
# ------

def _check_num(x, name):
    """Returns x if it is a number. Otherwise, indicate a type error in argument 1 of operation name."""
    return check_type(x, scheme_numberp, 1, name)


class SchemeNumber(SchemeValue):
    """The parent class of all Scheme numeric types."""

    def numbrep(self):
        return scheme_true

    def __repr__(self):
        return 'scnum({})'.format(self)

    def eq(self, y):
        return scbool(self == _check_num(y, '='))

    def ltp(self, y):
        return scbool(self < _check_num(y, '<'))

    def gtp(self, y):
        return scbool(self > _check_num(y, ">"))

    def lep(self, y):
        return scbool(self <= _check_num(y, "<="))

    def gep(self, y):
        return scbool(self >= _check_num(y, ">="))

    def zerop(self):
        return scbool(self == 0)


class SchemeInt(SchemeNumber, int):

    def integerp(self):
        return scheme_true

    def neg(self):
        return SchemeInt(-self)

    def quo(self, y):
        check_type(y, scheme_integerp, 1, 'quotient')
        try:
            if (y < 0) != (self < 0)
                return SchemeInt(- (abs(self) // abs(y)))
            else:
                return SchemeInt(self // y)
        except ZeroDivisionError as e:
            raise SchemeError(e)

    def modulo(self, y):
        check_type(y, scheme_integerp, 1, 'modulo')
        try:
            return SchemeInt(self % y)
        except ZeroDivisionError as e:
            raise SchemeError(e)

    def rem(self, y):
        q = self.quo()
        return SchemeInt(self - q * y)

    def floor(self):
        return self

    def ceil(self):
        return self

    def eqvp(self, y):
        return scbool(self == y)

    def evenp(self):
        return scbool(self % 2 == 0)

    def oddp(self):
        return scbool(self % 2 == 1)


class SchemeFloat(SchemeNumber, float):

    def neg(self):
        return SchemeFloat(-self)

    def floor(self):
        return SchemeInt(int(math.floor(self)))

    def ceil(self):
        return SchemeInt(int(math.ceil(self)))

    def eqvp(self, y):
        return scbool(self == y)

scint = SchemeInt
scfloat = SchemeFloat


def scnum(num):
    r = round(num)
    if r == num:
        return scint(r)
    else:
        return scfloat(num)


# ------
# Symbols
# ------


class SchemeSymbol(SchemeValue):
    """Represents a Scheme symbol."""

    def __init__(self, name):
        assert type(name) is str, 'invalid type of symbol name: {}'.format(type(name))
        self.name = name

    def symbolp(self):
        return scheme_true

    def __repr__(self):
        if self is _all_symbols.get(self.name, None):
            return 'intern("{}")'.format(self.name)
        else:
            return 'SchemeSymbol("{}")'.format(self.name)

    def __str__(self):
        return self.name

_all_symbols = {}


def intern(name):
    """
    If name is a string, the canonical symbol named name.
    If name if a symbol, a canonical symbol with that name.
    """
    if isinstance(name, SchemeSymbol):
        if str(name) in _all_symbols:
            return _all_symbols[str(name)]
        else:
            _all_symbols[str(name)] = name
            return name
    if name in _all_symbols:
        return _all_symbols[name]
    else:
        sym = SchemeSymbol(name)
        _all_symbols[name] = sym
        return sym


# ------
# Strings
# ------


class SchemeStr(SchemeValue, str):

    def stringp(self):
        return scheme_true

    def __repr__(self):
        return 'scstr({!r})'.format(str(self))

    _escape = re.compile(r'''"|\.''')

    def print_repr(self):
        s = str.__repr__(self)
        if s[0] == "'":
            s = s[1:-1]
            s = SchemeStr._escape.sub(
                lambda x: (r'\"' if x == '"' else "'" if x == r"\'" else x),
                s
            )
            s = '"' + s + '"'
        return s

scstr = SchemeStr


# -----------------
# Pairs and Scheme lists
# -----------------


class Pair(SchemeValue):
    pass
