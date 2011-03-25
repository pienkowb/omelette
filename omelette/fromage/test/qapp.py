from PyQt4 import QtGui
"""This module should be included in every test using Qt."""

# Running QApplication is needed for QObjects to be created w/o segfaults.
# There should be only one QApplication per program, so creating and
# destroying it for every test isn't an option and will cause segfaults.
QT_APP = QtGui.QApplication([])
