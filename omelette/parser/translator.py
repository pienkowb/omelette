from lexer import Lexer
from pyparsing import *
from uml import *

class Translator(object):
    """A class translating code to UMLObjects"""

    def __init__( self, lexer = Lexer() ):
        """Constructor that pins to a provided Lexer"""

        if not( isinstance(lexer, Lexer) ):
            raise TypeError("must pass a Lexer instance as argument")
        self.__lexer = lexer

        self.__handlers = self.__prepare_handlers()
        self.__lexer.register_handlers(self.__handlers)

    def parse( self, code_objects ):
        """Glues code_objects code and passes it to the lexer.
        Returns a list of uml_objects.
        """

        self.__current = None # __uml_object
        self.__objects = []

        text = "\n".join([str(code_object) for code_object in code_objects])

        self.__lexer.parse(text)

        return self.__objects

    def __prepare_handlers(self):
        """Builds a hash mapping handler methods to respective token names"""

        handlers = {}
        handlers['definition'] = self.__handle_definition
        handlers['header'] = self.__handle_header
        handlers['attribute'] = self.__handle_attribute
        handlers['operation'] = self.__handle_operation
        handlers['property'] = self.__handle_property
        return handlers

    def __handle_definition(self, s, l, t):
        self.__objects.append(self.__current)
        self.__current = None

    def __handle_header(self, s, l, t):
        name = None
        if 'name' in t['header']:
            name = t['header']['name']

        parent = t['header']['parent']
        if parent == 'base':
            parent = None

        prototype = False
        if 'prototype' in t['header']:
            prototype = True

        self.__current = UMLObject(parent, name, prototype)
        #self.__current = UMLObject()
        #self.__current.prototype = prototype
        #self.__current.name = name
        #self.__current.parent = parent

    def __handle_attribute( self, s, l, t ):

        static = False
        if 'static' in t['attribute']:
            static = True

        scope = None
        if 'scope' in t['attribute']:
            scope = t['attribute']['scope']

        name = t['attribute']['name']

        type = None
        if 'type' in t['attribute']:
            type = t['attribute']['type']

        default = None
        if 'default' in t['attribute']:
            default = t['attribute']['default']

        attribute = Attribute(static, scope, name, type, default)
        self.__current.add_attribute(attribute)

    def __handle_operation( self, s, l, t ):

        static = False
        if 'static' in t['operation']:
            static = True

        scope = None
        if 'scope' in t['operation']:
            scope = t['operation']['scope']

        name = t['operation']['name']

        parameters = []
        if 'parameters' in t['operation']:
            parameters_ = t['operation']['parameters']
            for p in parameters_:
                parameter_name = p['name']
                parameter_type = None
                if 'type' in p:
                    parameter_type = p['type']
                parameters.append((parameter_name, parameter_type))
        #if not parameters:
        #    parameters = None

        return_type = None
        if 'return_type' in t['operation']:
            return_type = t['operation']['return_type']

        operation = Operation(static, scope, name, parameters, return_type)
        self.__current.add_operation(operation)


    def __handle_property( self, s, l, t ):
        name = t['property']['name']
        
        ## uproszczenie gramatyki: property moze miec tylko jedna wartosc
        #values = []
        #values_ = t['property']['values']
        #for v in values_:
        #    value = ''.join(v)
        #    values.append(value)
        values = ''.join(t['property']['values'])

        self.__current[name] = values
