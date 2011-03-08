from pyparsing import *
ParserElement.setDefaultWhitespaceChars(" \t")

class Lexer(object):
    """A Class holding a representation of Barnex-Patyk grammar"""
    
    def __init__(self):
        self.tokens = {}
        self.__build_grammar()

    def __build_grammar(self):
        """DESU"""
        
        name_charset = alphanums + "-_"
        scope_charset = "+-#~"
        #TODO: a proper number representation
        self.number = Word(nums)
        self.name = Word(name_charset)
        self.string = quotedString
        self.scope = Word(scope_charset, exact=1).setResultsName("scope")
        self.static = Literal("_").setResultsName("static")
        
        self.header = self.__build_header()
        self.attribute = self.__build_attribute();
        self.operation = self.__build_operation();
        self.property = self.__build_property();
        self.definition = self.__build_definition()
        
        self.grammar = ZeroOrMore(self.definition).setResultsName("code")

    def __build_definition(self):
        element = self.operation ^ self.attribute ^ self.property ^ LineEnd()
        definition = (ZeroOrMore(LineEnd()) + self.header + LineEnd() + \
            ZeroOrMore(element+LineEnd())).setResultsName("definition")
        
        return definition

    def __build_header(self):
        object_name = self.name.setResultsName("name")
        parent_name = self.name.setResultsName("parent")
        prototype = Literal("prototype").setResultsName("prototype")
        header = (Optional(prototype) + parent_name + \
            Optional(object_name)).setResultsName("header")
            
        return header

    def __build_attribute(self):
        attribute_value = self.number ^ self.string 
        attribute_default = attribute_value.setResultsName("default")
        attribute_type = self.name.setResultsName("type")
        attribute_name = self.name.setResultsName("name")
        attribute = (Optional(self.static) + self.scope + attribute_name + \
            Optional(":"+attribute_type) +  Optional("="+attribute_default) \
            ).setResultsName("attribute")
            
        return attribute

    def __build_operation(self):
        parameter_name = self.name.setResultsName("name")
        parameter_type = self.name.setResultsName("type")
        parameter = Group(parameter_name + Optional(":"+parameter_type) \
                ).setResultsName("parameter")
        parameters = (delimitedList(parameter)).setResultsName("parameters")
        method_name = self.name.setResultsName("name")
        return_type = self.name.setResultsName("return_type")
        operation = (Optional(self.static) + self.scope + method_name + "(" + \
            Optional(parameters) + ")" +  Optional(":"+return_type) \
            ).setResultsName("operation")

        return operation
    
    def __build_property(self):
        #do we need to name left and right values of multiplicity?
        multiplicity = ((self.number ^ "*") + ".." + (self.number ^ "*") \
            ).setResultsName("multiplicity")
        property_name = self.name.setResultsName("name")
        property_value = Group(multiplicity ^ self.name ^ self.string \
            ).setResultsName("value")
        #uproszczenie gramatyki: property moze miec tylko jedna wartosc
        #property_values = OneOrMore(property_value).setResultsName("values")
        property_values = property_value.setResultsName("values")

        property = (property_name + ":" + property_values \
            ).setResultsName("property")

        return property