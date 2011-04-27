import math

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QLineF
from PyQt4.Qt import *

from omelette.fromage.common import *
from omelette.fromage.diagramcommon import DrawableText

class DrawableActor(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableActor, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__bounding_rect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)
        self.__sectionMargin = 5
        self.__text_margin = 3

        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)
        
        self.__actor_rectangle = QRectF(0, 0, 40, 80)
        
        self.__actor_name_text = DrawableText.create_drawable_text(self)

    def boundingRect(self):
        return self.__bounding_rect

    def paint(self, painter, style, widget):
        metrics = QFontMetrics(self.__font)
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))
        painter.fillRect(QRectF(self.__bounding_rect), QBrush(QColor(255, 255, 255), Qt.SolidPattern))

        painter.setRenderHint(QPainter.Antialiasing, True)
        
        head_rad = math.ceil(self.__actor_rectangle.height() / 3)
        center = self.__actor_rectangle.width() / 2
        head_start = center - head_rad / 2
        
        painter.drawEllipse(head_start,0,head_rad,head_rad)
        
        painter.drawLine(0, head_rad * 1.3, self.__actor_rectangle.width(), head_rad * 1.3)
        painter.drawLine(center, head_rad, center, head_rad*2)
        
        painter.drawLine(center, head_rad * 2, 0, self.__actor_rectangle.height())
        painter.drawLine(center, head_rad * 2, self.__actor_rectangle.width(), self.__actor_rectangle.height())
        
        painter.setRenderHint(QPainter.Antialiasing, False)
        

    def update(self):
        metrics = QFontMetrics(self.__font)
        
        self.__bounding_rect = QRectF(self.__actor_rectangle)
        globalRect = self.globalBoundingRect()
        
        # TODO: This again
        if "name" not in self.uml_object.properties:
            self.uml_object["name"] = self.uml_object.name
            
        self.__actor_name_text.text = self.uml_object["name"]
        self.__actor_name_text.origin_pos = QPointF(globalRect.x() + globalRect.width() / 2, 
                                                    globalRect.y() + globalRect.height())
        self.__actor_name_text.reset_vector = QPointF(- metrics.width(self.uml_object["name"]) / 2, 0)
        if(not self.__actor_name_text.isVisible()):
            self.__actor_name_text.reset_pos()
            self.__actor_name_text.setVisible(True)            

    def crop_line(self, line, line_point):
        global_rect = self.globalBoundingRect()
        
        vertexes = [global_rect.topLeft(), global_rect.topRight(),
                  global_rect.bottomRight(), global_rect.bottomLeft()]
        
        intersection_point = QPointF()
        
        # Iterate over pairs of vertexes that make rectangle edges
        for (a, b) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
            bok = QLineF(vertexes[a], vertexes[b])
            itype = line.intersect(bok, intersection_point)
            if(itype == QLineF.BoundedIntersection):
                if(line_point == 0):
                    return QLineF(intersection_point, line.p2())
                else:
                    return QLineF(line.p1(), intersection_point)
        
        return line
        
    def find_anchor(self):
        return self.globalBoundingRect().center()

    def itemChange(self, change, value):
        if(change == QGraphicsItem.ItemPositionChange):
            for anchor in self.anchors:
                anchor.connector.update()
                self.resize_scene_rect()
                
        return QGraphicsItem.itemChange(self, change, value)
