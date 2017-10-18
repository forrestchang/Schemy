# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import numbers

from schemy.exception import bad_type, SchemeError


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
    pass