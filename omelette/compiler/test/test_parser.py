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

        expected = UMLObject("class", "2a", False, code.objects()[1])
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

        result = self.parser.parse(code.objects())["2a"]
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

        expected = UMLObject("class", "2b", False, code.objects()[1])
        expected.add_operation(Operation("+", "op2b1"))
        expected.add_operation(Operation("-", "op2b2", False, [], "op2b2t"))
        expected.add_operation(Operation("#", "op2b3", False, [], "op2b3t"))
        expected.add_operation(Operation("~", "op2b4", True, [("op2b4p1",
            None)]))
        expected.add_operation(Operation("+", "op2b5", True, [("op2b5p1",
            "op2b5p1t")]))
        expected.add_operation(Operation("-", "op2b6", True, [("op2b6p1",
            "op2b6p1t"), ("op2b6p2", None)]))

        result = self.parser.parse(code.objects())["2b"]
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

        expected = UMLObject("class", "2c", False, code.objects()[1])
        expected.properties = {
            "2cp1": ("2cp1v", "OBJECT"),
            "2cp2": ("1234", "MULTIPLICITY"),
            "2cp3": ("2cp3", "STRING"),
            "2cp4": ("2cp4", "STRING"),
            "2cp5": ("1..3", "MULTIPLICITY"),
            "2cp6": ("1..*", "MULTIPLICITY"),
            "2cp7": ("*..1", "MULTIPLICITY"),
            "2cp8": ("*..*", "MULTIPLICITY")}

        result = self.parser.parse(code.objects())["2c"]
        self.assertEquals(expected, result)

    def test_constraints(self):
        """Tests if parser accepts various constraints"""

        code = Code("""class 2d
            allow klucz1 OBJECT
            allow klucz2 STRING
            allow klucz3 MULTIPLICITY
            allow klucz4 [fasada]
            allow klucz5 [rzubr, bubr, desu]
            require klucz6 OBJECT
            require klucz7 STRING
            require klucz8 MULTIPLICITY
            require klucz9 [fasada]
            require klucz10 [rzubr, bubr, desu]
            """)

        expected = UMLObject("class", "2d", False, code.objects()[1])
        expected.allowed = {
            "klucz1" : "OBJECT",
            "klucz2" : "STRING",
            "klucz3" : "MULTIPLICITY",
            "klucz4" : ["fasada"],
            "klucz5" : ["rzubr", "bubr", "desu"]}
        expected.required = {
            "klucz6" : "OBJECT",
            "klucz7" : "STRING",
            "klucz8" : "MULTIPLICITY",
            "klucz9" : ["fasada"],
            "klucz10" : ["rzubr", "bubr", "desu"]}

        result = self.parser.parse(code.objects())["2d"]
        self.assertEquals(expected, result)


if __name__ == "__main__":
    unittest.main()
