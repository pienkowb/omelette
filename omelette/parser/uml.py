class UMLObject(object):
    """
    Class representing UML diagram object.
    """
  
    def __init__(self):
        self.__operations = []
        self.__attributes = []
        self.__properties = {}
        
    def __setitem__(self, key, value):
        self.__properties[key] = value
        
    def __getitem__(self, key):
        return self.__properties[key]

    def add_operation(self, operation):
        self.__operations.append(UMLOperation(operation))

    def add_attribute(self, attribute):
        self.__attributes.append(UMLAttribute(attribute))
        
    def operations(self):
        ops = self.__operations
        ops.sort()
        return map(str, ops)
        
    def attributes(self):
        attrs = self.__attributes
        attrs.sort()
        return map(str, attrs)
                    
                    
class _ScopedThing(object):    
    """
    Helper class used in UMLObject. Provides __cmp__ for methods and attributes.
    """
    
    scope_order = ["+","~","#","-"]
    
    def __init__(self,string):
        self.str = string
        self.scope = self.__get_scope()
        self.identifier = self.__get_identifier()
        
    def __get_scope(self):
        return self.str[0]
    
    def __get_identifier(self):
        return self.str[1:]
    
    def __str__(self):
        return self.str
        
    def __cmp__(self,other):
        result = self.__cmp_by_scope(other)
        return result or cmp(self.identifier, other.identifier)
    
    def __cmp_by_scope(self,other):
        order = _ScopedThing.scope_order
        return  order.index(self.scope) - \
                order.index(other.scope)
                
class UMLOperation(_ScopedThing):
    """Class representing UML Operation"""
    pass

class UMLAttribute(_ScopedThing):
    """Class representing UML Attribute"""
    pass
    
