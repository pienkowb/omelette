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
        self.__fontMetrics = QFontMetrics(self.__font)
        
        self.__relationName = "aasdasd"
        
        self.__texts = []
        
        self.setLine(QLineF(410,10,330,330))
        self.update()
        
    def boundingRect(self):
        return self.__boundingRect
    
    def __getOrigin(self):
        x = min(self.line().p1().x(), self.line().p2().x())
        y = min(self.line().p1().y(), self.line().p2().y())
        return QPointF(x, y)
    
    def update(self):
        self.__distanceX = self.line().p2().x() - self.line().p1().x()
        self.__distanceY = self.line().p2().y() - self.line().p1().y()
        self.__originPos = self.__getOrigin()
        
        self.__boundingRect = QRectF(self.__originPos, QSizeF(math.fabs(self.__distanceX), math.fabs(self.__distanceY)))
        
        self.__angle = math.atan(self.__distanceY / self.__distanceX)
        
        self.__xmarg = math.sin(self.__angle)
        self.__ymarg = math.cos(self.__angle)
        
        del self.__texts[:]
        
        self.__addText(self.__relationName, 0.5, 1)
        
    def __addText(self, text, pos, orientation):
        xPos = self.__originPos.x() + math.fabs(self.__distanceX) * pos
        yPos = self.__originPos.y() + math.fabs(self.__distanceY) * pos
        
        xPos += self.__xmarg
        yPos -= self.__xmarg
        
        rect = QRectF(xPos, yPos, self.__fontMetrics.width(text), self.__fontMetrics.height())
        
        self.__texts.append((rect, text))
        self.__boundingRect = self.__boundingRect.united(rect)
    
    def paint(self, painter, style, widget):
        #QGraphicsLineItem.paint(self, painter, style, widget)
        myPen = self.pen()
        myPen.setColor(QColor(255,0,0))
        
        painter.setPen(myPen)
        painter.setBrush(QColor(0,0,255))
        
        painter.drawLine(self.line())
        
        painter.setFont(self.__font)
        
        """
        FFR
        if(angle >= 0):  
            textx -= xmarg
            texty -= ymarg
        else:
            textx += xmarg - width
            texty += ymarg
             """
             
        for text in self.__texts:
            painter.drawText(text[0], 0, text[1])