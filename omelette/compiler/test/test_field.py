from mock import Mock
from omelette.compiler.uml import Operation, Attribute
import unittest

class FieldStrTest(unittest.TestCase):
    """Tests for __str__ in both operation and attribute classes"""

    def test_operation(self):
        o = Operation("+", "asd", 0, [("a", "1"), ("b", "2")], "int")
        self.assertEquals(str(o), "+ asd(a : 1, b : 2) : int")
        self.assertEquals(o.is_static, 0)

    def test_operation_minimal(self):
        o = Operation("#", "ASD")
        self.assertEquals(str(o), "# ASD()")
        self.assertFalse(o.is_static)
        
        
    def test_operation_no_params(self):
        """
        test behavior of parameter formating methods when 
        no parameters are given
        """ 
        
        o = Operation("+", "asd", is_static=1)
        self.assertEqual(o.is_static, 1)
        
    def test_operation_no_types(self):
        """
        test behavior of parameter formating methods when 
        parameter types weren't given
        """
        
        o = Operation("+", "asd", 0, [("a", "int"), ("b", None)], "int")
        self.assertEquals(str(o), "+ asd(a : int, b) : int")
        
    def test_operation_no_return_type(self):
        """test behavior of __str__ when no return type is given"""
        
        o = Operation("+", "asd", 0, [("a", "int"), ("b", None)], None)
        self.assertEquals(str(o), "+ asd(a : int, b)")

    def test_operation_eq(self):
        instance = Operation("+", "asd", 0, [("a", "1"), ("b", "2")], "int")
        same = Operation("+", "asd", 0, [("a", "1"), ("b", "2")], "int")
        different = Operation("-", "asd", 0, [("a", "1"), ("b", "2")], "int")
        
        self.assertEqual(instance, same)
        self.assertNotEqual(instance, different)
        
    def test_attribute(self):
        a = Attribute("+", "asd", 1, "int", "42")
        self.assertEquals(str(a), "+ asd : int = 42")
        self.assertTrue(a.is_static)
        
    def test_attribute_minimal(self):
        a = Attribute("#", "ASD")
        self.assertEquals(str(a), "# ASD")
        self.assertFalse(a.is_static)
        
    def test_attribute_no_type(self):
        a = Attribute("+", "asd", 1, None, "42")
        self.assertEquals(str(a), "+ asd = 42")
        
    def test_attribute_no_default(self):
        a = Attribute("+", "asd", 1, "int")
        self.assertEquals(str(a), "+ asd : int")
        
    def test_attribute_eq(self):
        instance = Attribute("+", "asd", 1, "int", "42")
        same = Attribute("+", "asd", 1, "int", "42")
        different = Attribute("+", "asd", 1, "float", "42.0")
        
        self.assertEqual(instance, same)
        self.assertNotEqual(instance, different)
        
if __name__ == "__main__":
    unittest.main()

