
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

_sample = """
#Sample Omelette source code with kvp
class Person
    -age:int
    +getAge():int
    +setAge(age:int=25):void

association BaseAssociation
    name: "work for"
    label-direction: target
        source-object: Person
        source-count: 1..*
        source-role: "employee"
    target: Company * "employer" """

class QSci(QsciScintilla):
    def __init__(self, parent):
        QsciScintilla.__init__(self, parent)
        self.setUtf8(True)
        self.setMarginWidth(0,20)
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setAutoIndent(True)
        self.setIndentationWidth(4)
        self.setIndentationGuides(True)
        self.setIndentationsUseTabs(False)
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(QsciScintilla.AcsDocument)

        lexer = QsciLexerPython(self)
        self.setLexer(lexer)
        self.setText(_sample)



