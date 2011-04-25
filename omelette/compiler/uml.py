class UMLObject(object):
    """Class representing UML diagram object."""

    def __init__(self, parent=None, name=None, is_prototype=False):
        """
        Create UMLObject

        Keyword arguments:
        parent -- name of UMLObject this object is based upon (default: None)
        name -- name of this UMLObject (default: None)
        is_prototype -- prototype objects aren't returned by Compiler.compile
        method (default: False)
        """
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
        """Adds an instance of Operation class to objects operations"""
        self.__operations.append(operation)

    def add_attribute(self, attribute):
        """Adds an instance of Attribute class to objects attributes"""
        self.__attributes.append(attribute)

    def operations(self):
        """Returns list of object's operations"""
        return self.__operations

    def attributes(self):
        """Returns list of object's attributes"""
        return self.__attributes

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __contains__(self, key):
        return key in self.properties

def _try_to_format(format, value):
    """
    Tries to format value according to the format parameter.
    If unscuccessful returns empty string.
    """
    return format % value if value else ""


class _Field(object):
    """Helper class used in UMLObject."""

    def __eq__(self, other) :
        return self.__dict__ == other.__dict__


class Operation(_Field):
    """Class representing UML Operation."""

    def __init__(self, visibility, name, is_static=False, parameters=[], type=None):
        """
        Create Operation with given visibility ("+", "-", "#" or "~") and name.

        Parameters are list of tuples: name, type.

        Keyword arguments:
        is_static -- (default: False)
        parameters -- list of operation parameters (default: empty list)
        type -- type of value returned by the operation as a String (default: None)
        """

        self.is_static = is_static
        self.visibility = visibility
        self.name = name
        self.parameters = parameters
        self.type = type

    def __str__(self):
        return (self.visibility + " " + self.name + "(" +
                self.__formatted_params() + ")" +
                _try_to_format(" : %s", self.type))

    def __formatted_params(self):
        """
        Returns formatted list of operation's parameters.

        eg: "arg1 : type1, arg2 : type2, arg3"
        """

        format = lambda(n, t) : n + _try_to_format(" : %s", t)
        formatted = map(format, self.parameters)
        return ", ".join(formatted)

    def __format_parameter(self, parameter):
        """
        Used in __formatted_params, returns "arg1 : type" if param's type is
        not None, otherwise just "arg1".
        """
        (name, type) = parameter
        return name + ((" : " + type) if type else "")


class Attribute(_Field):
    """Class representing UML Attribute."""

    def __init__(self, visibility, name, is_static=False, type=None, default_value=None):
        """
        Create Attribute with given visibility ("+", "-", "#" or "~") and name.

        Keyword arguments:
        is_static -- (default: False)
        type -- type of value returned by the operation as a String (default: None)
        default_value -- (default : None).
        """
        self.is_static = is_static
        self.visibility = visibility
        self.name = name
        self.type = type
        self.default_value = default_value

    def __str__(self):
        return (self.visibility + " " + self.name +
                _try_to_format(" : %s", self.type) +
                _try_to_format(" = %s", self.default_value))
