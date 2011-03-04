from omelette.fromage.common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF
from PyQt4.Qt import *

import math

class DrawableRelation(DrawableEdge, QGraphicsLineItem):
    def __init__(self, uml_object):
        super(DrawableRelation, self).__init__(uml_object)
        QGraphicsLineItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 300, 300)
        self.__font = QFont('Comic Sans MS', 10)
        self.__fontMetrics = QFontMetrics(self.__font)
        
        self.__relationName = "aasdasd"
        
        self.__texts = []
        
        self.setLine(QLineF(210,100,330,330))
        self.update()
        
    def boundingRect(self):
        return self.__boundingRect
    
    def __getOrigin(self):
        x = min(self.line().p1().x(), self.line().p2().x())
        y = min(self.line().p1().y(), self.line().p2().y())
        return QPointF(x, y)
    
    def update(self):
        self.__distanceX = self.line().dx()
        self.__distanceY = self.line().dy()
        self.__originPos = self.__getOrigin()
        
        self.__boundingRect = QRectF(self.__originPos, QSizeF(math.fabs(self.__distanceX), math.fabs(self.__distanceY)))
        
        self.__angle = math.atan(self.__distanceY / self.__distanceX)
        
        self.__xmarg = math.sin(self.__angle)
        self.__ymarg = math.cos(self.__angle)
        
        del self.__texts[:]
        
        self.__addText(self.__relationName, 0.5, 1)
        self.__addText(str(self.__angle), 0.5, -1)
        self.__addText(str(self.__distanceX), 0.1, -1)
        self.__addText(str(self.__distanceY), 0.1, 1)
        self.__addText(str("bar"), 0.9, -1)
        self.__addText(str("nex"), 0.9, 1)
        
    def __addText(self, text, pos, orientation):
        xPos = self.line().p1().x() + self.__distanceX * pos
        yPos = self.line().p1().y() + self.__distanceY * pos
        
        if(self.__angle >= 0):
            if(orientation == -1):
                xPos -= self.__fontMetrics.width(text) + self.__xmarg * 10
                yPos += self.__ymarg * 10
            else:
                xPos += self.__xmarg * 10
                yPos -= self.__ymarg * 10 + self.__fontMetrics.height()
        else:
            if(orientation == -1):
                xPos += -self.__xmarg * 10
                yPos += self.__ymarg * 10
            else:
                xPos -= self.__fontMetrics.width(text) - self.__xmarg * 10
                yPos -= self.__ymarg * 10 + self.__fontMetrics.height()
                
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
             
        for text in self.__texts:
            painter.drawText(text[0], 0, text[1])