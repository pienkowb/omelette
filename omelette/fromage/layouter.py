import math
class Layouter(object):
    @staticmethod
    def layout(diagram):
#TODO add parameter for start angle
#TODO tidy up comments
#TODO refactor code
        sx = sy = 200 #Defining center of circle
	r = 0
	greatestwidth = greatestheight = 0
	for node in diagram.nodes.values(): #Finding greatest size of drawable
		if greatestwidth < node.boundingRect().size().width():
			greatestwidth = node.boundingRect().size().width()
		if greatestheight < node.boundingRect().size().height():
			greatestheight = node.boundingRect().size().height()
	n = len(diagram.nodes) #number of drawables
	if n > 1:
		rad = 2 * math.pi / n #calculating angle
		if math.sin( rad ) < 0.1:
			r = 2 * max( greatestwidth, greatestheight )
		else:
			r = 2 * max( greatestwidth, greatestheight ) / math.sin( rad )
		i = 0 #number of actual drawable
		for node in diagram.nodes.values():
			x = sx + r * math.sin( rad * i ) #calculating xpos
			y = sy + r * math.cos( rad * i ) #calculating ypos
			i += 1
			node.moveBy(x, y)
	else:
		node.moveBy(sx, sy)
