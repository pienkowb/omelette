from PyQt4.QtGui import QToolBar, QAction, QIcon, QApplication

class ToolBar(QToolBar):
    def __init__(self, window, actions):
        QToolBar.__init__(self)
        for action in actions:
            self.action = QAction(window)
            self.action.setIcon(QIcon.fromTheme(actions[action][0]))
            self.action.setObjectName(action)
            self.action.setIconText(QApplication.translate("MainWindow", actions[action][1], None, QApplication.UnicodeUTF8))
            self.addAction(self.action)
            self.addSeparator()