import unittest
from omelette.parser.code import Code

class CodeTest(unittest.TestCase):
    def setUp(self):
        self.instance = Code()
        self.lines = [
            "class Student",
            "    - name : String",
            "    + learn()",
            "association",
            "    source: Student",
            "    target: University"]

        for number, line in enumerate(self.lines):
            self.instance.insert_line(number, line)

    def test_insert_line(self):
        line = "    - id : Integer"

        self.instance.insert_line(1, line)
        result = self.instance.objects()

        self.assertEquals(result[1].lines[1], line)
        self.assertEquals(result[2].position, 4)

    def test_insert_header(self):
        line = "class Teacher"

        self.instance.insert_line(2, line)
        result = self.instance.objects()

        self.assertEquals(result[2].lines[0], line)
        self.assertEquals(result[2].lines[1], self.lines[2])
        self.assertEquals(result[3].position, 4)

    def test_remove_line(self):
        self.instance.remove_line(1)
        result = self.instance.objects()

        self.assertEquals(result[1].lines[1], self.lines[2])
        self.assertEquals(result[2].position, 2)

    def test_remove_header(self):
        self.instance.remove_line(3)
        result = self.instance.objects()

        self.assertEquals(len(result), 2)
        self.assertEquals(result[1].lines[3], self.lines[4])
        self.assertEquals(result[1].lines[4], self.lines[5])

    def test_str(self):
        code_objects = self.instance.objects()
        result = str(code_objects[1])

        expected = "\n".join(self.lines[:3])

        self.assertEquals(expected, result)


if __name__ == "__main__":
    unittest.main()
