from PySide2 import QtWidgets

from dataHandler.workspace.table.table import Table


class SerialEditor(QtWidgets.QTabWidget):
    def __init__(self, parent, file_c):
        super().__init__(parent)
        table = Table(self)

        self.addTab(table, file_c.get_file_name())
        parent.main_tab_widget.addTab(self, file_c.path_c.get_clear_file_name())

        table.load(file_c)

    def saveX(self):
        print("save sam")
