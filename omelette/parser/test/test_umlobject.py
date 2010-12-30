import unittest
from omelette.parser.uml import UMLObject
from mock import Mock,MagicMock

class Test(unittest.TestCase):

    def test_operation(self):
        instance = UMLObject()
        operation = MagicMock()
        operation.__str__.return_value = "+operation(a : int, b : int) : int"
        
        instance.add_operation(operation)
        result = instance.operations()[0]
        
        self.assertEquals(result, "+operation(a : int, b : int) : int")
        
    def test_attribute(self):
        instance = UMLObject()
        attribute = MagicMock()
        attribute.__str__.return_value = "+attribute : int = 3"
        
        instance.add_attribute(attribute)
        result = instance.attributes()[0]
        
        self.assertEquals(result, "+attribute : int = 3")
        
    def test_property(self):
        property   = "stereotype"
        value      = "Interface"
        instance = UMLObject()
        
        instance[property] = value
        
        self.assertEquals(value, instance[property])
        
    def test_root_property(self):
        instance = UMLObject()
        m = Mock()
        
        instance.root = m
        self.assertEqual(m, instance.root)
        

if __name__ == "__main__":
    unittest.main()

