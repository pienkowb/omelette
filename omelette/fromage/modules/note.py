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
        self.__font = QFont('Comic Sans MS', 10)
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
        
        painter.drawLine(self.__bounding_rect.width() - self.__note_margin, 0, self.__bounding_rect.width(), self.__note_margin)
        painter.drawLine(self.__bounding_rect.width() - self.__note_margin, 0, self.__bounding_rect.width() - self.__note_margin, self.__note_margin)
        painter.drawLine(self.__bounding_rect.width() - self.__note_margin, self.__note_margin, self.__bounding_rect.width(), self.__note_margin)
        
        text_rect = QRect(self.__text_margin, self.__text_margin, self.__bounding_rect.width() - self.__note_margin, self.__bounding_rect.height())
        
        painter.drawText(text_rect, Qt.TextWordWrap, self.uml_object['text'])
        
        painter.drawLine(0, 0, self.__bounding_rect.width() - self.__note_margin, 0)
        painter.drawLine(0, 0, 0, self.__bounding_rect.height())
        painter.drawLine(0, self.__bounding_rect.height(), self.__bounding_rect.width(), self.__bounding_rect.height())
        painter.drawLine(self.__bounding_rect.width(), self.__note_margin, self.__bounding_rect.width(), self.__bounding_rect.height())
        
    def update(self):
        metrics = QFontMetrics(self.__font)
        
        text = self.uml_object['text']
        width = metrics.width(text)
        height = metrics.height()
        
        rect_ratio = (width / height) * 0.337 # LOL MAGIC NUMBER
        
        note_width = height * rect_ratio
        note_height = 2 * note_width / height # no higher than that
        
        print "%d %d %d" % (rect_ratio, note_width, note_height)
        
        self.__bounding_rect = QRectF(metrics.boundingRect(QRect(0,0, note_width, note_height), Qt.TextWordWrap | Qt.TextDontClip, text)
                                .adjusted(0, 0, 2 * self.__text_margin + self.__note_margin, 2 * self.__text_margin))
        
        print "real: %d" % (self.__bounding_rect.width())
        
    def itemChange(self, change, value):        
        if(change == QGraphicsItem.ItemPositionChange):
            for anchor in self.anchors:
                anchor.connector.update()
                
            self.resize_scene_rect()
                
        return QGraphicsItem.itemChange(self, change, value)