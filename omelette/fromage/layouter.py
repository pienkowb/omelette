import math

class Layouter(object):
    
    """
    Basic layout function placing all nodes on circle, adjusting
    circle range to size of nodes.
    """
    @staticmethod
    def __circular_layout(diagram, sx=0, sy=0, start=math.pi/2, spread=2):
        r = 0
        # Finding max size of drawable
        maxsize = Layouter.__max_size_of_drawable_node(diagram.nodes.values())
        n = len(diagram.nodes) # number of drawables
        if n > 1:
            angle = 2 * math.pi / n # calculating angle step
            if angle % math.pi == 0:
                r = spread * maxsize
            else:
                r = (spread * maxsize
                    / math.sin( angle ))
            # shifting coordinates to be positive
            sx = r + maxsize - sx
            sy = r + maxsize - sy
            sortednodes = Layouter.__sort_nodes_by_neighbourhood(diagram.nodes.values())
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
    Function sorting nodes in order of vertex grade
    """
    @staticmethod
    def __sort_nodes_by_degree(nodes, rev=True):
        return sorted(nodes, key=Layouter.__node_degree, reverse=rev)
    
    """
    Function sorting nodes to have their neighbours on their both sides
    """
    @staticmethod
    def __sort_nodes_by_neighbourhood(nodes):
        sortednodes = []
        d = 0 # number of sorted nodes
        while d < len(nodes):
            for node in nodes:
                if not node in sortednodes:
                    sortednodes.append(node)
                    d += 1
                    for node in sortednodes:
                        i = 0 # sorted neighbours counter
                        for neigh in node.neighbours:
                            if not neigh in sortednodes:
                                # neighbour is placed on the right or on the left of node
                                sortednodes.insert(sortednodes.index(node) + pow(-1,i), neigh)
                                d += 1
                                i += 1
        return sortednodes
            
    """
    Function calculating node's degree
    """
    @staticmethod
    def __node_degree(node):
        return len(node.neighbours)
    
    """
    Function generating incidence matrix from given diagram
    """
    @staticmethod
    def __incidence_matrix(diagram):
        #initializing incidence array
        incidence = [[ 0 for row in range(len(diagram.nodes))]
                    for col in range(len(diagram.nodes)) ]
        #filling incidence array
        for node in diagram.nodes.values():
            for neigh in node.neighbours:
                incidence[diagram.nodes.values().index(node)][diagram.nodes.values().index(neigh)] = 1
        return incidence
    
    """
    Function calculating maximal size of nodes in given list of nodes
    """
    @staticmethod
    def __max_size_of_drawable_node(nodes):
        maxwidth = maxheight = 0
        for node in nodes:
            if maxwidth < node.boundingRect().size().width():
                maxwidth = node.boundingRect().size().width()
            if maxheight < node.boundingRect().size().height():
                maxheight = node.boundingRect().size().height()
        return max(maxwidth, maxheight)
    
    """
    General function calling different layout functions
    """
    @staticmethod
    def layout(diagram, mode=0):
        if(mode == 0):
            Layouter.__circular_layout(diagram)