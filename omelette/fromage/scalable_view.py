from PyQt4 import QtGui, QtCore
import math

class ScalableView(QtGui.QGraphicsView):
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self._current_center = QtCore.QPointF(0, 0)
        self.set_center(QtCore.QPointF(200, 200))

        """#pan point
        self.last_point = QtCore.QPoint(0, 0)
        self.setCursor(QtGui.QCursor(17))"""

        self._event_type = ""

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            event_type = "pressed"
            self.set_event_type(event_type)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            event_type = "release"
            self.set_event_type(event_type)

    def set_event_type(self, event_type):
        self._event_type = event_type

    def get_event_type(self):
        return self._event_type

    def get_center(self):
        return self._current_center

    def set_center(self, center):
        visible_area = self.mapToScene(self.rect()).boundingRect()
        scene_bounds = self.sceneRect()

        bound_x = visible_area.width() / 2.0
        bound_y = visible_area.height() / 2.0
        bound_w = scene_bounds.width() - 2.0 * bound_x
        bound_h = scene_bounds.height() - 2.0 * bound_y

        boundary = QtCore.QRectF(bound_x, bound_y, bound_w, bound_h)
        if boundary.contains(center):
            self._current_center = center
        else:
            if visible_area.contains(scene_bounds):
                self._current_center = scene_bounds.center()
            else:
                self._current_center = center

                if center.x() > boundary.x() + boundary.width():
                    self._current_center.setX(boundary.x() + boundary.width())
                elif center.x() < boundary.x():
                    self._current_center.setX(boundary.x())

                if center.y() > boundary.y() + boundary.height():
                    self._current_center.setY(boundary.y() + boundary.height())
                elif center.y() < boundary.y():
                    self._current_center.setY(boundary.y())

        self.centerOn(self._current_center)

    def wheelEvent(self, event):
        if self.get_event_type() == "pressed" and not self.get_event_type() == "release":
            point_before_scale = self.mapToScene(event.pos())
            screen_center = self.get_center()

            scale_factor = 1.15
            if event.delta() > 0:
                self.scale(scale_factor, scale_factor)
            else:
                self.scale(1.0 / scale_factor, 1.0 / scale_factor)

            point_after_scale = self.mapToScene(event.pos())
            offset = point_before_scale - point_after_scale
            new_center = screen_center + offset
            self.set_center(point_after_scale)#new_center)
        else:
            return

    def resizeEvent(self, event):
        visible_area = self.mapToScene(self.rect()).boundingRect()
        self.set_center(visible_area.center())

        super(ScalableView, self).resizeEvent(event)
"""
    def mousePressEvent(self, event):
        self.last_point = event.pos()
        self.setCursor(QtGui.QCursor(18))

    def mouseReleaseEvent(self, event):
        self.setCursor(QtGui.QCursor(17))
        self.last_point = QtCore.QPoint(0, 0)

    def mouseMoveEvent(self, event):
        if not self.last_point.isNull():
            delta = self.mapToScene(self.last_point) - self.mapToScene(event.pos())
            self.last_point = event.pos()

            self.set_center(self.get_center() + delta)
"""