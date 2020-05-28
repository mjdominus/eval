

import os
from pprint import pprint
from tatsu.ast import AST
import eval_builtins

def s(x): str(x)

if int(os.environ.get('DEBUG', 0)):
  def debug(*strings):
    print("".join(map(str, strings)))
else:
  def debug(*strings):
    pass

class Semantics:
  def __init__(self):
    self.vars = eval_builtins.builtin_funcs

  def expression(self, ast):
    debug("** expression: ", ast)
    if isinstance(ast, AST):
      if ast.op == '+':
        return ast.left + ast.right
      elif ast.op == '-':
        return ast.left - ast.right
      elif ast.op == '=':
        self.set_var(ast.varname, ast.val)
        return ast.val
      elif ast.op == ':=:':
        old = self.get_var(ast.varname)
        self.set_var(ast.varname, ast.val)
        return old
      else:
        raise Exception("WTF", ast.op)
    else:
      return ast

  def term(self, ast):
    debug("** term: ", ast)
    if isinstance(ast, AST):
      if ast.op == '*' or ast.op == '×':
        return ast.left * ast.right
      elif ast.op == '/' or ast.op == '÷':
        return ast.left / ast.right
      elif ast.op == '%':
        return ast.left % ast.right
      elif ast.op == '//':
        return ast.left // ast.right
      else:
        raise Exception("WTF", ast.op)
    else:
      return ast

  def funcall(self, ast):
    args = ast[2]
    return ast[0](*args)

  def factor(self, ast):
    if isinstance(ast, AST):
      return ast.left ** ast.right
    else:
      return ast

  # def digits(self, ast):
  #   from sys import stderr
  #   print("digits", ast, f"({type(ast)})", file=stderr)
  #   return float(ast)

  def sign(self, ast):
    if ast is None or ast == '+':
      return 1
    elif ast == '-':
      return -1
    else:
      raise Exception(f"Unknown numeric sign '{ast}'")

  def signed_digits(self, ast):
    sign, digits = ast
    return sign * int(digits)

  def integer(self, digits):
    return int(digits)

  def fp(self, ast):
    # Yuck
    return float(str(ast.integer_part) + "." + ast.fraction_part)

  def pi(self, ast):
    return 3.14159

  def varval(self, name):
    return self.get_var(name)

  def get_var(self, varname):
    return self.vars[varname]

  def set_var(self, var, val):
    assert isinstance(var, str)
    self.vars[var] = val
