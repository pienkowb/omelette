import math
class Layouter(object):
    @staticmethod
    def layout(diagram):
        sx = sy = 200 # Defining center of circle
	r = 0
	maxwidth = maxheight = 0
	start = math.pi / 2 # Starting angle
	spread = 2 # Diagram nodes spread factor
	for node in diagram.nodes.values(): # Finding max size of drawable
		if maxwidth < node.boundingRect().size().width():
			maxwidth = node.boundingRect().size().width()
		if maxheight < node.boundingRect().size().height():
			maxheight = node.boundingRect().size().height()
	n = len(diagram.nodes) # number of drawables
	if n > 1:
		angle = 2 * math.pi / n # calculating angle step
		if angle % math.pi == 0:
			r = spread * max(maxwidth, maxheight)
		else:
			r = spread * max(maxwidth, maxheight) / math.sin( angle )
		i = 0 # number of actual drawable
		# shifting coordinates
		sx = sy = r + max(maxwidth, maxheight);
		for node in diagram.nodes.values():
			# calculating xpos
			x = sx + r * math.sin(start + angle * i)
			# calculating ypos
			y = sy + r * math.cos(start + angle * i)
			i += 1
			node.moveBy(x, y)
	else:
		node.moveBy(sx, sy)
