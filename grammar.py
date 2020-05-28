#!/usr/bin/python3

import tatsu    # parser generator library
import pprint   # pretty-printer
import reprlib
from semantics import Semantics

class Grammar():

    def __init__(self, semantics=Semantics()):
        self.semantics = semantics

    def set_it(self, v):
        self.semantics.set_var("it", v)

    grammar = r'''
@@grammar::EVAL

start = expression $ ;

expression = varname:varname op:'='  val:expression
           | varname:varname op:':=:' val:expression
           | left:expression op:'+' right:term
           | left:expression op:'-' right:term
           | term
;

term =
         left:term op:'*' right:factor
       | left:term op:'×' right:factor
       | left:term op:'//' right:factor
       | left:term op:'/' right:factor
       | left:term op:'÷' right:factor
       | left:term op:'%' right:factor
       | factor
;

factor =
      left:base '**' right:factor
    | left:base '^' right:factor
    | base;

base = number | funcall | varval | compound_expression;

compound_expression = '(' @:expression ')' ;

funcall = varval '('   ','.{expression}+   ')' ;

number = fp | integer | pi;
integer = signed_digits ;
signed_digits = sign digits;
sign = '-' | '+' | ();
pi = 'π' | 'pi';
fp = [ integer_part:signed_digits ] '.' [ fraction_part:digits ] [ e_part:e_notation ];
e_notation = /[eE]/ @:signed_digits ;  # ('E' | 'e') does not work, because of nameguard
digits = /\d+/;

varval = varname ;
varname = /[A-Za-z]\w*/ ;

'''

    parser = tatsu.compile(grammar, name="eval")

    def parse(self, expr):
        return self.parser.parse(expr, semantics=self.semantics)
