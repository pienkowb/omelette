from omelette.fromage.common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QLineF
from PyQt4.Qt import *

class DrawableClass(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableClass, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)
        self.__sectionMargin = 5
        self.__textMargin = 3

        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)

    def boundingRect(self):
        return self.__boundingRect

    def __draw_oa(self, painter, current_height, list):
        metrics = QFontMetrics(self.__font)
        for obj in list:       
            print str(obj) + " " + str(obj.is_static)    
            if(obj.is_static):
                font = painter.getFont()
                font.setUnderline(True)
                painter.setFont(font)                
            
            painter.drawText(QRect(self.__textMargin, current_height, metrics.width(str(obj)), metrics.height()), 0, str(obj))
            
            # Set font back to non-underlined
            if(obj.is_static):
                font = painter.getFont()
                font.setUnderline(False)
                painter.setFont(font)
                
            current_height += self.__textMargin + metrics.height() 
            
        return current_height

    def paint(self, painter, style, widget):
        metrics = QFontMetrics(self.__font)
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))
        painter.fillRect(QRectF(self.__boundingRect), QBrush(QColor(255, 255, 255), Qt.SolidPattern))

        # Name of the class        
        currentHeight = self.__sectionMargin
        painter.drawText(QRect(self.__textMargin, currentHeight, metrics.width(self.uml_object['name']), metrics.height()), 0, self.uml_object['name'])
        currentHeight += metrics.height()
        
        # Stereotype
        if("stereotype" in self.uml_object.properties):
            currentHeight += self.__textMargin
            stereotype = "<< " + self.uml_object["stereotype"] + " >>"
            painter.drawText(QRect(self.__textMargin, currentHeight, metrics.width(stereotype), metrics.height()), 0, stereotype)
            currentHeight += metrics.height()
            
        currentHeight += self.__sectionMargin
        
        # Attributes section
        painter.drawLine(0, currentHeight, self.__boundingRect.width(), currentHeight)
        currentHeight += self.__sectionMargin
        
        currentHeight = self.__draw_oa(painter, currentHeight, self.uml_object.attributes()) 
        
        # Operations section
        painter.drawLine(0, currentHeight, self.__boundingRect.width(), currentHeight)
        
        currentHeight += self.__sectionMargin
        currentHeight = self.__draw_oa(painter, currentHeight, self.uml_object.operations())

        painter.drawRect(self.__boundingRect)

    def __sizeOfSection(self, metrics, list):
        count = 0
        maxWidth = 0
        for text in list:
            maxWidth = max(maxWidth, 2 * self.__textMargin + metrics.width(text))
            count += 1

        return (maxWidth, 2 * self.__sectionMargin + (count - 1) * self.__textMargin + count * metrics.height())

    def update(self):
        metrics = QFontMetrics(self.__font)
        # Start by finding size of class name block
        drawableHeight = 1 * self.__sectionMargin + metrics.height()

        # TODO: This doesn't belong here. Or does it?
        if "name" not in self.uml_object.properties:
            self.uml_object["name"] = self.uml_object.name

        drawableWidth = 2 * self.__textMargin + metrics.width(self.uml_object['name'])
        
        # Add stereotype height
        if("stereotype" in self.uml_object.properties):
            drawableHeight += self.__textMargin + metrics.height()
            
            stereotypeWidth = 2 * self.__textMargin + metrics.width("<< " + self.uml_object['stereotype'] + " >>")
            drawableWidth = max(drawableWidth, stereotypeWidth)

        # Find sizes of each section and update width/height
        for section in [map(str, self.uml_object.operations()), map(str,
                                                                    self.uml_object.attributes())]:
            size = self.__sizeOfSection(metrics, section)
            drawableWidth = max(drawableWidth, size[0])
            drawableHeight += size[1]

        self.__boundingRect = QRectF(0, 0, 2 * self.__textMargin + drawableWidth, drawableHeight)

    def crop_line(self, line, line_point):
        global_rect = self.globalBoundingRect()
        
        vertexes = [global_rect.topLeft(), global_rect.topRight(),
                  global_rect.bottomRight(), global_rect.bottomLeft()]
        
        intersectionPoint = QPointF()
        
        # Iterate over pairs of vertexes that make rectangle edges
        for (a, b) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
            bok = QLineF(vertexes[a], vertexes[b])
            itype = line.intersect(bok, intersectionPoint)
            if(itype == QLineF.BoundedIntersection):
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
