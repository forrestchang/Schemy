# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from .types import *
from .repl import *
from .utils import main, trace


def scheme_eval(expr, env):
    """
    Evaluate Scheme expression expr in env. I fenv is None, simply
    returns expr as its value without futher evaluation.

    >>> expr = read_line("(+ 1 2)")
    >>> expr
    Pair('+', Pair(1, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    scnum(4)
    """

    while env is not None:

        if expr is None:
            raise SchemeError('Cannot evaluate an undefined expression.')

        # Evaluate atoms
        if scheme_symbolp(expr):
            expr, env = env.loopup(expr).get_actual_value(), None
        elif scheme_atomp(expr):
            env = None

        # All non-atomic expressions are lists
        elif not scheme_listp(expr):
            raise SchemeError('malformed list: {}'.format(str(expr)))
        else:
            first, rest = scheme_car(expr), scheme_cdr(expr)

            # Evaluate combinations
            if (scheme_symbolp(first) and first in SPECIAL_FORMS):
                if proper_tail_recursion:
                    expr, env = SPECIAL_FORMS[first](rest, env)
                else:
                    expr, env = SPECIAL_FORMS[first](rest, env)
                    expr, env = scheme_eval(expr, env), None
            else:
                procedure = scheme_eval(first, env)
                args = procedure.evaluate_arguments(rest, env)
                if proper_tail_recursion:
                    expr, env = procedure.apply(args, env)
                else:
                    expr, env = scheme_apply(procedure, args, env), None
    return expr

# Tail recursion
proper_tail_recursion = False


def scheme_apply(procedure, args, env):
    """
    Apply procedure to argument values args in env.

    Returns the resulting Scheme value.
    """
    expr, env = procedure.apply(args, env)
    return scheme_eval(expr, env)