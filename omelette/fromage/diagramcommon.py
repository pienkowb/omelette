from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF
from PyQt4.Qt import *

class DrawableText(QGraphicsItem):
    def __init__(self, parentItem):
        QGraphicsItem.__init__(self)
        self.__parentItem = parentItem
        self.__font = QFont('Comic Sans MS', 10)
        self.__text = ""
        
        self.__extraFrame = 1
        
        self.setZValue(1)
        
        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)

    def boundingRect(self):
        metrics = QFontMetrics(self.__font)
        return QRectF(0, 0, metrics.width(self.__text), metrics.height()).adjusted(
            0, 0, 2 * self.__extraFrame, 2 * self.__extraFrame)
    
    def paint(self, painter, style, widget):
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))
        
        painter.fillRect(self.boundingRect(), QBrush(QColor(255,255,255)))
        painter.drawText(self.boundingRect().translated(self.__extraFrame, self.__extraFrame), 0, self.__text)
        
    def itemChange(self, change, value):
        if(change == QGraphicsItem.ItemPositionChange):
            pass
                
        return QGraphicsItem.itemChange(self, change, value)
    
    
    def __get_text(self):
        return self.__text
    
    def __set_text(self, value):
        self.__text = value
        #TODO: Save boundingRect here
        
    text = property(__get_text, __set_text)
        