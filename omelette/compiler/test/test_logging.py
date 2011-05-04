import unittest
from omelette.compiler import logging

class LoggerTest(unittest.TestCase):

    def setUp(self):
        logging.getLogger("test").flush()

    def test_is_empty(self):
        instance = logging.getLogger("test")

        self.assertTrue(instance.is_empty())

    def test_isnt_empty(self):
        instance = logging.getLogger("test")
        instance.error("ops")

        self.assertFalse(instance.is_empty())

    def test_flush(self):
        instance = logging.getLogger("test")
        instance.error("ops")
        instance.flush()

        self.assertTrue(instance.is_empty())

    def test_info(self):
        instance = logging.getLogger("test")
        instance.info("ops")
        value = str(instance.events.pop())

        self.assertRegexpMatches(value, "INFO")

    def test_warning(self):
        instance = logging.getLogger("test")
        instance.warning("ops")
        value = str(instance.events.pop())
        
        self.assertRegexpMatches(value, "WARNING")

    def test_error(self):
        instance = logging.getLogger("test")
        instance.error("ops")
        value = str(instance.events.pop())

        self.assertRegexpMatches(value, "ERROR")

    def test_critical(self):
        instance = logging.getLogger("test")
        instance.critical("ops")
        value = str(instance.events.pop())

        self.assertRegexpMatches(value, "CRITICAL")

    def test_different_modules(self):
        """
        Exploratory testing, do we get the same instance if we 
        import module twice?
        """
        m1 = __import__("logging")
        m2 = __import__("logging")

        self.assertEquals(m1.getLogger("test"), m2.getLogger("test"))

