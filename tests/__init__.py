import unittest
from io import StringIO
from contextlib import redirect_stdout

import constable

class TestDebugDecorator(unittest.TestCase):
    def test_decorator_does_not_change_behavior(self):
        @constable.trace('a', 'b', 'c', verbose=False)
        def complex_function(a, b, c):
            d = a + b
            e = b * c
            f = a - c
            return d, e, f
        
        with redirect_stdout(StringIO()):
            self.assertEqual(complex_function(1, 2, 3), (3, 6, -2))

    def test_decorator_output_count(self):
        @constable.trace('a', 'b', verbose=True)
        def add(a, b):
            a = a + 1
            b: int = b + 1
            a += 1
            return a + b

        f = StringIO()
        with redirect_stdout(f):
            add(1, 2)
        output = f.getvalue()
        num_lines = len(output.split('\n')) - 1 
        self.assertEqual(num_lines, 22)

    def test_decorator_datatype_check(self):
        @constable.trace('a', verbose=True, show_warnings=True)
        def datatype_change_function(a):
            a = a + 1
            a = []
            a = [1,2,3]
            a = {}
            a = (1,2)
            a = ()
            a = {1,2}
            a = "Hi"
            a = 3.0
            return a

        f = StringIO()
        with redirect_stdout(f):
            datatype_change_function(1)
        output = f.getvalue()
        lines = output.split('\n')
        count = sum('warning' in line.lower() for line in lines)

        self.assertEqual(count, 7)
        

    def test_decorator_multiple_datatype_check(self):
        @constable.trace('a', 'b', verbose=True, show_warnings=True)
        def datatype_change_function(a, b):
            a = []
            a = [1,2,3]
            a = {}
            b = (1,2)
            b = ()
            b = {1,2}
            b = "Hi"
            b = 3.0
            return a, b

        f = StringIO()
        with redirect_stdout(f):
            datatype_change_function(1,2)
        output = f.getvalue()
        lines = output.split('\n')
        
        count = sum('warning' in line.lower() for line in lines)
        
        self.assertEqual(count, 5)