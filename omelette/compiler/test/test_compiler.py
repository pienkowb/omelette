import unittest
from omelette.compiler.code import Code
from omelette.compiler.compiler import Compiler

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


if __name__ == "__main__":
    unittest.main()
