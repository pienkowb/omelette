import unittest
from mock import Mock
from omelette.fromage.diagram import Diagram
from PyQt4 import QtGui
import qapp

class DiagramTest(unittest.TestCase):

    def setUp(self):
        self.umlo = Mock()
        self.diag = Diagram(modules_path="omelette.fromage.test.data")
        self.diag.set_type("somediagram")
        self.umlo.name = "test"
        

    def test_edge(self):
        self.umlo.type = "Edge"
        self.diag.add(self.umlo)

        self.assertTrue("test" in self.diag.edges)
        self.assertFalse("test" in self.diag.nodes)

    def test_node(self):
        self.umlo.type = "Node"
        self.diag.add(self.umlo)

        self.assertTrue("test" in self.diag.nodes)
        self.assertFalse("test" in self.diag.edges)

    def test_clear(self):
        self.umlo.type = "Node"
        self.diag.add(self.umlo)
        self.umlo.type = "Edge"
        self.diag.add(self.umlo)

        self.diag.clear()

        self.assertFalse("test" in self.diag.edges)
        self.assertFalse("test" in self.diag.nodes)

if __name__ == "__main__":
    unittest.main()
