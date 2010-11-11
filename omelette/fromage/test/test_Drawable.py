import unittest
from mock import Mock
from omelette.fromage.common import Drawable
from omelette.parser.uml import UMLObject

class UnitTest(unittest.TestCase):


    def setUp(self):
        self.mock = Mock()    

    def test_properties(self):
        (key, val) = ("stereotype", "Interface")
        instance = Drawable({key: val})
        self.assertEqual(val, instance[key])
        
    def test_operations(self):
        operations = ["+a()", "+b()", "-c() : int"]
        self.mock.operations.return_value = operations
        
        instance = Drawable(self.mock)
        self.assertEqual(operations, instance.operations())
        
    def test_attributes(self):
        attributes = ["+a", "+b", "-c : int"]
        self.mock.attributes.return_value = attributes
        
        instance = Drawable(self.mock)
        self.assertEqual(attributes, instance.attributes())
        
class IntegrationTest(unittest.TestCase):
    
    
    def test_properties(self):
        (key, val) = ("stereotype", "Interface")
        o = UMLObject()
        o[key] = val
        
        instance = Drawable(o)
        self.assertEqual(val, instance[key])
    
    def test_operations(self):
        ops = ["+b()","-a()"]
        o = UMLObject()
        [o.add_operation(op) for op in reversed(ops)]
        
        instance = Drawable(o)
        self.assertEqual(ops, instance.operations())
        
    def test_attributes(self):
        attrs = ["+b","-a"]
        o = UMLObject()
        [o.add_attribute(attr) for attr in reversed(attrs)]
        
        instance = Drawable(o)
        self.assertEqual(attrs, instance.attributes())
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()