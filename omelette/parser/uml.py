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
        operations = self.__operations
        operations.sort()
        return map(str, operations)
        
    def attributes(self):
        attributes = self.__attributes
        attributes.sort()
        return map(str, attributes)
                    
                    
class _Field(object):    
    """
    Helper class used in UMLObject. Provides __cmp__ for methods and attributes.
    """
    
    scope_order = ["+", "~", "#", "-"]
    
    def __init__(self, content):
        self.content = content
        self.scope = self.__get_scope()
        self.identifier = self.__get_identifier()
        
    def __get_scope(self):
        return self.content[0]
    
    def __get_identifier(self):
        return self.content[1:]
    
    def __str__(self):
        return self.content
        
    def __cmp__(self, other):
        result = self.__cmp_by_scope(other)
        return result or cmp(self.identifier, other.identifier)
    
    def __cmp_by_scope(self, other):
        order = _Field.scope_order
        return  order.index(self.scope) - \
                order.index(other.scope) 


class UMLOperation(_Field):
    """
    Class representing UML Operation
    """
    pass


class UMLAttribute(_Field):
    """
    Class representing UML Attribute
    """
    pass

