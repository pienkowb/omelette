import unittest
from omelette.parser.uml import *

class Test(unittest.TestCase):


    def test_operation(self):
        instance = UMLObject()
        operation = "+operation()"
        
        instance.add_operation(operation)
        result = instance.operations()[0]
        
        self.assertEquals(result, operation)
        
    def test_attribute(self):
        instance = UMLObject()
        attribute = "+attribute"
        
        instance.add_attribute(attribute)
        result = instance.attributes()[0]
        
        self.assertEquals(attribute, result)
        
    def test_sorting(self):
        instance = UMLObject()
        data = ["+a", "-z", "#z", "#c", "-b", "+c"]
        
        [instance.add_attribute(attr) for attr in data]
        [instance.add_operation(op+"()") for op in data]
        
        attrs = instance.attributes()
        ops = instance.operations()
        
        self.assertEquals(attrs, ["+a", "+c", "#c","#z","-b","-z"])
        self.assertEquals(ops, ["+a()", "+c()", "#c()","#z()","-b()","-z()"])
        
    def test_property(self):
        property   = "stereotype"
        value       = "Interface"
        instance = UMLObject()
        
        instance[property] = value
        
        self.assertEquals(instance[property], value)
        


if __name__ == "__main__":
    unittest.main()
