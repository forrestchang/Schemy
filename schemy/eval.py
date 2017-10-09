# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from schemy.types import Symbol, List, Number
from schemy.environments import Env, global_env


class Procedure(object):

    def __init__(self, parms, body, env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))


def eval(x, env=global_env):
    if isinstance(x, Symbol):   # 变量引用
        return env[x]
    elif not isinstance(x, List):   # 字面常量
        return x
    elif x[0] == 'quote':
        (_, exp) = x
        return exp
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'set!':    # 赋值
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'lambda':  # 过程
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:   # 过程调用
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)