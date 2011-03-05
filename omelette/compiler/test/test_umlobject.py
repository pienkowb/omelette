import unittest
from omelette.compiler.uml import UMLObject
from mock import Mock, MagicMock

class UMLObjectTest(unittest.TestCase):
    def test_constructor(self):
        o = UMLObject("fasada", "asd", True)
        self.assertEquals(o.parent, "fasada")
        self.assertEquals(o.name, "asd")
        self.assertTrue(o.is_prototype)

    def test_eq(self):
        instance = UMLObject("fasada", "asd", True)
        other = UMLObject("fasada", "asd", True)
        instance["a"] = 3
        other["a"] = 3

        self.assertEquals(instance, other)

    def test_not_eq_field(self):
        instance = UMLObject("fasada", "asd", False)
        other = UMLObject("fasada", "asd", True)

        self.assertNotEqual(instance, other)

    def test_not_eq_property(self):
        instance = UMLObject()
        other = UMLObject()
        instance["a"] = 3
        other["a"] = 4

        self.assertNotEqual(instance, other)

    def test_not_eq_operation(self):
        instance = UMLObject()
        other = UMLObject()
        (o1, o2) = (Mock(), Mock())
        instance.add_operation(o1)
        instance.add_operation(o2)

        self.assertNotEqual(instance, other)

    def test_eq_operation(self):
        instance = UMLObject()
        other = UMLObject()
        o1 = MagicMock()
        o1.__eq__.return_value = True
        o2 = MagicMock()
        o2.__eq__.return_value = True
        instance.add_operation(o1)
        other.add_operation(o2)

        self.assertEqual(instance, other)

    def test_operation(self):
        instance = UMLObject()
        operation = Mock()
        instance.add_operation(operation)
        result = instance.operations()[0]

        self.assertEquals(result, operation)

    def test_attribute(self):
        instance = UMLObject()
        attribute = Mock()

        instance.add_attribute(attribute)
        result = instance.attributes()[0]

        self.assertEquals(result, attribute)

    def test_property(self):
        property = "stereotype"
        value = "Interface"
        instance = UMLObject()

        instance[property] = value

        self.assertEquals(value, instance[property])


if __name__ == "__main__":
    unittest.main()
