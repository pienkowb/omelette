import sys
sys.path.append('../../') 
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QImage, QPainter, QGraphicsScene
from omelette.fromage.diagram import Diagram
from omelette.compiler.compiler import Compiler
from omelette.compiler.code import Code
from omelette.fromage.layouter import Layouter

QT_APP = QtGui.QApplication([])

def main(argv):
    diagram = Diagram()
    scene = QGraphicsScene(None)

    loltext = "prototype base class\nprototype base relation\nclass asd\nclass bsd\nrelation csd\nsource-object: asd\ntarget-object: bsd\ntarget-arrow: composition"
    
    compiler = Compiler()
    
    code = Code(loltext)
    uml_objects = compiler.compile(code)
    
    for uml_object in uml_objects.values():
        diagram.add(uml_object)

    # nodes must be updated before layouting
    for node in diagram.nodes.values():
        node.update()

    # needed to layout and draw edges
    diagram.set_anchors()

    Layouter.layout(diagram)

    # edges must be updated after nodes are updated and layouted
    for edge in diagram.edges.values():
        edge.update()

    # this actually paints things, so must be invoked when everything is
    # ready
    for drawable in diagram.elements():
        scene.addItem(drawable)
        drawable.resize_scene_rect()
    
    img = QImage(scene.sceneRect().toRect().size(), QImage.Format_ARGB32)
    painter = QPainter(img)
    painter.resetMatrix()
    scene.render(painter)
    painter.end()
    ret = img.save("C:/home/zapu/omlet_test.png")
    print("Save returned " + str(ret))

    return 0


if __name__ == "__main__":
    exit(main(sys.argv))