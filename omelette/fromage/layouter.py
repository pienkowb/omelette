class Layouter(object):
    @staticmethod
    def layout(diagram):
	print "hello"
        sx = sy = 0
        left = bottom = 0
	r = 0
	greatestwidth = max( diagram.nodes.values().boundingRect().size().width() )
	greatestheight = max( diagram.nodes.values().boundingRect().size().height() )
	r = 2 * max( greatestwidth, greatestheight )
	print r
	n = diagram.nodes.len()
	rad = 2 * math.pi / n
	print rad
	i = 0
	for node in diagram.nodes.values():
            x = sx + r * math.sin( rad * i )
	    y = sy + r * math.cos( rad * i++ )
	    print "(%f, %f)" % (x, y)
	    node.moveBy(x, y)
