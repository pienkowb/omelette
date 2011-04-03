import unittest
from mock import Mock
from omelette.fromage.diagram import Diagram
import omelette.fromage.test.qapp

class DiagramTest(unittest.TestCase):

    def setUp(self):
        self.diagram = Diagram(modules_path="omelette.fromage.test.data")

        self.uml_object = Mock()
        self.uml_object.name = "test"

    def test_node(self):
        self.uml_object.type = "node"
        self.diagram.add(self.uml_object)

        self.assertTrue("test" in self.diagram.nodes)
        self.assertFalse("test" in self.diagram.edges)

    def test_edge(self):
        self.uml_object.type = "edge"
        self.diagram.add(self.uml_object)

        self.assertTrue("test" in self.diagram.edges)
        self.assertFalse("test" in self.diagram.nodes)

    def test_clear(self):
        self.uml_object.type = "node"
        self.diagram.add(self.uml_object)

        self.uml_object.type = "edge"
        self.diagram.add(self.uml_object)

        self.diagram.clear()

        self.assertFalse("test" in self.diagram.edges)
        self.assertFalse("test" in self.diagram.nodes)


if __name__ == "__main__":
    unittest.main()
