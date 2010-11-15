from PyQt4.QtGui import QToolBar, QAction, QIcon, QApplication
from PyQt4.QtCore import QObject, SIGNAL, SLOT

class ToolBar(QToolBar):
    def __init__(self, window, qsci):
        QToolBar.__init__(self)
        self.actions_dict = {'action_new':("document-new", "New", self._new_file),
                        'action_open':("document-open", "Open", self._open_file),
                        'action_save':("document-save", "Save", self._save_file),
                        'action_save_as':("document-save-as", "Save As", self._saveas_file),
                        'action_cut':("edit-cut", "Cut", SLOT("cut ()")),
                        'action_copy':("edit-copy", "Copy", SLOT("copy ()")),
                        'action_paste':("edit-paste", "Paste", SLOT("paste ()")),
                        'action_undo':("edit-undo", "Undo", SLOT("undo ()")),
                        'action_redo':("edit-redo", "Redo", SLOT("redo ()")),
                        'action_execute':("edit-Execute", "Execute", self._execute)}
        for action in self.actions_dict:
            self.action = QAction(window)
            self.action.setIcon(QIcon.fromTheme(self.actions_dict[action][0]))
            #self.action.setObjectName(action)
            self.action.setIconText(QApplication.translate("MainWindow", self.actions_dict[action][1], None, QApplication.UnicodeUTF8))
            self.addAction(self.action)
            self.addSeparator()
            if action in ('action_new', 'action_open', 'action_save', 'action_save_as', 'action_execute'):
                QObject.connect(self.action, SIGNAL("triggered()"), self.actions_dict[action][2])
            else:
                QObject.connect(self.action, SIGNAL("triggered()"), qsci, self.actions_dict[action][2])
        

    def _execute(self):
        pass

    def _new_file(self):
        pass

    def _save_file(self):
        pass

    def _saveas_file(self):
        pass

    def _open_file(self):
        pass