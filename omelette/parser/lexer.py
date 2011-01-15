from pyparsing import *
ParserElement.setDefaultWhitespaceChars(" \t")

"""
    !!!!!!!! czy scope powinno byc obowiazkowe? Bo teraz jest
    a chyba byc nie powinno.
"""

class NonexistentTokenException(Exception):
    """An exception that occurs when one tries to register handler for a token
    that is not in the grammar.
    """

    def __init__(self, token_name):
        self.__token_name = token_name

    def __str__(self):
        return "Lexer does not export a token named " + repr(self.__token_name)

class Lexer(object):
    """A Class holding a representation of Barnex-Patyk grammar"""

    def __init__(self):
        (self.__grammar, self.__tokens) = self.__build_grammar()

    def register_handlers(self, handlers):
        """Sets action handlers for tokens.
        dictionary of handlers - maps token names to parsing action functions
        """

        for token_name in handlers.keys():
            if not( token_name in self.__tokens ):
                raise NonexistentTokenException(token_name)
            self.__tokens[token_name].setParseAction(handlers[token_name])

    def unregister_handlers(self):
        """Unsets action handlers for all tokens."""

        for token_name in self.__tokens.keys():
            self.__tokens[token_name].setParseAction()

    def parse(self, code):
        """Parses a string with its grammar. Returns ParseResults object."""

        return self.__grammar.parseString(code)

    def __build_grammar(self):
        """Builds a Barnex-Patyk grammar representation. Returns a tuple of
            - a pyparsing ParserElement object describing the grammar
            - a hash mapping token names to ParserElements describing tokens
            TODO: refactor the shit out of here?
        """

        tokens={}
        name_charset = alphanums + "-_"
        scope_charset = "+-#~"

        #TODO: a proper number representation
        number = Word(nums)
        name = Word(name_charset)
        string = quotedString
        attribute_value = number ^ string 

        scope = Word(scope_charset, exact=1).setResultsName('scope')
        #do we need to name left and right values of multiplicity?
        multiplicity = ((number ^ '*') + '..' + (number ^ '*') \
            ).setResultsName('multiplicity')
        property_name = name.setResultsName('name')
        property_value = Group(multiplicity ^ name ^ string \
            ).setResultsName('value')

        #uproszczenie gramatyki: property moze miec tylko jedna wartosc
        #property_values = OneOrMore(property_value).setResultsName('values')
        property_values = property_value.setResultsName('values')

        property = (property_name + ':' + property_values \
            ).setResultsName('property')

        #what was the position of static token again?
        static = Literal('_').setResultsName('static')
        parameter_name = name.setResultsName('name')
        parameter_type = name.setResultsName('type')
        parameter = Group(parameter_name + Optional(':'+parameter_type) \
                ).setResultsName('parameter')
        parameters = (delimitedList(parameter)).setResultsName('parameters')
        method_name = name.setResultsName('name')
        return_type = name.setResultsName('return_type')
        operation = (Optional(static) + scope + method_name + "(" + \
            Optional(parameters) + ")" +  Optional(':'+return_type) \
            ).setResultsName('operation')
        
        attribute_default = attribute_value.setResultsName('default')
        attribute_type = name.setResultsName('type')
        attribute_name = name.setResultsName('name')
        attribute = (Optional(static) + scope + attribute_name + \
            Optional(':'+attribute_type) +  Optional('='+attribute_default) \
            ).setResultsName('attribute')

        element = operation ^ attribute ^ property

        object_name = name.setResultsName('name')
        parent_name = name.setResultsName('parent')
        prototype = Literal('prototype').setResultsName('prototype')
        header = (Optional(prototype) + parent_name + \
            Optional(object_name)).setResultsName('header')

        definition = (header + LineEnd() + \
            ZeroOrMore((element+LineEnd())^LineEnd())).setResultsName('definition')

        grammar = ZeroOrMore(definition).setResultsName('code')

        #todo: do it properly with reflection api
        #do we have to export all tokens?
        tokens['definition'] = definition
        tokens['header'] = header
        tokens['attribute'] = attribute
        tokens['operation'] = operation
        tokens['property'] = property
        #omg my eyes bleed

        return (grammar, tokens)
