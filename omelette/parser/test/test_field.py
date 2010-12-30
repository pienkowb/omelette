from mock import Mock
from omelette.parser.uml import Operation, Attribute
import unittest

class Test(unittest.TestCase):

    def test_operation(self):
        o = Operation(0, "+", "asd", [("a", "1"), ("b", "2")], "int")
        self.assertEquals(str(o), "+asd(a : 1, b : 2) : int")
        self.assertEquals(o.is_static, 0)
        
    def test_operation_no_params(self):
        """
        test behavior of parameter formating methods when 
        no parameters are given
        """ 
        o = Operation(1, "+", "asd", [], "int")
        self.assertEqual(str(o), "+asd() : int")
        self.assertEqual(o.is_static, 1)
        
    def test_operation_no_types(self):
        """
        test behavior of parameter formating methods when 
        parameter types weren't given
        """
        o = Operation(0, "+", "asd", [("a", "int"), ("b", None)], "int")
        self.assertEquals(str(o), "+asd(a : int, b) : int")
        
    def test_operation_no_return_type(self):
        """test behavior of __str__ when no return type is given"""
        o = Operation(0, "+", "asd", [("a", "int"), ("b", None)], None)
        self.assertEquals(str(o), "+asd(a : int, b)")
        
if __name__ == "__main__":
    unittest.main()

