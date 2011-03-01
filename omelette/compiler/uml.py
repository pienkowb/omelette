class UMLObject(object):
    """Class representing UML diagram object."""
  
    def __init__(self, parent=None, name=None, is_prototype=False):
        self.__operations = []
        self.__attributes = []
        self.properties = {}
        
        self.type = None
        self.parent = parent
        self.name = name
        self.is_prototype = is_prototype
        
    def __setitem__(self, key, value):
        self.properties[key] = value
        
    def __getitem__(self, key):
        return self.properties[key]

    def add_operation(self, operation):
        self.__operations.append(operation)

    def add_attribute(self, attribute):
        self.__attributes.append(attribute)
        
    def operations(self):
        return self.__operations
        
    def attributes(self):
        return self.__attributes
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

          
def _format_if_not_none(format, value):
    if value is None:
        return ""
    else:
        return format % value          

                    
class _Field(object):    
    """
    Helper class used in UMLObject..
    """
    
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__


class Operation(_Field):
    """Class representing UML Operation."""
    
    def __init__(self, visibility, name, is_static=False, parameters=[], type=None):
        self.is_static = is_static
        self.visibility = visibility
        self.name = name
        self.parameters = parameters
        self.type = type

    def __str__(self):
        return self.visibility + self.name + "(" + \
                self.__formatted_params() + ")" + \
                _format_if_not_none(" : %s", self.type)   
        
    def __formatted_params(self):
        format = lambda(n, t) : n + _format_if_not_none(" : %s", t)
        formatted = map(format, self.parameters)
        return ", ".join(formatted)
                
    def __format_parameter(self, parameter):
        (name, type) = parameter
        return name + (type and (" : " + type) or "")


class Attribute(_Field):
    """Class representing UML Attribute."""
    
    def __init__(self, visibility, name, is_static=False, type=None, default_value=None):
        self.is_static = is_static
        self.visibility = visibility
        self.name = name
        self.type = type
        self.default_value = default_value
        
    def __str__(self):
        return self.visibility + self.name + \
                _format_if_not_none(" : %s", self.type) + \
                _format_if_not_none(" = %s", self.default_value)
