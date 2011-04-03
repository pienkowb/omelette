from omelette.fromage.common import *
from omelette.fromage.diagramcommon import DrawableText

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF
from PyQt4.Qt import *

import math

class ArrowHead(object):
    def __init__(self):
        self.angle = math.radians(30)
        self.length = 15
        
    def draw(self, painter, point, angle):
        pass

class ArrowHeadAss(ArrowHead):
    # TODO: Update for arrowhead, keep points and just draw 
    # them instead of calculating every time
    def draw(self, painter, point, line):
        angle = math.asin(line.dx() / line.length())
        
        if(point == line.p2()):
            orientation = -1
        else: # always falling back to "1"
            orientation = 1
        
        if(line.dy() >= 0):
            y1 = math.cos(angle - self.angle) * self.length
            x1 = math.sin(angle - self.angle) * self.length
            
            y2 = math.cos(angle + self.angle) * self.length
            x2 = math.sin(angle + self.angle) * self.length
        else:
            y1 = math.cos(math.pi - angle - self.angle) * self.length
            x1 = math.sin(math.pi - angle - self.angle) * self.length
            
            y2 = math.cos(math.pi - angle + self.angle) * self.length
            x2 = math.sin(math.pi - angle + self.angle) * self.length

        painter.drawLine(QLineF(point, point + QPointF(x1, y1) * orientation))
        painter.drawLine(QLineF(point, point + QPointF(x2, y2) * orientation))

class ArrowHeadComp(ArrowHead):
    # TODO: Update for arrowhead, keep points and just draw 
    # them instead of calculating every time
    def draw(self, painter, point, line):
        angle = math.asin(line.dx() / line.length())
        
        if(point == line.p2()):
            orientation = -1
        else: # always falling back to "1"
            orientation = 1
        
        if(line.dy() >= 0):
            y1 = math.cos(angle - self.angle) * self.length
            x1 = math.sin(angle - self.angle) * self.length
            
            y2 = math.cos(angle + self.angle) * self.length
            x2 = math.sin(angle + self.angle) * self.length
        else:
            y1 = math.cos(math.pi - angle - self.angle) * self.length
            x1 = math.sin(math.pi - angle - self.angle) * self.length
            
            y2 = math.cos(math.pi - angle + self.angle) * self.length
            x2 = math.sin(math.pi - angle + self.angle) * self.length

        x3 = x2 - math.sin(math.pi*2 - angle - self.angle) * self.length
        y3 = y2 - math.cos(math.pi*2 - angle - self.angle) * self.length
        
        polygon = QPolygonF([point, 
                             point + QPointF(x1, y1) * orientation, 
                             point + QPointF(x3, y3) * orientation, 
                             point + QPointF(x2, y2) * orientation])
        
        painter.drawPolygon(polygon)
 
class ArrowHeadGen(ArrowHead):
    # TODO: Update for arrowhead, keep points and just draw 
    # them instead of calculating every time
    def draw(self, painter, point, line):
        angle = math.asin(line.dx() / line.length())
        
        if(point == line.p2()):
            orientation = -1
        else: # always falling back to "1"
            orientation = 1
        
        if(line.dy() >= 0):
            y1 = math.cos(angle - self.angle) * self.length
            x1 = math.sin(angle - self.angle) * self.length
            
            y2 = math.cos(angle + self.angle) * self.length
            x2 = math.sin(angle + self.angle) * self.length
        else:
            y1 = math.cos(math.pi - angle - self.angle) * self.length
            x1 = math.sin(math.pi - angle - self.angle) * self.length
            
            y2 = math.cos(math.pi - angle + self.angle) * self.length
            x2 = math.sin(math.pi - angle + self.angle) * self.length
            
        polygon = QPolygonF([point, 
                             point + QPointF(x1, y1) * orientation,  
                             point + QPointF(x2, y2) * orientation])
        
        painter.drawPolygon(polygon)

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
                
        line = self.source_anchor.slot.przytnij_linie(line, 0)
        line = self.target_anchor.slot.przytnij_linie(line, 1)
        
        return line
    
    def update(self):
        self.setLine(QLineF(self.source_anchor.slot.znajdz_anchor(), self.target_anchor.slot.znajdz_anchor()))
        self.__real_line = self.__find_real_line()
        
        self.__distanceX = self.real_line().dx()
        self.__distanceY = self.real_line().dy()
        self.__originPos = self.__get_origin()
        
        #Adjust for arrowheads, hardcoded values for now 
        self.__boundingRect = (QRectF(self.__originPos, QSizeF(math.fabs(self.__distanceX), math.fabs(self.__distanceY)))
                                    .adjusted(-30,-30,30,30))
        
        self.__angle = math.asin(self.__distanceX / self.real_line().length())
        
        self.__xmarg = math.sin(self.__angle)
        self.__ymarg = math.cos(self.__angle)
        
        self.__update_text('name', 'Bar', 0.5, 1)
        self.__update_text('name2', 'nex', 0.1, -1)
        
    def __update_text(self, tag, text, pos, orientation):
        dtext = self.__texts[tag]
        
        xPos = self.real_line().p1().x() + self.__distanceX * pos
        yPos = self.real_line().p1().y() + self.__distanceY * pos
        
        dtext.origin_pos = QPointF(xPos, yPos)
        
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
        
        dtext.setPos(xPos, yPos)
        dtext.text = text
        #dtext.setVisible(False)
    
    def paint(self, painter, style, widget):
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        myPen = self.pen()
        myPen.setColor(QColor(0, 0, 0))
        
        painter.setPen(myPen)
        painter.setBrush(QColor(0, 0, 0))
        
        painter.drawLine(self.real_line())

        head1 = ArrowHeadGen()
        head1.draw(painter, self.real_line().p1(), self.real_line())
        head2 = ArrowHeadComp()
        head2.draw(painter, self.real_line().p2(), self.real_line())
        
        painter.setRenderHint(QPainter.Antialiasing, False)
