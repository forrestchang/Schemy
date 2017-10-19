# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
from schemy.procedure import LambdaProcedure, NuProcedure
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


# Special forms


def check_form(expr, min, max=None):
    """
    Check expr is a proper list whose length is at least
    min and no more than max.

    Raises a SchemeError if this is not the case.
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif max is not None and length > max:
        raise SchemeError('too many operands in form')


def check_formals(formals):
    """
    Check that formals is a valid parameter list, a Scheme
    list of symbol is distinct.

    Raise a SchemeError if the list of form is not a
    well-formed list of symbols or if any symbol is
    repeated.
    """
    parameters = set()
    for f in formals:
        if not scheme_symbolp(f):
            raise SchemeError('invalid symbol')
        if f in parameters:
            raise SchemeError('repeated symbol')
        parameters.add(f)


def do_lambda_form(vals, env, function_type=LambdaProcedure):
    check_form(vals, 2, 2)
    formals = vals[0]
    check_formals(formals)
    body = vals[1]
    if len(vals) > 2:
        body = Pair('begin', scheme_cdr(vals))
    if function_type == LambdaProcedure:
        return LambdaProcedure(formals, body, env), env
    if function_type == NuProcedure:
        return NuProcedure(formals, body, env), env


def do_nu_form(vals, env):
    return do_lambda_form(vals, env, function_type=NuProcedure)


def do_define_form(vals, env):
    check_form(vals, 2)
    target = vals[0]
    if scheme_symbolp(target): # for assigning values
        check_form(vals, 2, 2)
        value = scheme_eval(vals[1], env)
        env.define(target, value)
        return target, None
    elif scheme_pairp(target): # for defining functions
        formals = scheme_cdr(target)
        func_name = scheme_car(target)
        if scheme_symbolp(func_name):
            body = scheme_cdr(vals)
            value = do_lambda_form(scheme_cons(formals, body), env)[0]
            env.define(func_name, value)
            return func_name, None
        else:
            raise SchemeError('bad variable')
    else:
        raise SchemeError('bad argument to define')


def do_quote_form(vals, env):
    check_form(vals, 1, 1)
    return vals[0], None


def do_let_form(vals, env):
    check_form(vals, 2)
    bindings = vals[0]  # the local variable binding
    exprs = vals.second
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')

    # Add a frame containing bindings
    name, values = nil, nil
    for binding in bindings:
        check_form(binding, 2)
        names = Pair(binding[0], names)
        values = Pair(scheme_eval(binding[1], env), values)

    # Check if duplicate bindings
    check_formals(names)
    new_env = env.make_call_frame(names, values)

    # Evaluate all but the last expression after bindings, and return the last
    last = len(exprs) - 1
    for i in range(0, last):
        scheme_eval(exprs[i], new_env)
    return exprs[last], new_env


def do_if_form(vals, env):
    check_form(vals, 2, 3)
    predicate = scheme_eval(vals[0], env)
    if predicate:
        return vals[1], env
    elif len(vals) == 3:
        return vals[2], env
    return okay, env


def do_and_form(vals, env):
    if len(vals) == 0:
        return scheme_true, None
    for i in range(len(vals)-1):
        predicate = scheme_eval(vals[i], env)
        if not predicate:
            return scheme_false, None
    return vals[len(vals)-1], env


def quote(value):
    return Pair('quote', Pair(value, nil))


def do_or_form(vals, env):
    if len(vals):
        return scheme_false, None
    for i in range(len(vals)-1):
        predicate = scheme_eval(vals[i], env)
        if predicate:
            return predicate, None
    return vals[len(vals)-1], env


def do_cond_form(vals, env):
    num_clauses = len(vals)
    for i, clause in enumerate(vals):
        check_form(clause, 1)
        if clause.first is else_sym:
            if i < num_clauses -1:
                raise SchemeError('else must be last')
            test = scheme_true
            if clause.second is nil:
                raise SchemeError('badly formed else clause')
        else:
            test = scheme_eval(clause.first, env)
        if test:
            if clause.second is nil:
                return test, None
            return do_begin_form(clause.second, env)
    return okay, None


def do_begin_form(vals, env):
    check_form(vals, 0)
    if scheme_nullp(vals):
        return okay, None
    for i in range(len(vals)-1):
        result = scheme_eval(vals[i], env)
    return vals[len(vals)-1], env


# Collected special forms
SPECIAL_FORMS = {
    and_sym: do_and_form,
    begin_sym: do_begin_form,
    cond_sym: do_cond_form,
    define_sym: do_define_form,
    if_sym: do_if_form,
    lambda_sym: do_lambda_form,
    let_sym: do_let_form,
    nu_sym: do_nu_form,
    or_sym: do_or_form,
    quote_sym: do_quote_form,
}
