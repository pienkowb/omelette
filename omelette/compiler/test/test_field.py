from mock import Mock
from omelette.compiler.uml import Operation, Attribute
import unittest

class TestField(unittest.TestCase):

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
        
    def test_operation_eq(self):
        instance = Operation(0, "+", "asd", [("a", "1"), ("b", "2")], "int")
        same = Operation(0, "+", "asd", [("a", "1"), ("b", "2")], "int")
        different = Operation(0, "-", "asd", [("a", "1"), ("b", "2")], "int")
        
        self.assertEqual(instance, same)
        self.assertNotEqual(instance, different)
        
    def test_attribute(self):
        a = Attribute(1, "+", "asd", "int", "42")
        self.assertEquals(str(a), "+asd : int = 42")
        self.assertTrue(a.is_static)
        
    def test_attribute_minimal(self):
        a = Attribute(0, "#", "ASD", None, None)
        self.assertEquals(str(a), "#ASD")
        self.assertFalse(a.is_static)
        
    def test_attribute_no_type(self):
        a = Attribute(1, "+", "asd", None, "42")
        self.assertEquals(str(a), "+asd = 42")
        
    def test_attribute_no_default(self):
        a = Attribute(1, "+", "asd", "int", None)
        self.assertEquals(str(a), "+asd : int")
        
    def test_attribute_eq(self):
        instance = Attribute(1, "+", "asd", "int", "42")
        same = Attribute(1, "+", "asd", "int", "42")
        different = Attribute(1, "+", "asd", "float", "42.0")
        
        self.assertEqual(instance, same)
        self.assertNotEqual(instance, different)
        
if __name__ == "__main__":
    unittest.main()

