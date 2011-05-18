from pyparsing import *
from omelette.compiler.lexer import Lexer
from omelette.compiler.uml import *

def callback(handler):
    def wrapper(self, s, l, t):
        handler(self, t)
    return wrapper


class Parser(object):
    """A class translating code to UMLObjects."""

    def __init__(self, lexer=Lexer()):
        """Constructor that pins to a provided Lexer."""

        self.__lexer = lexer
        self.__register_handlers()

    def parse(self, code_objects):
        self.__uml_object = None
        self.__objects = {}

        for code_object in code_objects:
            if code_object.position < 0: continue

            self.__code_object = code_object
            self.__lexer["definition"].parseString(str(code_object))

        return self.__objects

    def __register_handlers(self):
        """Sets parseActions for appropriate tokens in lexer."""

        self.__lexer["definition"].setParseAction(self.__handle_definition)
        self.__lexer["header"].setParseAction(self.__handle_header)
        self.__lexer["operation"].setParseAction(self.__handle_operation)
        self.__lexer["attribute"].setParseAction(self.__handle_attribute)
        self.__lexer["property"].setParseAction(self.__handle_property)
        self.__lexer["constraint"].setParseAction(self.__handle_constraint)

    @callback
    def __handle_constraint(self, token):
        type = token["type"]
        key = token["key"]
        
        if type == "deny":
            self.__uml_object.denied.append(key)
            return
            
        constants = token.get("constants")
        value = []
        if constants!=None:
            for constant in constants:
                value.append(constant)
        else:
            value = token.get("value")
            
        if type == "allow":
            self.__uml_object.allowed[key] = value
        if type == "require":
            self.__uml_object.required[key] = value

    @callback
    def __handle_definition(self, token):
        name = self.__uml_object.name

        self.__objects[name] = self.__uml_object
        self.__uml_object = None

    @callback
    def __handle_header(self, token):
        name = token["header"].get("name")
        parent = token["header"]["parent"]
        prototype = "prototype" in token["header"]

        if name == None:
            name = "@%s" % id(self.__code_object)

        if parent == "base":
            parent = None

        self.__uml_object = UMLObject(parent, name, prototype)

    @callback
    def __handle_attribute(self, token):
        static = "static" in token["attribute"]
        visibility = token["attribute"].get("visibility")
        name = token["attribute"]["name"]
        type = token["attribute"].get("type")
        default = token["attribute"].get("default")
        attribute = Attribute(visibility, name, static, type, default)

        self.__uml_object.add_attribute(attribute)

    @callback
    def __handle_operation(self, token):
        static = "static" in token["operation"]
        visibility = token["operation"].get("visibility")
        name = token["operation"]["name"]
        parameters = []

        if "parameters" in token["operation"]:
            for parameter in token["operation"]["parameters"]:
                parameter_name = parameter["name"]
                type = parameter.get("type")

                parameters.append((parameter_name, type))

        return_type = token["operation"].get("return_type")
        operation = Operation(visibility, name, static, parameters, return_type)

        self.__uml_object.add_operation(operation)

    @callback
    def __handle_property(self, token):
        name = token["property"]["name"]
        values = "".join(token["property"]["values"])

        self.__uml_object[name] = values
