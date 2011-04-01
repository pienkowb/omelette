from omelette.fromage.common import *
from omelette.fromage.diagramcommon import DrawableText

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
        
        self.__texts = {}
        for tag in ['name', 'name2']:
            self.__texts[tag] = DrawableText(self)
            self.__texts[tag].setParentItem(self) 
        
        self.setLine(QLineF(210, 100, 330, 330))
        
    def boundingRect(self):
        return self.__boundingRect
    
    def __get_origin(self):
        x = min(self.real_line().p1().x(), self.real_line().p2().x())
        y = min(self.real_line().p1().y(), self.real_line().p2().y())
        return QPointF(x, y)
    
    def real_line(self):
        return self.__real_line 
    
    def __find_real_line(self):
        line = self.line()
                
        line = self.source.przytnij_linie(line, 0)
        line = self.target.przytnij_linie(line, 1)
        
        return line
    
    def update(self):
        self.setLine(QLineF(self.source.znajdz_anchor(), self.target.znajdz_anchor()))
        self.__real_line = self.__find_real_line()
        
        self.__distanceX = self.real_line().dx()
        self.__distanceY = self.real_line().dy()
        self.__originPos = self.__get_origin()
        
        self.__boundingRect = QRectF(self.__originPos, QSizeF(math.fabs(self.__distanceX), math.fabs(self.__distanceY)))
        
        #TODO: Fix division by 0
        self.__angle = math.atan(self.__distanceY / self.__distanceX)
        
        self.__xmarg = math.sin(self.__angle)
        self.__ymarg = math.cos(self.__angle)
        
        self.__update_text('name', 'Bar', 0.5, 1)
        self.__update_text('name2', 'nex', 0.1, -1)
        
    def __update_text(self, tag, text, pos, orientation):
        xPos = self.real_line().p1().x() + self.__distanceX * pos
        yPos = self.real_line().p1().y() + self.__distanceY * pos
        
        if(self.__angle >= 0):
            if(orientation == -1):
                xPos -= self.__xmarg * 10
                yPos += self.__ymarg * 10
            else:
                xPos += self.__xmarg * 10
                yPos -= self.__ymarg * 10 + self.__fontMetrics.height()
        else:
            if(orientation == -1):
                xPos += -self.__xmarg * 10
                yPos += self.__ymarg * 10
            else:
                xPos -= self.__xmarg * 10
                yPos -= self.__ymarg * 10 + self.__fontMetrics.height()
                
        xPos -= self.__fontMetrics.width(text) / 2
        #rect = QRectF(xPos, yPos, self.__fontMetrics.width(text), self.__fontMetrics.height())        
        
        self.__texts[tag].setPos(xPos, yPos)
        self.__texts[tag].text = text
        
        #self.__texts.append((rect, text))
        #self.__boundingRect = self.__boundingRect.united(rect)
    
    def paint(self, painter, style, widget):
        myPen = self.pen()
        myPen.setColor(QColor(255, 0, 0))
        
        painter.setPen(myPen)
        painter.setBrush(QColor(0, 0, 255))
        
        painter.drawLine(self.real_line())

