import unittest
from mock import Mock
from omelette.fromage.factory import DrawableFactory

class DrawableFactoryTest(unittest.TestCase):
    def test_create(self):
        uml_object = Mock()
        uml_object.type = "relation"

        drawable = DrawableFactory.create("class", uml_object)
        self.assertEquals("DrawableRelation", drawable.__class__.__name__)


if __name__ == "__main__":
    unittest.main()
