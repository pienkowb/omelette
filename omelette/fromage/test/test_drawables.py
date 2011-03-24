import unittest
from omelette.fromage.common import *

class DrawablesTest(unittest.TestCase):
    
    def test_anchors(self):
        instance = DrawableEdge(None)
        anchor = Anchor()
        instance.target_anchor = anchor
        self.assertEqual(anchor, instance.target_anchor)

    def test_position(self):
        instance = DrawableNode(None)
        pos = (3, 5)
        instance.position = pos
        self.assertEqual(pos, instance.position)       

if __name__ == "__main__":
    unittest.main()
