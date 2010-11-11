import unittest
import random
from mock import Mock
from omelette.fromage.common import *
from omelette.parser.uml import UMLObject

class UnitTest(unittest.TestCase):


    def setUp(self):
        self.mock = Mock()
        self.classes = [Drawable, DrawableNode, DrawableEdge]

    def test_properties(self):
        for class_ in self.classes:
            (key, val) = ("stereotype", "Interface")
            instance = class_({key: val})
            self.assertEqual(val, instance[key])
        
    def test_operations(self):
        for class_ in self.classes:
            operations = ["+a()", "+b()", "-c() : int"]
            self.mock.operations.return_value = operations
            
            instance = class_(self.mock)
            self.assertEqual(operations, instance.operations())
        
    def test_attributes(self):
        for class_ in self.classes:
            attributes = ["+a", "+b", "-c : int"]
            self.mock.attributes.return_value = attributes
            
            instance = class_(self.mock)
            self.assertEqual(attributes, instance.attributes())
    
    def test_has_anchors(self):
        instance = DrawableEdge(None)
        self.assertTrue(hasattr(instance, "source_anchor"))
        self.assertTrue(hasattr(instance, "target_anchor"))
        
    def test_has_position(self):
        instance = DrawableNode(None)
        pos = (3, 5)
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
        ops = ["+b()", "-a()"]
        o = UMLObject()
        [o.add_operation(op) for op in reversed(ops)]
        
        instance = Drawable(o)
        self.assertEqual(ops, instance.operations())
        
    def test_attributes(self):
        attrs = ["+b", "-a"]
        o = UMLObject()
        [o.add_attribute(attr) for attr in reversed(attrs)]
        
        instance = Drawable(o)
        self.assertEqual(attrs, instance.attributes())
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
