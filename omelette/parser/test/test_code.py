import unittest
from omelette.parser.code import Code

class CodeTest(unittest.TestCase):
    def test_insert_line(self):
        instance = Code()
        lines = ["class Student", "  - name : String", "  + learn()",
            "association", "  source: Student", "  target: Student"]

        for i in range(len(lines)):
            instance.insert_line(i, lines[i])

        result = instance.objects()

        self.assertEquals(result[0].position, 0)
        self.assertEquals(result[1].position, 3)
        
        self.assertEquals(result[0].lines, lines[:3])
        self.assertEquals(result[1].lines, lines[-3:])

    def test_update_line(self):
        pass

    def test_remove_line(self):
        pass


if __name__ == "__main__":
    unittest.main()