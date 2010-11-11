import unittest
from omelette.parser.code import Code

class CodeTest(unittest.TestCase):
    def setUp(self):
        self.instance = Code()
        self.lines = [
            "class Student",
            "  - name : String",
            "  + learn()",
            "association",
            "  source: Student",
            "  target: University"]

        for number in range(len(self.lines)):
            self.instance.insert_line(number, self.lines[number])

    def test_insert_line(self):
        line = "  - id : Integer"

        self.instance.insert_line(1, line)
        result = self.instance.objects()

        self.assertEquals(result[0].lines[1], line)
        self.assertEquals(result[1].position, 4)

    def test_update_line(self):
        line = "  target: School"

        self.instance.update_line(5, line)
        result = self.instance.objects()

        self.assertEquals(result[1].lines[2], line)

    def test_remove_line(self):
        self.instance.remove_line(1)
        result = self.instance.objects()

        self.assertEquals(result[0].lines[1], self.lines[2])
        self.assertEquals(result[1].position, 2)


if __name__ == "__main__":
    unittest.main()
