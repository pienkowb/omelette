import unittest
from omelette.fromage.common import *
from omelette.compiler.uml import UMLObject,Attribute,Operation

class UnitTest(unittest.TestCase):

    def test_anchors(self):
        instance = DrawableEdge(None)
        
        anchor = Anchor()
        instance.target_anchor = anchor
        self.assertEqual(anchor, instance.target_anchor)
    

if __name__ == "__main__":
    unittest.main()

