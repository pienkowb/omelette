import unittest
from omelette.compiler.uml import UMLObject
from omelette.compiler.validator import Validator

class ValidatorTest(unittest.TestCase):

    def setUp(self):
        self.instance = Validator()
        self.uml_object = UMLObject()

        self.uml_object.required = {"source-object": "OBJECT"}

        self.uml_object.allowed = {
            "arrow": "STRING",
            "direction": ["none", "source", "target", "both"],
            "source-role": "STRING",
            "source-count": "MULTIPLICITY"}

    def test_validate_all_allowed(self):
        self.uml_object.properties = {
            "arrow": ("association", "STRING"),
            "direction": ("target", "CONSTANT"),
            "source-object": ("Student", "OBJECT"),
            "source-role": ("learns", "STRING"),
            "source-count": ("1", "MULTIPLICITY")}

        self.assertTrue(self.instance.validate(self.uml_object))

    def test_validate_not_allowed(self):
        self.uml_object.properties = {
            "stereotype": ("not_allowed", "STRING"),
            "source-object": ("Student", "OBJECT")}

        self.assertFalse(self.instance.validate(self.uml_object))

    def test_validate_no_required(self):
        self.uml_object.properties = {
            "arrow": ("association", "STRING"),
            "direction": ("none", "CONSTANT")}

        self.assertFalse(self.instance.validate(self.uml_object))


if __name__ == "__main__":
    unittest.main()
