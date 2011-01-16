
from PyQt4.Qsci import QsciLexerPython, QsciScintilla
from PyQt4.QtGui import QColor, QFont, QFontMetrics
from PyQt4.QtCore import QObject, SIGNAL
from omelette.parser.parser import Parser

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
        QsciScintilla.__init__(self,parent)
#        self.nrOfLines = 0
#        self.line_nr = 0
#        self.pos = 0
        self.parser = Parser()

        self.set_up()
        
#        QObject.connect(self, SIGNAL("cursorPositionChanged(int, int)"), self.set_line_nr)
#        QObject.connect(self, SIGNAL("linesChanged()"), self.check_lines_count)
#        QObject.connect(self, SIGNAL("textChanged()"), self.get_updated_line)
#        QObject.connect(self, SIGNAL("copyAvailable()"), None)
#        QObject.connect(self, SIGNAL("selectionChanged()"), None)

    def get_lines(self):
        for idx in range(self.lines()):
            self.parser.update(idx+1, self.text(idx))
            #print idx+1, self.text(idx)

#    def set_line_nr(self, line_nr, pos):
#        ##Scintilla numerates lines from 0
#        self.line_nr = line_nr + 1
#        #print self.line_nr, pos+1

#    def get_updated_line(self):
#        print self.line_nr, self.text(self.line_nr-1)
#        #self.parser.update(self.line_nr, self.text(self.line_nr-1))
#
#    def check_lines_count(self):
#        if(self.lines() > self.nrOfLines):
#            self.nrOfLines = self.lines()
#            #self.parser.insert(self.line_nr+1, self.text(self.line_nr))
#            print self.line_nr+1, self.text(self.line_nr)
#        else:
#            self.nrOfLines = self.lines()



    def set_up(self):
        """Widget configuration"""
        self.setToolTip("")
        self.setWhatsThis("")

        self.setUtf8(True)

        ##font to use
        font = QFont()
        font.setFamily("Consolas")
        font.setFixedPitch(True)
        font.setPointSize(10)

        ##font metrics to build margin width
        fm = QFontMetrics(font)

        ##default font for editor
        self.setFont(font)
        self.setMarginsFont(font)

        ##line numbers
        self.setMarginWidth(0, fm.width("00000") + 5)
        self.setMarginLineNumbers(0, True)

        ##folding visual
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        ##brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        ##line color editing
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#CDA869"))

        ##margins color
        self.setMarginsBackgroundColor(QColor("#333333"))
        self.setMarginsForegroundColor(QColor("#CCCCCC"))

        ##folding margins color
        self.setFoldMarginColors(QColor("#99CC66"), QColor("#333300"))

        ##indentation
        self.setAutoIndent(True)
        self.setIndentationWidth(4)
        self.setIndentationGuides(True)
        self.setIndentationsUseTabs(False)

        ##code auto completion
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(QsciScintilla.AcsDocument)

        ##edge mode shows vertical line at 80 chars
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setEdgeColor(QColor("#FF0000"))

        ##choosing a lexer
        lexer = QsciLexerPython(self)
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        #self.setText(_sample)


        