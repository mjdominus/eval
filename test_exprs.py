#!/usr/bin/env python3

import math
import sys

from grammar import Grammar

class TestParser(Grammar):
    def __init__(self, *args, **kwargs):
        self.count = 0
        self.fh = sys.stdout
        self.done = False
        super().__init__(*args, **kwargs)

    def done_testing(self):
        self.done = True

    def ok(self, *msgs, ok=True, todo=None):
        self.count += 1
        msgs = list(msgs)

        if len(msgs) > 0:
            msg = "- " + "".join(msgs)
        else:
            msg = ""

        if todo:
            if todo is True:
                msg += " # TODO"
            else:
                msg += " # TODO " + str(todo)

        print("ok" if ok else "not ok", self.count, msg, file=self.fh)

    def nok(self, *args, **kwargs):
        self.ok(*args, **kwargs, ok=False)

    def eval(self, expr, x_res, **kwargs):
        try:
            res = self.parse(expr)
        except Exception as e:
            self.nok(f"Compile '{expr}' failed:", **kwargs)
            self.diag(str(type(e)), str(e))
            return

        self._is(x_res, res, expr, **kwargs)

    def _is(self, x, a, *msgs, **kwargs):
        ok = x==a
        self.ok(*msgs, **kwargs, ok=ok)
        if not ok:
            self.diag("expected: " + str(x))
            self.diag("got:      " + str(a))

    def diag(self, *msgs):
        for msg in msgs:
            print("#", msg.replace("\n", "\n# "), file=self.fh)

    def typeis(self, expr, x_type, **kwargs):
        try:
            a_type = type(self.parse(expr))
        except Exception as e:
            self.nok(f"Compile '{expr}' failed:", **kwargs)
            self.diag(str(type(e)), str(e))
            return
        self._is(x_type, a_type, f"type of '{expr}'", **kwargs)

    def closeEnough(self, expr, x_res):
        assert math.isclose(self.parse(expr), x_res)

    def __del__(self):
        if self.done:
            print(f"1..{self.count}", file=self.fh)
        else:
            self.nok("done_testing not called")

parser = TestParser()

def test_assignment(parser):
    parser.eval("x = 17", 17)
    parser.eval("x", 17)
    parser.eval("x = y = 3", 3)
    parser.eval("x", 3)
    parser.eval("y", 3)
    parser.eval("y = 4", 4)
    parser.eval("x :=: y :=: 5", 3)
    parser.eval("x", 4)
    parser.eval("y", 5)
    parser.eval("2", 2)

def test_constants(parser):
    parser.typeis("2", int)
    parser.typeis("2.0", float)
    parser.typeis("π", float)
    parser.typeis(".3", float, todo="leading integer required for now")

def test_spaces(parser):
    parser.eval("1+1", 2)
    parser.eval("1 + 1", 2)
    parser.eval("  1 +1  ", 2)
    parser.eval(" 1+   1", 2)

def test_sum(parser):
    parser.eval("1+1", 2)

def test_precedence(parser):
    parser.eval("3+5*4", 23)
    parser.eval("3*5+4", 19)
    parser.eval("3*(5+4)", 27)

def test_assoc(parser):
    parser.eval("8-(4-3)", 7)
    parser.eval("(8-4)-3", 1)
    parser.eval("100/5/2", 10)
    parser.eval("8-4-3", 1)

def test_paren(parser):
    parser.eval("3", 3)
    parser.eval("(3)", 3)
    parser.eval("((3))", 3)

def test_opsym(parser):
    parser.eval("8*4", 32)
    parser.eval("8×4", 32)
    parser.eval("8/4", 2)
    parser.eval("8÷4", 2)

def test_pi(parser):
    parser.closeEnough("π*2", 6.28318)
    parser.closeEnough("pi*2", 6.28318)

def test_pow(parser):
    parser.eval("2^4", 16)
    parser.eval("2^2^3", 256)
    parser.eval("2^(2^3)", 256)
    parser.eval("((2^2)^3)", 64)

def test_funcall(parser):
    parser.eval("sqrt(4)", 2)
    parser.eval("sqrt(sqrt(81))", 3)

test_assignment(parser)
test_constants(parser)
test_spaces(parser)
test_sum(parser)
test_precedence(parser)
test_assoc(parser)
test_paren(parser)
test_opsym(parser)
test_pi(parser)
test_pow(parser)
test_funcall(parser)
parser.done_testing()
