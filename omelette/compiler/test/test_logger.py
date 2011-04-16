import unittest
from omelette.compiler import logger 

class LoggerTest(unittest.TestCase):

    def setUp(self):
        logger.instance.clear()

    def test_error(self):
        logger.instance.log_error(1,"fasada")
        self.assertTrue(logger.instance.has_errors)

    def test_clear(self):
        self.assertFalse(logger.instance.has_errors)
