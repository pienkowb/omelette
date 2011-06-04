from omelette.fromage.common import *

import math

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QLineF
from PyQt4.Qt import *

class DrawableNote(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableNote, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__bounding_rect = QRectF(0, 0, 100, 100)
        self.__font = Drawable.get_font()
        self.__text_margin = 3
        self.__note_margin = 10

        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)

    def boundingRect(self):
        return self.__bounding_rect

    def paint(self, painter, style, widget):
        metrics = QFontMetrics(self.__font)
        
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))
        painter.fillRect(QRectF(self.__bounding_rect), QBrush(QColor(255, 255, 255), Qt.SolidPattern))
        
        # Draw folded corner first
        painter.drawLine(self.__bounding_rect.width() - self.__note_margin, 0, self.__bounding_rect.width(), self.__note_margin)
        painter.drawLine(self.__bounding_rect.width() - self.__note_margin, 0, self.__bounding_rect.width() - self.__note_margin, self.__note_margin)
        painter.drawLine(self.__bounding_rect.width() - self.__note_margin, self.__note_margin, self.__bounding_rect.width(), self.__note_margin)
        
        text_rect = QRect(self.__text_margin, self.__text_margin, self.__bounding_rect.width() - self.__note_margin, self.__bounding_rect.height())
        
        if('text' in self.uml_object):
            painter.drawText(text_rect, Qt.TextWordWrap, self.uml_object['text'])
        
        painter.drawLine(0, 0, self.__bounding_rect.width() - self.__note_margin, 0)
        painter.drawLine(0, 0, 0, self.__bounding_rect.height())
        painter.drawLine(0, self.__bounding_rect.height(), self.__bounding_rect.width(), self.__bounding_rect.height())
        painter.drawLine(self.__bounding_rect.width(), self.__note_margin, self.__bounding_rect.width(), self.__bounding_rect.height())
        
    def update(self):
        metrics = QFontMetrics(self.__font)
        
        if('text' in self.uml_object):
            text = self.uml_object['text']
            width = metrics.width(text)
            height = metrics.height()
            
            rect_ratio = (width / height) * 0.337 # LOL MAGIC NUMBER
            rect_ratio = min(10, rect_ratio)
            
            note_width = height * rect_ratio
            note_height = 2 * note_width / height # no higher than that
            
            self.__bounding_rect = QRectF(metrics.boundingRect(QRect(0,0, note_width, note_height), Qt.TextWordWrap | Qt.TextDontClip, text)
                                    .adjusted(0, 0, 2 * self.__text_margin + self.__note_margin, 2 * self.__text_margin))
        else:
            self.__bounding_rect = QRectF(0,0,50,50)
            
    def itemChange(self, change, value):        
        if(change == QGraphicsItem.ItemPositionChange):
            for anchor in self.anchors:
                anchor.connector.update()
                
            self.resize_scene_rect()
                
        return QGraphicsItem.itemChange(self, change, value)
    
    def crop_line(self, line, line_point):
        global_rect = self.globalBoundingRect()
        
        vertexes = [global_rect.topLeft(), global_rect.topRight(),
                  global_rect.bottomRight(), global_rect.bottomLeft(),
                  
                  # Folded corner
                  QPointF(global_rect.topRight().x() - self.__note_margin, global_rect.topRight().y()), 
                  QPointF(global_rect.topRight().x(), global_rect.topRight().y() + self.__note_margin)
                  ]
                
        intersection_point = QPointF()
        
        # Iterate over pairs of vertices that make rectangle edges
        # Check folded corner first and we don't have to crop
        # rest of the edges. 
        for (a, b) in [(4, 5), (0, 1), (1, 2), (2, 3), (3, 0)]:
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