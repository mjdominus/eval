
import os
from tatsu.ast import AST
from pprint import pprint

def s(x): str(x)

if int(os.environ.get('DEBUG', 0)):
  def debug(*strings):
    print("".join(map(str, strings)))
else:
  def debug(*strings):
    pass

class Semantics:
  def __init__(self):
    self.vars = {}

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
      else:
        raise Exception("WTF", ast.op)
    else:
      return ast

  def compound_expression(self, ast):
    return ast[1]

  def factor(self, ast):
    if isinstance(ast, AST):
      return ast.left ** ast.right
    else:
      return ast

  def number(self, ast):
    return float(ast)

  def pi(self, ast):
    return 3.14159

  def varval(self, name):
    return self.get_var(name)

  def get_var(self, varname):
    return self.vars[varname]

  def set_var(self, var, val):
    assert isinstance(var, str)
    self.vars[var] = val
