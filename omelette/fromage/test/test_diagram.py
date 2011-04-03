import unittest
from mock import Mock
from omelette.fromage.diagram import Diagram
import omelette.fromage.test.qapp
from omelette.fromage.common import DrawableNode, DrawableEdge

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

    def test_anchor(self):
        target = Mock()
        target.type = "node"

        source = Mock()
        source.type = "node"

        relation = Mock()
        relation.type = "edge"

        # given two node objects connected by an edge object
        
        target.name = "target"
        source.name = "source"

        properties = {"source-object": "source", "target-object": "target"}

        def getitem(name):
            return properties[name]

        relation.__getitem__ = Mock(side_effect=getitem)
        relation.name = "relation"

        # added to diagram

        self.diagram.add(relation)
        self.diagram.add(target)
        self.diagram.add(source)

        # when anchors are set 

        self.diagram.set_anchors()

        # each DrawableNode object should be referenced by proper DrawableEdge object's anchors
        drawable_relation = self.diagram.edges["relation"]
        drawable_source = self.diagram.nodes["source"]
        drawable_target = self.diagram.nodes["target"]

        self.assertEquals(drawable_source, drawable_relation.source_anchor.slot)
        self.assertEquals(drawable_target, drawable_relation.target_anchor.slot)

        # and each DrawableNode object's anchor should reference the
        # DrawableEdge object
        self.assertEquals(drawable_relation, drawable_source.anchors.pop().connector)
        self.assertEquals(drawable_relation, drawable_target.anchors.pop().connector)


if __name__ == "__main__":
    unittest.main()
