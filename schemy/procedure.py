# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
from schemy.eval import proper_tail_recursion, scheme_eval, nil
from schemy.exception import SchemeError
from schemy.types import SchemeValue


class Procedure(SchemeValue):
    """The superclass of all kinds of procedure in Scheme."""

    def evaluate_arguments(self, arg_list, env):
        """
        Evaluate the expression in arg_list in env to produce arguments for this procedure.
        Default definition for procedures.
        """
        from .eval import scheme_eval
        return arg_list.map(lambda operand: scheme_eval(operand, env))


class PrimitiveProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, func, use_env=False):
        self.func= func
        self.use_env = use_env

    def __str__(self):
        return '#[primitive]'

    def __repr__(self):
        return 'PrimitiveProcedure({})'.format(str(self))

    def apply(self, args, env):
        """
        Apply a primitive procedure to args in env.

        Returns a pair (val, None), where val is the resulting value.
        """
        try:
            args_list = list(args)
            if self.use_env:
                args_list.append(env)
            val = self.func(*args_list)
        except TypeError as e:
            raise SchemeError(e)
        return val, None


class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or the complex define form."""

    def __init__(self, formals, body, env=None):
        self.formals = formals
        self.body = body
        self.env = env

    def _symbol(self):
        return 'lambda'

    def __str__(self):
        return '({0} {1} {2})'.format(self._symbol(), str(self.formals), str(self.body))

    def __repr__(self):
        args = (self.formals, self.body, self.env)
        return '{}Procedure({}, {}, {})'.format(
            self._symbol().capitalize(),
            *(repr(a) for a in args)
        )

    def __eq__(self, other):
        return type(other) is type(self) and \
            self.formals == other.formals and \
            self.body == other.body and \
            self.env == other.env

    def apply(self, args, env):
        if proper_tail_recursion:
            new_env = self.env.make_call_frame(self.formals, args)
            return self.body, new_env
        else:
            new_env = self.env.make_call_frame(self.formals, args)
            return scheme_eval(self.body, new_env), None


class NuProcedure(LambdaProcedure):
    """A procedure whose parameters are to be passed by name."""

    def _symbol(self):
        return 'nu'

    def evaluate_arguments(self, arg_list, env):
        return arg_list.map(lambda operand: Thunk(nil, operand, env))


class Thunk(LambdaProcedure):
    """A by-name value that is to be called as a parameterless function when its value is fetched to be used."""

    def get_actual_value(self):
        return scheme_eval(self.body, self.env)
