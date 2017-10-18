# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)


class SchemeError(Exception):
    """Exception indication an error in a Scheme program."""


def bad_type(val, k, name):
    """Raise a SchemeError using 'argument K of NAME' to describe the offending value (VAL)."""
    msg = 'argument {} of {} has wrong type ({})'
    raise SchemeError(msg.format(k, name, type(val).__name__))


def check_type(val, predicate, k, name):
    """
    Returns VAL. Raises a SchemeError if not PREDICATE(VAL) using 'argument K of NAME'
    to describe the offending value.
    """
    if not predicate(val):
        bad_type(val, k, name)
    return val