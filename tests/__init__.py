import unittest
from io import StringIO
from contextlib import redirect_stdout

import ast_debug

class TestDebugDecorator(unittest.TestCase):
    def test_debug_decorator_does_not_change_behavior(self):
        @ast_debug.trace(variables=['a', 'b', 'c'])
        def complex_function(a, b, c):
            d = a + b
            e = b * c
            f = a - c
            return d, e, f
        
        with redirect_stdout(StringIO()):
            self.assertEqual(complex_function(1, 2, 3), (3, 6, -2))

    def test_debug_decorator_output_count(self):
        @ast_debug.trace(variables=['a', 'b'])
        def add(a, b):
            a = a + 1
            b = b + 1
            return a + b

        f = StringIO()
        with redirect_stdout(f):
            add(1, 2)
        output = f.getvalue()
        num_lines = len(output.split('\n')) - 1 
        self.assertEqual(num_lines, 3)