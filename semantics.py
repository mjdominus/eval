
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
  def expression(self, ast):
    debug("** expression: ", ast)
    if isinstance(ast, AST):
      if ast.op == '+':
        return ast.left + ast.right
      elif ast.op == '-':
        return ast.left - ast.right
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

  
        

  
