import unittest
from omelette.compiler.lexer import Lexer, NonexistentTokenException

class Test(unittest.TestCase):

    def setUp(self):
        self.code = """father son
    + at1 : type1
    - op1()
    pr1 : 12
prototype son grandson
    pr2: "text"
    # at2 : type2 = 'text'
    ~ op2(param1, param2)
prototype grandson
    _+ op3(param3:type3)
    pr3 : 13..*
    _- at3 : type4
    """
        self.lexer = Lexer()

        self.definition_hits = 0;
        self.operation_hits = 0;
        self.attribute_hits = 0;
        self.property_hits = 0;
        self.header_hits = 0;

        self.handlers = {}
        self.handlers["definition"] = self.__hit_definition
        self.handlers["operation"] = self.__hit_operation
        self.handlers["attribute"] = self.__hit_attribute
        self.handlers["property"] = self.__hit_property
        self.handlers["header"] = self.__hit_header

    def __hit_definition(self, s, l, t):
        self.definition_hits = self.definition_hits + 1

    def __hit_operation(self, s, l, t):
        self.operation_hits = self.operation_hits + 1

    def __hit_attribute(self, s, l, t):
        self.attribute_hits = self.attribute_hits + 1

    def __hit_property(self, s, l, t):
        self.property_hits = self.property_hits + 1

    def __hit_header(self, s, l, t):
        self.header_hits = self.header_hits + 1

    def test_register_handlers_1(self):
        """Tests if lexer accepts handlers for a set of typical tokens"""

        self.lexer.register_handlers(self.handlers)

    def test_register_handlers_2(self):
        """Tests if lexer calls handlers at all"""

        self.lexer.register_handlers(self.handlers)
        self.lexer["grammar"].parseString(self.code)

        self.assertNotEquals(self.definition_hits, 0)
        self.assertNotEquals(self.attribute_hits, 0)
        self.assertNotEquals(self.operation_hits, 0)
        self.assertNotEquals(self.property_hits, 0)
        self.assertNotEquals(self.header_hits, 0)

    def test_register_handlers_3(self):
        """Tests if lexer calls handlers proper times"""

        self.lexer.register_handlers(self.handlers)
        self.lexer["grammar"].parseString(self.code)

        self.assertEquals(self.definition_hits, 3)
        self.assertEquals(self.attribute_hits, 3)
        self.assertEquals(self.operation_hits, 3)
        self.assertEquals(self.property_hits, 3)
        self.assertEquals(self.header_hits, 3)

    def test_register_handlers_4(self):
        """Tests if lexer does not accept a handler for non-existent token"""

        self.handlers["the game"] = None
        self.assertRaises(NonexistentTokenException, self.lexer.register_handlers, \
            self.handlers)

    def test_unregister_handlers(self):
        """Tests if handlers are properly unregistered"""

        self.lexer.register_handlers(self.handlers)
        self.lexer.unregister_handlers()
        self.lexer["grammar"].parseString(self.code)

        self.assertEquals(self.definition_hits, 0)
        self.assertEquals(self.attribute_hits, 0)
        self.assertEquals(self.operation_hits, 0)
        self.assertEquals(self.property_hits, 0)
        self.assertEquals(self.header_hits, 0)

if __name__ == "__main__":
    unittest.main()
