# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
from .exception import SchemeError
from .types import intern, scheme_car, nil, scheme_cdr, SchemeValue


class Frame:
    """An environment binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with a Parent frame (that may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        else:
            s = sorted('{0}: {1}'.format(k, v) for k, v in self.bindings.items())
            return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def __eq__(self, other):
        return isinstance(other, Frame) and self.parent == other.parent

    def lookup(self, symbol):
        """Return the value bound to symbol. Erros if symbol is not found."""
        if type(symbol) is str:
            symbol = intern(symbol)
        if symbol in self.bindings:
            return self.bindings[symbol]
        elif self.parent:
            return Frame.lookup(self.parent, symbol)
        else:
            raise SchemeError('unknown identifier: {0}'.format(str(symbol)))

    def global_frame(self):
        """The global environment at the root of the parent chain."""
        e = self
        while e.parent is not None:
            e = e.parent
        return e

    def make_call_frame(self, formals, vals):
        """
        Return a new local frame whose parent is self, in which the symbol in the Scheme formal
        parameter list formals are bound to the Scheme values in the Scheme value list vals. Raise an
        error if too many or too few arguments are given.
        """
        frame = Frame(self)
        if len(formals) == len(vals):
            while formals != nil and vals != nil:
                frame.define(scheme_car(formals), scheme_car(vals))
                formals, vals = scheme_cdr(formals), scheme_cdr(vals)
        else:
            raise SchemeError('different number of formal parameters and args')


    def define(self, sym, val):
        """Define Scheme symbol sym to have value val in self."""
        assert isinstance(val, SchemeValue)
        if type(sym) is str:
            sym = intern(sym)
        self.bindings[sym] = val