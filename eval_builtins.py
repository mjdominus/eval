import math

builtin_funcs = {}
for n in dir(math):
    if not n.startswith("__"):
        builtin_funcs[n] = getattr(math, n)
