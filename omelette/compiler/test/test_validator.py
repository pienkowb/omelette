import unittest
from omelette.compiler.uml import UMLObject
from omelette.compiler.validator import Validator
from omelette.compiler import logging

class ValidatorTest(unittest.TestCase):

    def setUp(self):
        self.uml_object = UMLObject()
        self.uml_object.required = {"source-object": "OBJECT"}
        self.uml_object.allowed = {
            "arrow": "STRING",
            "direction": ["none", "source", "target", "both"],
            "source-role": "STRING",
            "source-count": "MULTIPLICITY"}

        self.logger = logging.getLogger("compiler")
        self.logger.flush()

    def test_validate_all_allowed(self):
        self.uml_object.properties = {
            "arrow": ("association", "STRING"),
            "direction": ("target", "OBJECT"),
            "source-object": ("Student", "OBJECT"),
            "source-role": ("learns", "STRING"),
            "source-count": ("1", "MULTIPLICITY")}

        Validator(self.uml_object).validate()
        self.assertTrue(self.logger.is_empty())

    def test_validate_not_allowed(self):
        self.uml_object.properties = {
            "stereotype": ("not_allowed", "STRING"),
            "source-object": ("Student", "OBJECT")}

        Validator(self.uml_object).validate()
        self.assertFalse(self.logger.is_empty())

    def test_validate_no_required(self):
        self.uml_object.properties = {
            "arrow": ("association", "STRING"),
            "direction": ("none", "OBJECT")}

        Validator(self.uml_object).validate()
        self.assertFalse(self.logger.is_empty())


if __name__ == "__main__":
    unittest.main()
