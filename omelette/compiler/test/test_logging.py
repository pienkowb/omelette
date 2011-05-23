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

        self.assertNotEquals(value.find("INFO"), -1)

    def test_warning(self):
        instance = logging.getLogger("test")
        instance.warning("ops")
        value = str(instance.events.pop())

        self.assertNotEquals(value.find("WARNING"), -1)

    def test_error(self):
        instance = logging.getLogger("test")
        instance.error("ops")
        value = str(instance.events.pop())

        self.assertNotEquals(value.find("ERROR"), -1)

    def test_critical(self):
        instance = logging.getLogger("test")
        instance.critical("ops")
        value = str(instance.events.pop())

        self.assertNotEquals(value.find("CRITICAL"), -1)

    def test_different_modules(self):
        """
        Exploratory testing, do we get the same instance if we
        import module twice?
        """
        m1 = __import__("logging")
        m2 = __import__("logging")

        self.assertEquals(m1.getLogger("test"), m2.getLogger("test"))

    def test_get_events(self):
        instance = logging.getLogger("test")
        instance.warning("ops")
        instance.critical("ooops")
        result = instance.get_events("CRITICAL WARNING INFO")
        self.assertEquals(2,len(result))
        result = instance.get_events("CRITICAL")
        self.assertEquals(1,len(result))

    def test_has(self):
        instance = logging.getLogger("test")
        instance.warning("ops")
        instance.critical("ooops")
        self.assertTrue(instance.has("CRITICAL"))
        self.assertTrue(instance.has("CRITICAL WARNING"))
        self.assertFalse(instance.has("ERROR"))


if __name__ == "__main__":
    unittest.main()
