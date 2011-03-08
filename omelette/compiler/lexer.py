from pyparsing import *
ParserElement.setDefaultWhitespaceChars(" \t")

class NonexistentTokenException(Exception):
    """An exception that occurs when one tries to register handler for a token
    that is not in the grammar.
    """

    def __init__(self, token_name):
        self.__token_name = token_name

    def __str__(self):
        return "Lexer does not export a token named " + self.__token_name

class Lexer(object):
    """A Class holding a representation of Barnex-Patyk grammar"""
    
    def __setitem__(self, key, value):
        self.tokens[key] = value
        
    def __getitem__(self, key):
        return self.tokens[key]
    
    def __init__(self):
        self.tokens = {}
        self.__build_grammar()
    
    def register_handlers(self, handlers):
        """Sets action handlers for tokens.
        dictionary of handlers - maps token names to parsing action functions
        """
        
        for token_name in handlers.keys():
            if not( token_name in self.tokens ):
                raise NonexistentTokenException(token_name)
            self.tokens[token_name].setParseAction(handlers[token_name])

    def unregister_handlers(self):
        """Unsets action handlers for all tokens."""
        
        for token_name in self.tokens.keys():
            self.tokens[token_name].setParseAction()

    def parse(self, code):
        """Parses a string with its grammar. Returns ParseResults object."""
        
        return self["grammar"].parseString(code)

    def __build_grammar(self):
        """DESU"""
        
        name_charset = alphanums + "-_"
        scope_charset = "+-#~"
        #TODO: a proper number representation
        number = Word(nums)
        name = Word(name_charset)
        string = quotedString
        scope = Word(scope_charset, exact=1).setResultsName("scope")	
        static = Literal("_").setResultsName("static")
        
        header = self.__build_header(name)
        attribute = self.__build_attribute(name, number, static, string, scope);
        operation = self.__build_operation(name, scope, static);
        property = self.__build_property(name, number, string);
        definition = self.__build_definition(header, operation, attribute, property)
        
        grammar = ZeroOrMore(definition).setResultsName("code")
        
        
        self.tokens = {}
        locals_ = locals()
        for key in locals_:
            if isinstance(locals_[key], ParserElement):
                self.tokens[key]=locals_[key]

    def __build_definition(self, header, operation, attribute, property):
        
        element = operation ^ attribute ^ property ^ LineEnd()
        definition = (ZeroOrMore(LineEnd()) + header + LineEnd() + \
            ZeroOrMore(element+LineEnd())).setResultsName("definition")
        
        return definition

    def __build_header(self, name):
        
        object_name = name.setResultsName("name")
        parent_name = name.setResultsName("parent")
        prototype = Literal("prototype").setResultsName("prototype")
        header = (Optional(prototype) + parent_name + \
            Optional(object_name)).setResultsName("header")
            
        return header

    def __build_attribute(self, name, number, static, string, scope):
        
        attribute_value = number ^ string 
        attribute_default = attribute_value.setResultsName("default")
        attribute_type = name.setResultsName("type")
        attribute_name = name.setResultsName("name")
        attribute = (Optional(static) + scope + attribute_name + \
            Optional(":"+attribute_type) +  Optional("="+attribute_default) \
            ).setResultsName("attribute")
            
        return attribute

    def __build_operation(self, name, scope, static):

        parameter_name = name.setResultsName("name")
        parameter_type = name.setResultsName("type")
        parameter = Group(parameter_name + Optional(":"+parameter_type) \
                ).setResultsName("parameter")
        parameters = (delimitedList(parameter)).setResultsName("parameters")
        method_name = name.setResultsName("name")
        return_type = name.setResultsName("return_type")
        operation = (Optional(static) + scope + method_name + "(" + \
            Optional(parameters) + ")" +  Optional(":"+return_type) \
            ).setResultsName("operation")

        return operation
    
    def __build_property(self, name, number, string):
        
        #do we need to name left and right values of multiplicity?
        multiplicity = ((number ^ "*") + ".." + (number ^ "*") \
            ).setResultsName("multiplicity")
        property_name = name.setResultsName("name")
        property_value = Group(multiplicity ^ name ^ string \
            ).setResultsName("value")
    #uproszczenie gramatyki: property moze miec tylko jedna wartosc
        #property_values = OneOrMore(property_value).setResultsName("values")
        property_values = property_value.setResultsName("values")

        property = (property_name + ":" + property_values \
            ).setResultsName("property")

        return property