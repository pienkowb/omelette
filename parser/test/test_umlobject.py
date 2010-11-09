import unittest
from omelette.parser.util import *

class Test(unittest.TestCase):


    def test_method(self):
        instance = UMLObject()
        method = "+method()"
        
        instance.add_method(method)
        result = instance.methods()[0]
        
        self.assertEquals(result, method)
        
    def test_property(self):
        instance = UMLObject()
        property = "+property"
        
        instance.add_method(property)
        result = instance.methods()[0]
        
        self.assertEquals(result, property)
        
    def test_attribute_sorting(self):
        instance = UMLObject()
        attributes = ["+a", "-z", "#z", "#c", "-b", "+c"]
        
        [instance.add_attribute(attr) for attr in attributes]
        
        result = instance.attributes()

        visibilities = map(lambda str: str[0] , result)
        identificators = map(lambda str: str[1:] , result)
        self.assertEquals(visibilities, ["+", "+", "#","#","-","-"])
        self.assertEquals(identificators, ["a", "c", "c","z","b","z"])
        
    def test_attribute(self):
        attribute   = "prototype"
        value       = "Interface"
        instance = UMLObject()
        
        instance[attribute] = value
        
        self.assertEquals(instance[attribute], value)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
