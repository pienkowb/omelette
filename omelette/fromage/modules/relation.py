from omelette.fromage.common import *
from omelette.fromage.diagramcommon import DrawableText

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF
from PyQt4.Qt import *

import math

def str2arrow(name):
    if name == "association":
        return ArrowHeadAss();
    elif name == "composition":
        return ArrowHeadComp(filled=True)
    elif name == "aggregation":
        return ArrowHeadComp(filled=False)
    elif name == "generalization":
        return ArrowHeadGen(filled=False)
    else: 
        raise AttributeError('Unknow arrowname given!!')

# Warning. Copy&Paste methodology was used to write following code
#TODO: Please consider refactoring and/or moving ArrowHead classes.

class ArrowHead(object):
    def __init__(self, filled=False):
        self.angle = math.radians(30)
        self.length = 15
        self.filled = filled
        
    def draw(self, painter, point, line):
        pass

class ArrowHeadStandard(ArrowHead):
    def draw(self, painter, point, line):
        # Does not actually draw anything, just finds points
        # TODO: Move finding points to another method, "update" ?
        
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
            
            x3 = x1 + math.sin(angle + self.angle) * self.length
            y3 = y1 + math.cos(angle + self.angle) * self.length
        else:
            y1 = math.cos(math.pi - angle - self.angle) * self.length
            x1 = math.sin(math.pi - angle - self.angle) * self.length
            
            y2 = math.cos(math.pi - angle + self.angle) * self.length
            x2 = math.sin(math.pi - angle + self.angle) * self.length
            
            x3 = x2 - math.sin(math.pi*2 - angle - self.angle) * self.length
            y3 = y2 - math.cos(math.pi*2 - angle - self.angle) * self.length
            
        self.pointA = point + QPointF(x1, y1) * orientation
        self.pointB = point + QPointF(x2, y2) * orientation
        self.pointC = point + QPointF(x3, y3) * orientation  
        
        # Prepare the painter, too
        if(self.filled):
            painter.setBrush(QColor(0, 0, 0))
        else:
            painter.setBrush(QColor(255, 255, 255))

class ArrowHeadAss(ArrowHeadStandard):
    def draw(self, painter, point, line):
        super(ArrowHeadAss, self).draw(painter, point, line)

        painter.drawLine(QLineF(point, self.pointA))
        painter.drawLine(QLineF(point, self.pointB))

class ArrowHeadComp(ArrowHeadStandard):   
    def draw(self, painter, point, line):
        super(ArrowHeadComp, self).draw(painter, point, line)
        
        polygon = QPolygonF([point, self.pointA, self.pointC, self.pointB])
        painter.drawPolygon(polygon)
 
class ArrowHeadGen(ArrowHeadStandard):        
    def draw(self, painter, point, line):
        super(ArrowHeadGen, self).draw(painter, point, line)
        
        polygon = QPolygonF([point, self.pointA, self.pointB])
        painter.drawPolygon(polygon)


class DrawableRelation(DrawableEdge, QGraphicsLineItem):
    def __init__(self, uml_object):
        super(DrawableRelation, self).__init__(uml_object)
        QGraphicsLineItem.__init__(self)
        
        self.__boundingRect = QRectF(0, 0, 300, 300)
        self.__font = QFont('Comic Sans MS', 10)
        self.__fontMetrics = QFontMetrics(self.__font)
        
        self.__texts = {}
        
        self.__create_text('name', 0.5, 1)
        
        self.__create_text('source-count', 0.1, 1)
        self.__create_text('source-role', 0.1, -1)
        
        self.__create_text('target-count', 0.9, 1)
        self.__create_text('target-role', 0.9, -1)
        
        self.source_arrow = None
        self.target_arrow = None
        
    def __create_text(self, tag, position, orientation):
        dtext = DrawableText.create_drawable_text(self)
        dtext.text_position = position
        dtext.text_orientation = orientation
        
        self.__texts[tag] = dtext
         
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
                
        line = self.source_anchor.slot.crop_line(line, 0)
        line = self.target_anchor.slot.crop_line(line, 1)
        
        return line
    
    def update(self):        
        self.setLine(QLineF(self.source_anchor.slot.find_anchor(), self.target_anchor.slot.find_anchor()))
        self.__real_line = self.__find_real_line()
        
        if(self.real_line().length() <= 0):
            # ABANDON SHIP!
            return

        self.__distanceX = self.real_line().dx()
        self.__distanceY = self.real_line().dy()
        self.__originPos = self.__get_origin()
        
        # Adjust for arrowheads, hardcoded values for now 
        #TODO: make it not hardcoded? :(
        self.__boundingRect = (QRectF(self.__originPos, QSizeF(math.fabs(self.__distanceX), math.fabs(self.__distanceY)))
                                    .adjusted(-30,-30,30,30))
        
        self.__angle = math.asin(self.__distanceX / self.real_line().length())
        
        self.__xmarg = math.sin(self.__angle)
        self.__ymarg = math.cos(self.__angle)
        
        for (tag, text) in self.__texts.iteritems():
            self.__update_text(tag, text)
            
        # Updating arrows
        # (Damn, that's ugly.)
        if('source-arrow' in self.uml_object):
            self.source_arrow = str2arrow(self.uml_object['source-arrow'])
        else:
            self.source_arrow = None
            
        if('target-arrow' in self.uml_object):
            self.target_arrow = str2arrow(self.uml_object['target-arrow'])
        else:
            self.target_arrow = None
            
    def __update_text(self, tag, dtext):
        if tag not in self.uml_object: 
            # just dock the unused DrawableText somewhere
            dockPoint = QPointF(self.real_line().p1().x(), self.real_line().p1().y())
            dtext.setPos(dockPoint)
            dtext.origin_pos = QPointF(dockPoint)
            dtext.setVisible(False)
            return
        
        text = str(self.uml_object[tag])
        
        xPos = self.real_line().p1().x() + self.__distanceX * dtext.text_position
        yPos = self.real_line().p1().y() + self.__distanceY * dtext.text_position
        
        dtext.origin_pos = QPointF(xPos, yPos)
        
        if(self.__angle >= 0):
            if(dtext.text_orientation == -1):
                xPos -= self.__xmarg * 10
                yPos += self.__ymarg * 10
            else:
                xPos += self.__xmarg * 10
                yPos -= self.__ymarg * 10 + self.__fontMetrics.height()
        else:
            if(dtext.text_orientation == -1):
                xPos += -self.__xmarg * 10
                yPos += self.__ymarg * 10
            else:
                xPos -= self.__xmarg * 10
                yPos -= self.__ymarg * 10 + self.__fontMetrics.height()
                
        xPos -= self.__fontMetrics.width(text) / 2        
        
        # Reset pos if not visible.
        if(dtext.isVisible() == False):
            dtext.reset_pos()
            
        dtext.text = text
        dtext.setVisible(True)
    
    def paint(self, painter, style, widget):
        if(self.real_line().length() <= 0):
            return # nothing to draw (not really but we are better this way!)
        
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        myPen = self.pen()
        myPen.setColor(QColor(0, 0, 0))
        
        painter.setPen(myPen)
        painter.setBrush(QColor(255, 255, 255))
        
        painter.drawLine(self.real_line())

        if self.source_arrow:
            self.source_arrow.draw(painter, self.real_line().p1(), self.real_line())
        if self.target_arrow:
            self.target_arrow.draw(painter, self.real_line().p2(), self.real_line())
        
        painter.setRenderHint(QPainter.Antialiasing, False)
