#!/usr/bin/python3
import math
import pytest
from grammar import Grammar

class TestParser(Grammar):
    def tryit(self, expr, x_res):
        assert self.parse(expr) == x_res

    def closeEnough(self, expr, x_res):
        assert math.isclose(self.parse(expr), x_res)

@pytest.fixture
def parser():
     return TestParser()

def test_assignment(parser):
    parser.tryit("x = 17", 17)
    parser.tryit("x", 17)
    parser.tryit("x = y = 3", 3)
    parser.tryit("x", 3)
    parser.tryit("y", 3)
    parser.tryit("y = 4", 4)
    parser.tryit("x :=: y :=: 5", 3)
    parser.tryit("x", 4)
    parser.tryit("y", 5)

def test_spaces(parser):
    parser.tryit("1+1", 2)
    parser.tryit("1 + 1", 2)
    parser.tryit("  1 +1  ", 2)
    parser.tryit(" 1+   1", 2)

def test_sum(parser):
    parser.tryit("1+1", 2)

def test_precedence(parser):
    parser.tryit("3+5*4", 23)
    parser.tryit("3*5+4", 19)
    parser.tryit("3*(5+4)", 27)

def test_assoc(parser):
    parser.tryit("8-(4-3)", 7)
    parser.tryit("(8-4)-3", 1)
    parser.tryit("100/5/2", 10)
    parser.tryit("8-4-3", 1)

def test_paren(parser):
    parser.tryit("3", 3)
    parser.tryit("(3)", 3)
    parser.tryit("((3))", 3)

def test_opsym(parser):
    parser.tryit("8*4", 32)
    parser.tryit("8×4", 32)
    parser.tryit("8/4", 2)
    parser.tryit("8÷4", 2)

def test_pi(parser):
    parser.closeEnough("π*2", 6.28318)
    parser.closeEnough("pi*2", 6.28318)

def test_pow(parser):
    parser.tryit("2^4", 16)
    parser.tryit("2^2^3", 256)
    parser.tryit("2^(2^3)", 256)
    parser.tryit("((2^2)^3)", 64)

def test_funcall(parser):
    parser.tryit("sqrt(4)", 2)
    parser.tryit("sqrt(sqrt(81))", 3)
