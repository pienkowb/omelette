class UMLObject(object):
    """Class representing UML diagram object."""
  
    def __init__(self, parent=None, name=None, prototype=False):
        self.__operations = []
        self.__attributes = []
        self.__properties = {}
        
        self.type = None
        self.parent = parent
        self.name = name
        self.is_prototype = prototype
        
    def __setitem__(self, key, value):
        self.__properties[key] = value
        
    def __getitem__(self, key):
        return self.__properties[key]
      
    def add_operation(self, operation):
        self.__operations.append(operation)

    def add_attribute(self, attribute):
        self.__attributes.append(attribute)
        
    def operations(self):
        operations = self.__operations
        return map(str, operations)
        
    def attributes(self):
        attributes = self.__attributes
        return map(str, attributes)
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
          
def _format_if_not_none(format, value):
    if value is None:
        return ""
    else:
        return format % value          
                    
class _Field(object):    
    """
    Helper class used in UMLObject. Provides __cmp__ for methods and attributes.
    """
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__



class Operation(_Field):
    """Class representing UML Operation."""
    
    def __init__(self, static, scope, name, parameters, type):
        self.is_static = static
        self.scope = scope
        self.name = name
        self.parameters = parameters
        self.type = type

    def __str__(self):
        return self.scope + self.name + "(" + \
                self.__formatted_param_list() + ")" + \
                _format_if_not_none(" : %s", self.type)   
        
    def __formatted_param_list(self):
        format = lambda(n, t) : n + _format_if_not_none(" : %s", t)
        formatted = map(format, self.parameters)
        return ", ".join(formatted)
                
    def __format_parameter(self, parameter):
        (name, type) = parameter
        return name + (type and (" : " + type) or "")


class Attribute(_Field):
    """Class representing UML Attribute."""
    pass

