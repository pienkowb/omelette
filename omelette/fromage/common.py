class Drawable(object):
    """
    Base for other Drawable objects. It's made with UMLObject, and
    provides interface for accessing its attributes, properties and
    operations. Properties are accessible via [] operator.
    """

    def __init__(self, uml_object):
        self.__uml_object = uml_object
    
    def __setitem__(self, key, value):
        self.__uml_object[key] = value
        
    def __getitem__(self, key):
        return self.__uml_object[key]
        
    def attributes(self):
        return self.__uml_object.attributes()
        
    def operations(self):
        return self.__uml_object.operations()
    
    def __get_root(self):
        return self.__uml_object.root
    
    def __set_root(self, value):
        self.__uml_object.root = value
        
    root = property(__get_root, __set_root)
    
    def addToScene(self, scene):
        scene.addItem(self)

class DrawableEdge(Drawable):
    def __init__(self, uml_object):
        super(DrawableEdge, self).__init__(uml_object)
        self.__source_anchor = None
        self.__target_anchor = None
        
    def __get_source_anchor(self):
        return self.__source_anchor
    
    def __set_source_anchor(self, value):
        self.__source_anchor = value
    
    def __get_target_anchor(self):
        return self.__target_anchor
    
    def __set_target_anchor(self, value):
        self.__target_anchor = value
        
    source_anchor = property(__get_source_anchor, __set_source_anchor)
    target_anchor = property(__get_target_anchor, __set_target_anchor)
        
        
class DrawableNode(Drawable):
    def __init__(self, uml_object):
        super(DrawableNode, self).__init__(uml_object)
    
    def __set_position(self, position):
        self.__position = position
        
    def __get_position(self):
        return self.__position
    
    position = property(__get_position, __set_position)

