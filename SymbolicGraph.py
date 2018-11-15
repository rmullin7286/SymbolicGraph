from pyeda.inter import *
from functools import reduce


def to_expr(li, varname):
    bdd = bddvars(varname, 5)
    varlist = [var if val else ~var for var, val in zip(bdd, li)]
    return reduce(lambda a, b: a & b, varlist)


def bool_array(num):
    return [bool(num >> n & 1) for n in range(4, -1, -1)]


def create_bool_formula(i, j):
    x = to_expr(bool_array(i), 'x')
    y = to_expr(bool_array(j), 'y')

    return x & y


def compose(r1, r2):
    Z = bddvars('z', 5)
    Y = bddvars('y', 5)
    X = bddvars('x', 5)
    for i in range(0, 4):
        r1 = r1.compose({Y[i]: Z[i]})
        r2 = r2.compose({X[i]: Z[i]})
    return (r1 & r2).smoothing(Z)


S = range(0, 32)
G = [(i, j) for i in S for j in S if (i+3) % 32 == j % 32 or (i+7) % 32 == j % 32]
exprs = [create_bool_formula(i, j) for i, j in G]
F = reduce(lambda a, b: a | b, exprs)

H = F
while True:
    Hp = H
    H = Hp | compose(Hp, F)
    if H.equivalent(Hp):
        break

S_bool = [bool_array(i) for i in S]

X = bddvars('x', 5)
Y = bddvars('y', 5)

P = Not(H).smoothing().equivalent(False)

print("P is true for all nodes i, j" if P else "P is false for all nodes i, j")







