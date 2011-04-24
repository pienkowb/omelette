import math

class Layouter(object):
    
    """
    Basic layout function placing all nodes on circle, adjusting
    circle range to size of nodes.
    """
    @staticmethod
    def circular_layout(diagram, sx=0, sy=0, start=math.pi/2, spread=2):
#        sx = sy = 200 # Defining center of circle
        r = 0
        maxwidth = maxheight = 0
#        start = math.pi / 2 # Starting angle
#        spread = 2 # Diagram nodes spread factor
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
            # shifting coordinates to be positive
            sx = r + max(maxwidth, maxheight) - sx
            sy = r + max(maxwidth, maxheight) - sy
            sortednodes = []
            
            #TODO dopisac sortowanie po stopniu wierzcholka
            d = 0
            while d < len(diagram.nodes):
                for node in diagram.nodes.values():
                    if not node in sortednodes:
                        sortednodes.append(node)
                        d += 1
                        for node in sortednodes:
                            i = 0
                            for neigh in node.neighbours:
                                if not neigh in sortednodes:
                                    sortednodes.insert(sortednodes.index(node) + pow(-1,i), neigh)
                                    d += 1
                                    i += 1
            i = 0
            for node in sortednodes:
                # calculating xpos
                x = sx + r * math.sin(start + angle * i)
                # calculating ypos
                y = sy + r * math.cos(start + angle * i)
                i += 1
                node.moveBy(x, y)
        else:
            node.moveBy(sx, sy)

    """
    Function generating incidence matrix from given diagram.
    """
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
                incidence[diagram.nodes.values().index(node)][diagram.node.values().index(neigh)] = 1
        return incidence
    
    """
    General function calling different layout functions.
    """
    @staticmethod
    def layout(diagram, mode=0):
        if(mode == 0):
            Layouter.circular_layout(diagram)