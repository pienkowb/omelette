import math

from omelette.fromage.common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QLineF
from PyQt4.Qt import *

class DrawableUseCase(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableUseCase, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)

        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)
        
    def boundingRect(self):
        return self.__boundingRect

    def paint(self, painter, style, widget):
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QBrush(QColor(255, 255, 255), Qt.SolidPattern))
        
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawEllipse(self.__boundingRect)
        painter.setRenderHint(QPainter.Antialiasing, False)
        
        painter.drawText(self.__text_rect, 0, self.uml_object['name'])
    
    def update(self):
        metrics = QFontMetrics(self.__font)
        textHeight = metrics.height()

        # TODO: This doesn't belong here. Or does it?
        if "name" not in self.uml_object.properties:
            self.uml_object["name"] = self.uml_object.name

        textWidth = metrics.width(self.uml_object['name'])

        ratio = (float(textWidth) / textHeight) / 1.5
        
        drawableHeight = textHeight * 2
        drawableWidth = ratio * drawableHeight
        
        if(ratio > 3.5):
            drawableHeight = drawableWidth / max(3.5, ratio/3)
        elif(ratio < 1):
            drawableWidth = drawableHeight * 1.2

        self.__text_rect = QRectF((drawableWidth - textWidth) / 2,
                                  (drawableHeight - textHeight) / 2,
                                  textWidth, textHeight)

        self.__boundingRect = QRectF(0, 0, drawableWidth, drawableHeight)

    def crop_line(self, line, line_point):
        global_rect = self.globalBoundingRect()
        
        # Go to local coordinate system - ellipse equations assume ellipse is centered on (0,0)        
        local_trans = global_rect.center()
        local_line = QLineF(line.p1() - local_trans, line.p2() - local_trans)
        
        if(local_line.dx() == 0):
            return line
        
        # Solve line equation        
        e_a = ((local_line.p2().y() - local_line.p1().y()) / 
                  (local_line.p2().x() - local_line.p1().x()))
        
        e_b = local_line.p1().y() - e_a * local_line.p1().x()
        
        # ellipse params 
        e_c = global_rect.width()/2
        e_d = global_rect.height()/2
        
        # check condition
        if(e_c * e_d == 0):
            return line
        
        # precalculate things that are used more than once
        # a^2, b^2 ...
        ak = math.pow(e_a, 2)
        bk = math.pow(e_b, 2)
        ck = math.pow(e_c, 2)
        dk = math.pow(e_d, 2)
        
        # check another condition
        if((ak * ck + dk) == 0):
            return line
        
        # a^2*c^2, c^2*d^2
        akck = ak * ck
        ckdk = ck * dk
        
        # a*b*c^2
        abck = e_a*e_b*ck
        
        # parts of denomiator and numerator of x
        denom = (akck + dk)
        numer =  math.sqrt(ck*dk*(akck-bk+dk))
        
        # Decide which points to take
        xrel = (line.p1().x() > line.p2().x())
        yrel = (line.p1().y() > line.p2().y())
        
        if(line_point != 0):
            xrel = not xrel
            yrel = not yrel
        
        if((xrel and yrel) or (xrel and not yrel)):
            x1 = (-numer - abck) / denom
            y1 = (e_b*dk - e_a*math.sqrt(-ckdk*(-akck+bk-dk))) / denom
            
            intersectionPoint = QPointF(x1, y1)
        elif((not xrel and yrel) or (not xrel and not yrel)):
            x2 = (numer - abck) / denom         
            y2 = -(e_b*dk - e_a*math.sqrt(-ckdk*(-akck+bk-dk))) / denom  
        
            intersectionPoint = QPointF(x2, y2)
    
        # Go back to global coordinate system
        intersectionPoint = intersectionPoint + local_trans
    
        if(line_point == 0):
            return QLineF(intersectionPoint, line.p2())
        else:
            return QLineF(line.p1(), intersectionPoint)  
        
        return line
        
    def find_anchor(self):
        return self.globalBoundingRect().center()

    def itemChange(self, change, value):
        if(change == QGraphicsItem.ItemPositionChange):
            for anchor in self.anchors:
                anchor.connector.update()
                
                self.resize_scene_rect()
                
        return QGraphicsItem.itemChange(self, change, value)