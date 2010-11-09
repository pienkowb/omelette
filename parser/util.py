class UMLObject(object):
    '''
    Class representing UML diagram object.
    '''
  
    def __init__(self):
        self.__operations = []
        self.__attributes = []
        self.__properties = {}
        
    def __setitem__(self, key, value):
        self.__properties[key] = value
        
    def __getitem__(self, key):
        return self.__properties[key]

    def add_operation(self, operation):
        self.__operations.append(_Identifier_with_visibility(operation))

    def add_attribute(self, attribute):
        self.__attributes.append(_Identifier_with_visibility(attribute))
        
    def operations(self):
        ops = self.__operations
        ops.sort()
        return map(str, ops)
        
    def attributes(self):
        attrs = self.__attributes
        attrs.sort()
        return map(str, attrs)
                    
                    
class _Identifier_with_visibility(object):
    
    '''
    Helper class used in UMLObject. Provides __cmp__ for methods and attributes
    '''
    
    visibilities_order = ["+","~","#","-"]
    
    def __init__(self,string):
        self.str = string
        self.__visibility = self.__get_visibility()
        self.__identifier = self.__get_identifier()
        
    def __get_visibility(self):
        return self.str[0]
    
    def __get_identifier(self):
        return self.str[1:]
        
    def __cmp__(self,other):
        order = _Identifier_with_visibility.visibilities_order
        visibility = order.index(self.__visibility) - \
        order.index(other.__visibility)
        if visibility:
            return visibility
        else:
            if self.__identifier > other.__identifier:
                return 1
            elif self.__identifier < other.__identifier:
                return -1
            else:
                return 0
    
    def __str__(self):
        return self.str