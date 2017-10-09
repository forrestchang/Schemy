# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from .environments import Env, global_env
from .types import Symbol, List


class Procedure(object):

    def __init__(self, parms, body, env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return evaluate(self.body, Env(self.parms, args, self.env))


def evaluate(x, env=global_env):
    if isinstance(x, Symbol):   # 变量引用
        return env.find(x)[x]
    elif not isinstance(x, List):   # 字面常量
        return x
    elif x[0] == 'quote':
        (_, exp) = x
        return exp
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if evaluate(test, env) else alt)
        return evaluate(exp, env)
    elif x[0] == 'define':
        (_, var, exp) = x
        env[var] = evaluate(exp, env)
    elif x[0] == 'set!':    # 赋值
        (_, var, exp) = x
        env.find(var)[var] = evaluate(exp, env)
    elif x[0] == 'lambda':  # 过程
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:   # 过程调用
        proc = evaluate(x[0], env)
        args = [evaluate(arg, env) for arg in x[1:]]
        return proc(*args)