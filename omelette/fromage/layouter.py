import math
import random

class Layouter(object):
    
    @staticmethod
    def __circular_layout(diagram, sx=0, sy=0, start=math.pi/2, spread=2):
        """
        Basic layout function placing all nodes on circle, adjusting
        circle range to size of nodes.
        """
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
        
    @staticmethod
    def __spring_layout(diagram, c1=2, c2=1, c3=1, c4=0.1, m=100):
        """
        Layout function using mechanical model of spring embedder.
        """
        maxrand = 300
        infinity = 200
#TODO set infinity as scene size
        # Incidence matrix
        incidence = Layouter.__incidence_matrix(diagram)
        embedder = Layouter.__init_spring_embedder(incidence, infinity)

        # Moving all nodes in random positions
        for node in diagram.nodes.values():
            node.moveBy(random.randint(0, maxrand),
                        random.randint(0,maxrand))

        # Calculating force for each node
        # Moving node

    @staticmethod
    def __sort_nodes_by_degree(nodes, rev=True):
        """
        Function sorting nodes in order of vertex grade
        """
        return sorted(nodes, key=Layouter.__node_degree, reverse=rev)
    
    @staticmethod
    def __sort_nodes_by_neighbourhood(nodes):
        """
        Function sorting nodes to have their neighbours on their both sides
        """
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
            
    @staticmethod
    def __node_degree(node):
        """
        Function calculating node's degree
        """
        return len(node.neighbours)
    
    @staticmethod
    def __incidence_matrix(diagram):
        """
        Function generating incidence matrix from given diagram
        """
        #initializing incidence array
        incidence = [[ 0 for row in range(len(diagram.nodes))]
                    for col in range(len(diagram.nodes)) ]
        #filling incidence array
        for node in diagram.nodes.values():
            for neigh in node.neighbours:
                incidence[diagram.nodes.values().index(node)][diagram.nodes.values().index(neigh)] = 1
        return incidence

    @staticmethod
    def __init_spring_embedder(incidence,inf=200):
        for i in range(len(incidence)):
            for j in range(len(incidence)):
                if incidence[i][j] == 0:
                    incidence[i][j] == inf
        return incidence
    
    @staticmethod
    def __max_size_of_drawable_node(nodes):
        """
        Function calculating maximal size of nodes in given list of nodes
        """
        maxwidth = maxheight = 0
        for node in nodes:
            if maxwidth < node.boundingRect().size().width():
                maxwidth = node.boundingRect().size().width()
            if maxheight < node.boundingRect().size().height():
                maxheight = node.boundingRect().size().height()
        return max(maxwidth, maxheight)
    
    @staticmethod
    def layout(diagram, mode=1):
        """
        General function calling different layout functions
        """
        if mode == 0:
            Layouter.__circular_layout(diagram)
        elif mode == 1:
            Layouter.__spring_layout(diagram)
