from omelette.fromage.common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF
from PyQt4.Qt import *

import math

class DrawableRelation(DrawableEdge, QGraphicsLineItem):
    def __init__(self, uml_object):
        super(DrawableRelation, self).__init__(uml_object)
        QGraphicsLineItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)
        
        self.setLine(QLineF(410,10,330,330))
        self.__boundingRect = QRectF(self.line().p1(), 
                                     QSizeF(self.line().p2().x() - self.line().p1().x(),
                                       self.line().p2().y() - self.line().p1().y())).normalized()
        
    def boundingRect(self):
        return self.__boundingRect
    
    def getOrigin(self):
        x = min(self.line().p1().x(), self.line().p2().x())
        y = min(self.line().p1().y(), self.line().p2().y())
        return QPointF(x, y)
    
    def update(self):
        self.__boundingRect = QRectF(self.line().p1(), 
                                     QSizeF(self.line().p2().x() - self.line().p1().x(),
                                       self.line().p2().y() - self.line().p1().y())).normalized()
    
    def paint(self, painter, style, widget):
        #QGraphicsLineItem.paint(self, painter, style, widget)
        myPen = self.pen()
        myPen.setColor(QColor(255,0,0))
        
        painter.setPen(myPen)
        painter.setBrush(QColor(0,0,255))
        
        painter.drawLine(self.line())
        
        metrics = QFontMetrics(self.__font)
        painter.setFont(self.__font)
        
        textToDraw = "asdasdqwe"
        width = metrics.width(textToDraw)
        height = metrics.height()
        
        angle = math.atan((self.line().p2().y() - self.line().p1().y()) / (self.line().p2().x() - self.line().p1().x()))
        
        xmarg = 10 * math.sin(angle)
        ymarg = 10 * math.cos(angle)
        
        textx = self.getOrigin().x() + (math.fabs(self.line().p1().x() - self.line().p2().x()) / 2)
        texty = self.getOrigin().y() + (math.fabs(self.line().p1().y() - self.line().p2().y()) / 2)
        
        print angle
        
        if(angle >= 0):  
            textx -= xmarg
            texty -= ymarg
        else:
            textx += xmarg - width
            texty += ymarg
             
        
        painter.drawText(QRect(textx, texty - height, width, height), 0, textToDraw)