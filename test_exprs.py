#!/usr/bin/env python3

import math
import sys

from grammar import Grammar

class TestParser(Grammar):
    def __init__(self, *args, **kwargs):
        self.count = 0
        self.fh = sys.stdout
        self.done = False
        self.happy = True
        self.results = { "ok": 0, "nok": 0, "todo": 0, "total": 0 }

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
        self.count_result(ok=ok, todo=todo)
        self.happy = self.happy and (ok or todo)

    def nok(self, *args, **kwargs):
        self.ok(*args, **kwargs, ok=False)

    def count_result(self, ok, todo):
        self.results["total"] += 1
        if todo:
            self.results["todo"] += 1
        else:
            self.results["ok" if ok else "nok"] += 1

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

    def closeEnough(self, expr, x_res, **kwargs):
        try:
            res = self.parse(expr)
        except Exception as e:
            self.nok(f"Compile '{expr}' failed:", **kwargs)
            self.diag(str(type(e)), str(e))
            return

        ok=math.isclose(res, x_res)
        self.ok(f"{expr}: {res} close enough to {x_res}", ok=ok)

    def exit(self):
        self.done_testing()
        res = self.results
        self.diag("-- done --", f"{res['total']} tests", f"{res['ok']} passed", f"{res['nok']} failed", f"{res['todo']} todo")
        self.diag("* success *" if self.happy else "> failure <")
        exit(0 if self.happy else 1)

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

def test_constants(parser):
    parser.typeis("2", int)
    parser.eval("2", 2)

    parser.typeis("π", float)
    parser.closeEnough("π*2", 6.28318)
    parser.typeis("pi", float)
    parser.closeEnough("pi*2", 6.28318)

    test_floats(parser)

def test_floats(parser):
    parser.typeis("2.0", float)
    parser.eval("2.0", 2)
    parser.typeis(".3", float)
    parser.closeEnough(".3", .3)
    parser.typeis("4.", float)
    parser.closeEnough("4.", 4)
    parser.typeis("4.3e2", float)
    parser.closeEnough("4.3e2", 430)
    parser.typeis("4.3e+2", float)
    parser.closeEnough("4.3e+2", 430)
    parser.typeis("4.3e+02", float)
    parser.closeEnough("4.3e+02", 430)
    parser.typeis("4.3e-2", float)
    parser.closeEnough("4.3e-2", 0.043)

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

def test_pow(parser):
    parser.eval("2^4", 16)
    parser.eval("2^2^3", 256)
    parser.eval("2^(2^3)", 256)
    parser.eval("((2^2)^3)", 64)

def test_funcall(parser):
    parser.eval("sqrt(4)", 2)
    parser.eval("sqrt(sqrt(81))", 3)
    parser.closeEnough("sin(π/2)", 1.0)
    parser.eval("gcd(24, 84)", 12)

test_assignment(parser)
test_constants(parser)
test_spaces(parser)
test_sum(parser)
test_precedence(parser)
test_assoc(parser)
test_paren(parser)
test_opsym(parser)
test_pow(parser)
test_funcall(parser)

parser.exit()
