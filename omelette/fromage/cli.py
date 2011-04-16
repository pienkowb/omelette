import sys
sys.path.append('../../') 
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QImage, QPainter
from omelette.fromage.diagram import Diagram
from omelette.compiler.compiler import Compiler
from omelette.compiler.code import Code

QT_APP = QtGui.QApplication([])

def main(argv):
    diagram = Diagram(None)

    loltext = "prototype base class\nprototype base relation\nclass asd\nclass bsd\nrelation csd\nsource-object: asd\ntarget-object: bsd\ntarget-arrow: composition"
    
    compiler = Compiler()
    
    code = Code(loltext)
    uml_objects = compiler.compile(code)
    diagram.set_type("class")

    for name, uml_object in uml_objects.items():
        if "name" not in uml_object.properties:
            uml_object["name"] = name
        if uml_object.is_prototype:
            del uml_objects[name]
    
    diagram.add(uml_objects)
    
    img = QImage(1024, 768, QImage.Format_ARGB32)
    painter = QPainter(img)
    painter.resetMatrix()
    diagram.render(painter)
    painter.end()
    ret = img.save("/dev/null")
    print("Save returned " + str(ret))

    return 0


if __name__ == "__main__":
    exit(main(sys.argv))