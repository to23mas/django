from django.test import TestCase
from ..validator import check_ast

class TestASTChecker(TestCase):
    def test_safe_function(self):
        """Test safe function definition"""
        code = """
def triple(x):
    return x * 3
"""
        self.assertTrue(check_ast(code))

    def test_safe_with_multiple_functions(self):
        """Test multiple safe functions"""
        code = """
def triple(x):
    return x * 3

def double(x):
    return x * 2
"""
        self.assertTrue(check_ast(code))

    def test_dangerous_import(self):
        """Test dangerous import statements"""
        dangerous_imports = [
            "import os",
            "from sys import exit",
            "import subprocess as sub",
            "from os import system",
        ]
        for code in dangerous_imports:
            self.assertFalse(check_ast(code), f"Should detect dangerous import: {code}")

    def test_dangerous_builtins(self):
        """Test dangerous built-in function calls"""
        dangerous_codes = [
            "eval('2 + 2')",
            "exec('print(1)')",
            "open('file.txt')",
            "__import__('os')",
            "globals()",
            "locals()",
        ]
        for code in dangerous_codes:
            self.assertFalse(check_ast(code), f"Should detect dangerous builtin: {code}")

    def test_dangerous_attributes(self):
        """Test dangerous attribute access"""
        dangerous_codes = [
            "obj.system('ls')",
            "x.subprocess.call(['ls'])",
            "f.write('data')",
            "f.read()",
        ]
        for code in dangerous_codes:
            self.assertFalse(check_ast(code), f"Should detect dangerous attribute: {code}")

    def test_safe_operations(self):
        """Test various safe operations"""
        safe_codes = [
            "x = 1 + 2 * 3",
            "'hello' + ' world'",
            "[1, 2, 3].append(4)",
            "{'a': 1, 'b': 2}",
            """
if x > 0:
    return True
else:
    return False
""",
            """
for i in range(10):
    print(i)
""",
        ]
        for code in safe_codes:
            self.assertTrue(check_ast(code), f"Should allow safe code: {code}")

    def test_syntax_error(self):
        """Test invalid Python syntax"""
        invalid_codes = [
            "def missing_colon(x)",
            "for i in range(10)",
            "if x >",
        ]
        for code in invalid_codes:
            self.assertFalse(check_ast(code), f"Should reject invalid syntax: {code}")

    def test_nested_dangerous_calls(self):
        """Test nested dangerous operations"""
        dangerous_codes = [
            """
def wrapper():
    return eval('2 + 2')
""",
            """
def innocent():
    x = open('file.txt')
    return x.read()
""",
        ]
        for code in dangerous_codes:
            self.assertFalse(check_ast(code), f"Should detect nested dangerous operations: {code}")
