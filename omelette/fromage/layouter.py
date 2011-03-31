import math
class Layouter(object):
    @staticmethod
    def layout(diagram):
        sx = sy = 200 %Defining center of circle
	r = 0
	greatestwidth = greatestheight = 0
	for node in diagram.nodes.values(): %Finding greatest size of drawable
		if greatestwidth < node.boundingRect().size().width():
			greatestwidth = node.boundingRect().size().width()
		if greatestheight < node.boundingRect().size().height():
			greatestheight = node.boundingRect().size().height()
	r = 2 * max( greatestwidth, greatestheight )
	n = len(diagram.nodes) %number of drawables
	rad = 2 * math.pi / n %calculating radian
	i = 0 %number of actual drawable
	for node in diagram.nodes.values():
            x = sx + r * math.sin( rad * i ) %calculating xpos
	    y = sy + r * math.cos( rad * i ) %calculating ypos
	    i += 1
	    node.moveBy(x, y)
