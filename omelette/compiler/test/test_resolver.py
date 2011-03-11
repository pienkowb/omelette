import unittest
from omelette.compiler.resolver import DependencyResolver
from omelette.compiler.uml import UMLObject

class DependencyResolverTest(unittest.TestCase):
    def setUp(self):
        relation = UMLObject()
        relation.name = "relation"

        association = UMLObject()
        association.name = "association"
        association.parent = "relation"
        association["arrow"] = "association"
        association["direction"] = "none"

        one_to_many = UMLObject()
        one_to_many.name = "one-to-many"
        one_to_many.parent = "association"
        one_to_many["source-count"] = "1"
        one_to_many["target-count"] = "*"

        list = [relation, association, one_to_many]
        self.uml_objects = dict([(object.name, object) for object in list])
    
    def test_resolve(self):
        DependencyResolver(self.uml_objects).resolve()

        one_to_many = self.uml_objects["one-to-many"]

        self.assertEquals("relation", one_to_many.type)
        self.assertEquals("association", one_to_many["arrow"])


if __name__ == "__main__":
    unittest.main()
