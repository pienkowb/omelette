from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF
from PyQt4.Qt import *

class DrawableText(QGraphicsItem):
    
    def __init__(self, parentItem):
        QGraphicsItem.__init__(self)
        self.setParentItem(parentItem)
        self.__font = QFont('Comic Sans MS', 10)
        self.__text = ""
        
        self.__extraFrame = 1
        
        self.setZValue(1)
        
        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)

    def boundingRect(self):
        metrics = QFontMetrics(self.__font)
        return (QRectF(0, 0, metrics.width(self.__text), metrics.height())
                .adjusted(0, 0, 2 * self.__extraFrame, 2 * self.__extraFrame)
                .united(QRectF(QPointF(0,0), self.__get_local_origin())))
    
    def paint(self, painter, style, widget):
        painter.setFont(self.__font)
        painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.DotLine))
        
        metrics = QFontMetrics(self.__font)
        
        painter.drawLine(QLineF(QPointF(metrics.width(self.__text) / 2, metrics.height() / 2), QPointF(self.__get_local_origin())))
        
        text_rect = QRectF(0, 0, metrics.width(self.__text), metrics.height()).adjusted(0, 0, 2 * self.__extraFrame, 2 * self.__extraFrame)
        painter.fillRect(text_rect, QBrush(QColor(255,255,255)))
        painter.drawText(text_rect.translated(self.__extraFrame, self.__extraFrame), 0, self.__text)
        
    def itemChange(self, change, value):
        if(change == QGraphicsItem.ItemPositionChange):
            pass
                
        return QGraphicsItem.itemChange(self, change, value)
    
    def __get_text(self):
        return self.__text
    
    def __set_text(self, value):
        self.__text = value
        #TODO: Cache boundingRect here
        
    text = property(__get_text, __set_text)

    def __get_origin(self):
        return self.__origin_pos
    
    def __get_local_origin(self):
        return self.__origin_pos - self.pos()
    
    def __set_origin(self, value):
        self.__origin_pos = value
        #TODO: Cache boundingRect here too
        
    origin_pos = property(__get_origin, __set_origin)
