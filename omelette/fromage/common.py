class Drawable(object):
    '''
    Base for other Drawable objects. It's made with UMLObject, and
    provides interface for accessing its attributes, properties and
    attributes.
    '''

    def __init__(self, umlObject):
        self.__uml_object = umlObject
    
    def __setitem__(self, key, value):
        self.__uml_object[key] = value
        
    def __getitem__(self, key):
        return self.__uml_object[key]
        
    def attributes(self):
        return self.__uml_object.attributes()
        
    def operations(self):
        return self.__uml_object.operations()


class DrawableEdge(Drawable):
    def __init__(self, uml_object):
        super(DrawableEdge,self).__init__(umlObject)
        self.source_anchor = None
        self.target_anchor = None
        
        
class DrawableNode(Drawable):
    def __init__(self, umlObject):
        super(DrawableNode,self).__init__(umlObject)
    
    def set_position(self,pos):
        self.__position = pos
        
    def get_position(self):
        return self.__position

