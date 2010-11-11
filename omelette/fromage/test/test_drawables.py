import unittest
import random
from mock import Mock
from omelette.fromage.common import *
from omelette.parser.uml import UMLObject

class UnitTest(unittest.TestCase):


    def setUp(self):
        self.mock = Mock()
        self.class_ = random.choice([Drawable, DrawableNode, DrawableEdge])

    def test_properties(self):
        "Caution: If this test behaves randomly it's because tested class is choosen randomly!"
        (key, val) = ("stereotype", "Interface")
        instance = self.class_({key: val})
        self.assertEqual(val, instance[key])
        
    def test_operations(self):
        "Caution: If this test behaves randomly it's because tested class is choosen randomly!"
        operations = ["+a()", "+b()", "-c() : int"]
        self.mock.operations.return_value = operations
        
        instance = self.class_(self.mock)
        self.assertEqual(operations, instance.operations())
        
    def test_attributes(self):
        "Caution: If this test behaves randomly it's because tested class is choosen randomly!"
        attributes = ["+a", "+b", "-c : int"]
        self.mock.attributes.return_value = attributes
        
        instance = self.class_(self.mock)
        self.assertEqual(attributes, instance.attributes())
    
    def test_has_anchors(self):
        instance = DrawableEdge(None)
        self.assertTrue(hasattr(instance,"source_anchor"))
        self.assertTrue(hasattr(instance,"target_anchor"))
        
    def test_has_position(self):
        instance = DrawableNode(None)
        pos = (3,5)
        instance.set_position(pos)
        
        self.assertEqual(pos, instance.get_position())
        
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