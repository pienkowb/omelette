from omelette.fromage.common import *

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QLineF
from PyQt4.Qt import *

class DrawableClass(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableClass, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__bounding_rect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)
        self.__section_margin = 5
        self.__text_margin = 3
        self.__min_width = 100 

        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)

    def boundingRect(self):
        return self.__bounding_rect

    def __draw_oa(self, painter, current_height, list):
        """ Used to draw operation or attribute list """
        metrics = QFontMetrics(self.__font)
        for obj in list:
            # TODO: Make font changing less ugly
            if(obj.is_static):
                font = painter.font()
                font.setUnderline(True)
                painter.setFont(font)
            
            painter.drawText(QRect(self.__text_margin, current_height, metrics.width(str(obj)), metrics.height()), 0, str(obj))
            
            # Set font back to non-underlined
            if(obj.is_static):
                font = painter.font()
                font.setUnderline(False)
                painter.setFont(font)
                
            current_height += self.__text_margin + metrics.height() 
            
        return current_height

    def paint(self, painter, style, widget):
        metrics = QFontMetrics(self.__font)
        painter.setFont(self.__font)
        painter.setPen(QColor(0, 0, 0))
        painter.fillRect(QRectF(self.__bounding_rect), QBrush(QColor(255, 255, 255), Qt.SolidPattern))

        # Name of the class        
        current_height = self.__section_margin
        painter.drawText(QRect(self.__text_margin, current_height, self.__bounding_rect.width() - self.__text_margin * 2, metrics.height()), Qt.AlignCenter, self.uml_object['name'])
        current_height += metrics.height()
        
        # Stereotype
        if("stereotype" in self.uml_object.properties):
            current_height += self.__text_margin
            stereotype = "<< " + self.uml_object["stereotype"] + " >>"
            painter.drawText(QRect(self.__text_margin, current_height, self.__bounding_rect.width() - self.__text_margin * 2, metrics.height()), Qt.AlignCenter, stereotype)
            current_height += metrics.height()
            
        current_height += self.__section_margin
        
        # Attributes section
        painter.drawLine(0, current_height, self.__bounding_rect.width(), current_height)
        current_height += self.__section_margin
        
        current_height = self.__draw_oa(painter, current_height, self.uml_object.attributes()) 
        
        # Operations section
        painter.drawLine(0, current_height, self.__bounding_rect.width(), current_height)
        
        current_height += self.__section_margin
        current_height = self.__draw_oa(painter, current_height, self.uml_object.operations())

        painter.drawRect(self.__bounding_rect)

    def __size_of_section(self, metrics, list):
        """ Used to determine size of section - attribute or operation list. """
        count = 0
        maxWidth = 0
        for text in list:
            maxWidth = max(maxWidth, 2 * self.__text_margin + metrics.width(text))
            count += 1

        return (maxWidth, 2 * self.__section_margin + (count - 1) * self.__text_margin + count * metrics.height())

    def update(self):
        metrics = QFontMetrics(self.__font)
        # Start by finding size of class name block
        drawable_height = 1 * self.__section_margin + metrics.height()

        # TODO: This doesn't belong here. Or does it?
        if "name" not in self.uml_object.properties:
            self.uml_object["name"] = self.uml_object.name

        drawable_width = 2 * self.__text_margin + metrics.width(self.uml_object['name'])
        
        # Add stereotype height
        if("stereotype" in self.uml_object.properties):
            drawable_height += self.__text_margin + metrics.height()
            
            stereotypeWidth = 2 * self.__text_margin + metrics.width("<< " + self.uml_object['stereotype'] + " >>")
            drawable_width = max(drawable_width, stereotypeWidth)

        # Find sizes of each section and update width/height
        for section in [map(str, self.uml_object.operations()), map(str,
                                                                    self.uml_object.attributes())]:
            size = self.__size_of_section(metrics, section)
            drawable_width = max(drawable_width, size[0])
            drawable_height += size[1]

        self.__bounding_rect = QRectF(0, 0, max(2 * self.__text_margin + drawable_width, self.__min_width), drawable_height)

    def crop_line(self, line, line_point):
        global_rect = self.globalBoundingRect()
        
        vertexes = [global_rect.topLeft(), global_rect.topRight(),
                  global_rect.bottomRight(), global_rect.bottomLeft()]
        
        intersection_point = QPointF()
        
        # Iterate over pairs of vertices that make rectangle edges
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
