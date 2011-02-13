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

        for object in self.instance.objects():
            object.modified = False

    def test_insert_line(self):
        line = "    - id : Integer"

        self.instance.insert_line(1, line)
        result = self.instance.objects()

        self.assertEquals(result[1].lines[1], line)
        self.assertEquals(result[2].position, 4)
        self.assertEquals(result[1].modified, True)

    def test_insert_header(self):
        line = "class Teacher"

        self.instance.insert_line(2, line)
        result = self.instance.objects()

        self.assertEquals(result[2].lines[0], line)
        self.assertEquals(result[2].lines[1], self.lines[2])
        self.assertEquals(result[3].position, 4)
        self.assertEquals(result[1].modified, True)
        self.assertEquals(result[2].modified, True)

    def test_update_line(self):
        line = "    target: School"

        self.instance.update_line(5, line)
        result = self.instance.objects()

        self.assertEquals(result[2].lines[2], line)
        self.assertEquals(result[2].modified, True)

    def test_update_header(self):
        line = "    class Teacher"

        self.instance.update_line(1, line)
        result = self.instance.objects()

        self.assertEquals(result[2].lines[0], line)
        self.assertEquals(result[1].modified, True)
        self.assertEquals(result[2].modified, True)

    def test_remove_line(self):
        self.instance.remove_line(1)
        result = self.instance.objects()

        self.assertEquals(result[1].lines[1], self.lines[2])
        self.assertEquals(result[2].position, 2)
        self.assertEquals(result[1].modified, True)

    def test_remove_header(self):
        self.instance.remove_line(3)
        result = self.instance.objects()

        self.assertEquals(len(result), 2)
        self.assertEquals(result[1].lines[3], self.lines[4])
        self.assertEquals(result[1].lines[4], self.lines[5])
        self.assertEquals(result[1].modified, True)


if __name__ == "__main__":
    unittest.main()
