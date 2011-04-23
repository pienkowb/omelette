import math

class Layouter(object):

    @staticmethod
    def circular_layout(diagram):
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
                r = (spread * max(maxwidth, maxheight)
                    / math.sin( angle ))
            i = 0 # number of actual drawable
            # shifting coordinates to be positive
            sx = sy = r + max(maxwidth, maxheight)
            for node in diagram.nodes.values():
                # calculating xpos
                x = sx + r * math.sin(start + angle * i)
                # calculating ypos
                y = sy + r * math.cos(start + angle * i)
                i += 1
                node.moveBy(x, y)
        else:
            node.moveBy(sx, sy)
            
    @staticmethod
    def nodes_hash(diagram):
        hash = []
        for node in diagram.nodes.values():
            hash.append(node)
        return hash
    
    @staticmethod
    def incidence_matrix(diagram):
        #initializing incidence array
        incidence = [[ 0 for row in range(len(diagram.nodes))]
                    for col in range(len(diagram.nodes)) ]
        #enumerating nodes
        hash = Layouter.nodes_hash(diagram)
        #filling incidence array
        for node in diagram.nodes.values():
            for neigh in node.neighbours:
                incidence[hash.index(node)][hash.index(neigh)] = 1
        return incidence

    @staticmethod
    def layout(diagram):
        print Layouter.incidence_matrix(diagram)
        Layouter.circular_layout(diagram)