import unittest
from omelette.compiler.code import Code
from omelette.compiler.compiler import Compiler
from omelette.compiler import logging

class CompilerTest(unittest.TestCase):

    def test_compile(self):
        instance = Compiler()
        code = Code("""base class
            class Student
                - name : String
                + learn()""")

        result = instance.compile(code)

        self.assertEquals(len(result), 2)
        self.assertEquals(len(result["Student"].attributes()), 1)
        self.assertEquals(len(result["Student"].operations()), 1)

    def test_compile_modified_object(self):
        instance = Compiler()
        code = Code("""base class
            class Student
            class University""")

        instance.compile(code)

        code.insert_line(2, "   - name : String")
        result = instance.compile(code)

        self.assertEquals(len(result), 1)
        self.assertEquals(len(result["Student"].attributes()), 1)

    def test_compile_library(self):
        instance = Compiler([Code("base class")])
        result = instance.compile(Code("class Student"))

        self.assertTrue("Student" in result)
        self.assertEquals(result["Student"].type, "class")

    def test_compile_prototype(self):
        instance = Compiler()
        code = Code("""prototype base class
            class Student""")

        result = instance.compile(code)

        self.assertEquals(len(result), 1)
        self.assertEquals(result.keys().pop(), "Student")


class CompilerIntegrationTest(unittest.TestCase):
    """Test for compilation errors"""

    def setUp(self):
        self.instance = Compiler()

        self.logger = logging.getLogger("compiler")
        self.logger.flush()

    def test_circular_reference(self):
        code = Code("objectname objectname")

        self.instance.compile(code)
        self.assertFalse(self.logger.is_empty(),
            "Logger should contain errors")

    def test_sophisticated_circular(self):
        code = Code("""a b
            b c
            c a""")

        self.instance.compile(code)
        self.assertFalse(self.logger.is_empty(),
            "Logger should contain errors")

    def test_bad_reference(self):
        """object refers to a non-existing object"""

        code = Code("""not-defined""")

        self.instance.compile(code)
        self.assertFalse(self.logger.is_empty(),
            "Logger should contain errors")


if __name__ == "__main__":
    unittest.main()
