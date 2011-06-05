#!/usr/bin/env python
import sys
import os

script_path = os.path.dirname(os.path.realpath(__file__))
modules_path = os.path.normcase("../../")
modules_directory = os.path.join(script_path, modules_path)
sys.path.append(modules_directory)

import getopt
from PyQt4 import QtGui
from PyQt4.QtGui import QImage, QPainter, QGraphicsScene, QBrush, QColor
from PyQt4.Qt import *

from omelette.fromage.diagram import Diagram
from omelette.compiler.compiler import Compiler
from omelette.compiler.code import Code, Library
from omelette.fromage.layouter import LayoutFactory
from omelette.compiler import logging

QT_APP = QtGui.QApplication([])

def usage():
    print """Usage: cli.py -h --help -i --input -o -output -l --layout -m --margin -s --scale"""

def help():
    usage()
    print """-h --help Displays this info
-i --input Input .uml file. If not provided, stdin is used.
-o --output Output image file.
-m --margin Picture margins. Default: 10px
-s --scale Scale of diagram. Default: 1
-l --layout Sets the layouter
Default layouter is Circular layout.
Available layouters:"""
    for i in LayoutFactory.layouts():
        print "\t- " + i

def main(argv):
    logger = logging.getLogger('compiler')
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hi:o:l:m:s:", ["help", "input=", "output=", "layout=", "margin=", "scale="])
    except getopt.GetoptError, err:
        print str(err)
        print usage()
        return 1

    input = ""
    output = ""
    layouter = LayoutFactory.get("Circular layout") #default layouter
    margin = 10
    scale = 1
    
    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            return 1
        elif o in ("-i", "--input"):
            input = a
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-l", "--layout"):
            if(a in LayoutFactory.layouts()):
                layouter = LayoutFactory.get(a)
            elif(a + " layout" in LayoutFactory.layouts()):
                layouter = LayoutFactory.get(a + " layout")
            else:
                print "Unknown layout '", a, "', using Circular layout."
        elif o in ("-m", "--margin"):
            margin = int(a)
        elif o in ("-s", "--scale"):
            scale = float(a)
        else:
            assert False, "unhandled opt " + o

    if(output == ""):
        print "Output file not provided."
        return -1

    if(input == ""):
        input_file = sys.stdin
    else:
        try:
            input_file = open(input, 'r')
        except IOError, err:
            print "IOError: " + str(err)
            return 2
    code = Code(input_file.read())

    diagram = Diagram()
    scene = QGraphicsScene(None)
    compiler = Compiler(Library.load_libraries())

    uml_objects = compiler.compile(code)
    if not logger.has("ERROR CRITICAL"):
        for uml_object in uml_objects.values():
            diagram.add(uml_object)

        # nodes must be updated before layouting
        for node in diagram.nodes.values():
            node.update()

        # needed to layout and draw edges
        diagram.set_anchors()

        layouter.apply(diagram)

        # edges must be updated after nodes are updated and layouted
        for edge in diagram.edges.values():
            edge.update()

        # this actually paints things, so must be invoked when everything is
        # ready
        for drawable in diagram.elements():
            scene.addItem(drawable)
            drawable.resize_scene_rect()
            
        adj_scene_rect = scene.sceneRect().adjusted(-margin, -margin, margin, margin)
        scene.setSceneRect(adj_scene_rect)
        
        diagramsize = adj_scene_rect.toRect().size()

        img = QImage(QSize(diagramsize.width() * scale, diagramsize.height() * scale), QImage.Format_ARGB32)
        painter = QPainter(img)
        print margin
        absoluteRect = QRectF(0, 0, scene.sceneRect().width() * scale, scene.sceneRect().height() * scale)
        painter.fillRect(absoluteRect, QBrush(QColor(255, 255, 255), Qt.SolidPattern))
        painter.resetMatrix()
        scene.render(painter)
        painter.end()
        ret = img.save(output)
        print("Saved to " + output)

    for e in logger.events:
        print str(e)
    if not logger.has("ERROR CRITICAL"):
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main(sys.argv))
