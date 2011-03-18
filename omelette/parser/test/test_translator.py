import unittest
from mock import Mock
from omelette.parser.translator import Translator
from omelette.parser.lexer import Lexer
from omelette.parser.uml import UMLObject, Operation, Attribute

class Test(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()

    def test_prepare_handlers(self):
        """Tests if translator doesn't want to register handlers for tokens
        that are not in the grammar. If it does, test fails in setUp.
        """

        pass

    def test_definition_headers(self):
        """Tests if translator accepts various headers in definitions"""
        
        code = """class 1a
        class
        prototype relation
        prototype class 1b
        """
        
        expected = [
            UMLObject("class", "1a", False),
            UMLObject("class", None, False),
            UMLObject("relation", None, True),
            UMLObject("class", "1b", True)
            ]

        result = self.translator.parse([code])

        self.assertEquals(len(expected), len(result))

        for i in range(0, len(expected)):
            self.assertEquals(expected[i], result[i])
        
    def test_attributes(self):
        """Tests if translator accepts various attributes"""

        code = """class 2a
            + at2a1
            - at2a2
            # at2a3
            ~ at2a4
            _+ at2a5
            _- at2a6
            _# at2a7
            _~ at2a8
            + at2a9 : at2a9t
            - at2a10 : at2a10t = 1234
            # at2a11 : at2a11t = \"at2a11\"
            ~ at2a12 : at2a12t = \'at2a12\'
            _+ at2a13 = 54321
            _- at2a14 = \"at2a14\"
            _# at2a15 = \'at2a15\'
            """

        expected = UMLObject("class", "2a", False)
        expected.add_attribute(Attribute(False, "+", "at2a1", None, None))
        expected.add_attribute(Attribute(False, "-", "at2a2", None, None))
        expected.add_attribute(Attribute(False, "#", "at2a3", None, None))
        expected.add_attribute(Attribute(False, "~", "at2a4", None, None))

        expected.add_attribute(Attribute(True, "+", "at2a5", None, None))
        expected.add_attribute(Attribute(True, "-", "at2a6", None, None))
        expected.add_attribute(Attribute(True, "#", "at2a7", None, None))
        expected.add_attribute(Attribute(True, "~", "at2a8", None, None))

        expected.add_attribute(Attribute(False, "+", "at2a9", "at2a9t", None))
        expected.add_attribute(Attribute(False, "-", "at2a10", "at2a10t", "1234"))
        expected.add_attribute(Attribute(False, "#", "at2a11", "at2a11t", "\"at2a11\""))
        expected.add_attribute(Attribute(False, "~", "at2a12", "at2a12t", "\'at2a12\'"))

        expected.add_attribute(Attribute(True, "+", "at2a13", None, "54321"))
        expected.add_attribute(Attribute(True, "-", "at2a14", None, "\"at2a14\""))
        expected.add_attribute(Attribute(True, "#", "at2a15", None, "\'at2a15\'"))

        result = self.translator.parse([code])[0]
        self.assertEquals(expected, result)
            
    def test_operations(self):
        """Tests if translator accepts various operations"""

        code = """class 2b
            + op2b1()
            - op2b2() : op2b2t
            _# op2b3() : op2b3t
            ~ op2b4(op2b4p1)
            _+ op2b5(op2b5p1 : op2b5p1t)
            _- op2b6(op2b6p1 : op2b6p1t, op2b6p2)
            """
        
        expected = UMLObject("class", "2b", False)
        expected.add_operation(Operation(False, "+", "op2b1", [], None))
        expected.add_operation(Operation(False, "-", "op2b2", [], "op2b2t"))
        expected.add_operation(Operation(True, "#", "op2b3", [], "op2b3t"))
        expected.add_operation(Operation(False, "~", "op2b4", [("op2b4p1", None)], None))
        expected.add_operation(Operation(True, "+", "op2b5", [("op2b5p1", "op2b5p1t")], None))
        expected.add_operation(Operation(True, "-", "op2b6", [("op2b6p1", "op2b6p1t"), ("op2b6p2", None)], None))

        result = self.translator.parse([code])[0]
        self.assertEquals(expected, result)

    def test_properties(self):
        """Tests if translator accepts various properties"""

        code = """class 2c
            2cp1 : 2cp1v
            2cp2 : 1234
            2cp3 : \"2cp3\"
            2cp4 : \'2cp4\'
            2cp5 : 1..3
            2cp6 : 1..*
            2cp7 : *..1
            2cp8 : *..*
            """

        expected = UMLObject("class", "2c", False)
        expected["2cp1"] = "2cp1v"
        expected["2cp2"] = "1234"
        expected["2cp3"] = "\"2cp3\""
        expected["2cp4"] = "\'2cp4\'"
        expected["2cp5"] = "1..3"
        expected["2cp6"] = "1..*"
        expected["2cp7"] = "*..1"
        expected["2cp8"] = "*..*"

        result = self.translator.parse([code])[0]
        self.assertEquals(expected, result)        
