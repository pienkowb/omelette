import unittest
from omelette.compiler.parser import Parser
from omelette.compiler.uml import *
from omelette.compiler.code import *

class ParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_attributes(self):
        """Tests if parser accepts various attributes."""

        code = Code("""class 2a
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
            """)

        expected = UMLObject("class", "2a", False)
        expected.add_attribute(Attribute("+", "at2a1"))
        expected.add_attribute(Attribute("-", "at2a2"))
        expected.add_attribute(Attribute("#", "at2a3"))
        expected.add_attribute(Attribute("~", "at2a4"))

        expected.add_attribute(Attribute("+", "at2a5", True))
        expected.add_attribute(Attribute("-", "at2a6", True))
        expected.add_attribute(Attribute("#", "at2a7", True))
        expected.add_attribute(Attribute("~", "at2a8", True))

        expected.add_attribute(Attribute("+", "at2a9", False, "at2a9t"))
        expected.add_attribute(Attribute("-", "at2a10", False, "at2a10t",
            "1234"))
        expected.add_attribute(Attribute("#", "at2a11", False, "at2a11t",
            "at2a11"))
        expected.add_attribute(Attribute("~", "at2a12", False, "at2a12t",
            "at2a12"))

        expected.add_attribute(Attribute("+", "at2a13", True, None, "54321"))
        expected.add_attribute(Attribute("-", "at2a14", True, None,
            "at2a14"))
        expected.add_attribute(Attribute("#", "at2a15", True, None,
            "at2a15"))

        result = self.parser.parse(code.objects()[1:])["2a"]
        
        
        self.assertEquals(expected, result)

    def test_operations(self):
        """Tests if parser accepts various operations."""

        code = Code("""class 2b
            + op2b1()
            - op2b2() : op2b2t
            # op2b3() : op2b3t
            _~ op2b4(op2b4p1)
            _+ op2b5(op2b5p1 : op2b5p1t)
            _- op2b6(op2b6p1 : op2b6p1t, op2b6p2)
            """)

        expected = UMLObject("class", "2b", False)
        expected.add_operation(Operation("+", "op2b1"))
        expected.add_operation(Operation("-", "op2b2", False, [], "op2b2t"))
        expected.add_operation(Operation("#", "op2b3", False, [], "op2b3t"))
        expected.add_operation(Operation("~", "op2b4", True, [("op2b4p1",
            None)]))
        expected.add_operation(Operation("+", "op2b5", True, [("op2b5p1",
            "op2b5p1t")]))
        expected.add_operation(Operation("-", "op2b6", True, [("op2b6p1",
            "op2b6p1t"), ("op2b6p2", None)]))

        result = self.parser.parse(code.objects()[1:])["2b"]
        self.assertEquals(expected, result)

    def test_properties(self):
        """Tests if parser accepts various properties."""

        code = Code("""class 2c
            2cp1 : 2cp1v
            2cp2 : 1234
            2cp3 : \"2cp3\"
            2cp4 : \'2cp4\'
            2cp5 : 1..3
            2cp6 : 1..*
            2cp7 : *..1
            2cp8 : *..*
            """)

        expected = UMLObject("class", "2c", False)
        expected["2cp1"] = "2cp1v"
        expected["2cp2"] = "1234"
        expected["2cp3"] = "2cp3"
        expected["2cp4"] = "2cp4"
        expected["2cp5"] = "1..3"
        expected["2cp6"] = "1..*"
        expected["2cp7"] = "*..1"
        expected["2cp8"] = "*..*"

        result = self.parser.parse(code.objects()[1:])["2c"]
        self.assertEquals(expected, result)

    def test_constraints(self):
        """Tests if parser accepts various constraints"""
            
        code = Code("""class 2d
            allow key klucz1 OBJECT
            allow key klucz2 STRING
            allow key klucz3 NUMBER
            allow key klucz4 MULTIPLICITY
            allow key klucz5 [fasada]
            allow key klucz6 [rzubr, bubr, desu]
            require key klucz7 OBJECT
            deny key zabronione
            require key klucz8 STRING
            require key klucz9 NUMBER
            require key klucz10 MULTIPLICITY
            require key klucz11 [fasada]
            require key klucz12 [rzubr, bubr, desu]
            """)
                
        expected = UMLObject("class", "2d", False)
        expected.allowed = {
            "klucz1" : "OBJECT",
            "klucz2" : "STRING",
            "klucz3" : "NUMBER",
            "klucz4" : "MULTIPLICITY",
            "klucz5" : ["fasada"],
            "klucz6" : ["rzubr", "bubr", "desu"]}
        expected.required = {
            "klucz7" : "OBJECT",
            "klucz8" : "STRING",
            "klucz9" : "NUMBER",
            "klucz10" : "MULTIPLICITY",
            "klucz11" : ["fasada"],
            "klucz12" : ["rzubr", "bubr", "desu"]}
            
        expected.denied = ["zabronione"]
        result = self.parser.parse(code.objects()[1:])["2d"]
        self.assertEquals(expected, result)

if __name__ == "__main__":
    unittest.main()
