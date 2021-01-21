from PySide2 import QtWidgets

from component.popup import Error
from dataHandler.dataExtras.file import File
from dataHandler.dataExtras.path import Path
from dataHandler.dataExtras.sq_file import SQFile
from dataHandler.workspace.sequental_editor import SequentialEditor
from dataHandler.workspace.table.table import Table


class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent, status_bar):
        super().__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_tab_widget = None

        self.create_main_tab_widget()

        self.main_layout.addWidget(self.main_tab_widget)

        self.setLayout(self.main_layout)
        self.status_bar = status_bar
        self.status_bar.showMessage("Workspace created")

    def create_main_tab_widget(self):
        self.main_tab_widget = QtWidgets.QTabWidget(self)
        self.main_tab_widget.setTabsClosable(True)
        self.main_tab_widget.setMovable(True)
        self.main_tab_widget.tabCloseRequested.connect(self.delete_tab)
        self.main_tab_widget.currentChanged.connect(self.change_tool_bar)

    def change_tool_bar(self):
        if self.main_tab_widget.currentWidget() is not None:
            self.main_tab_widget.currentWidget().create_my_tool_bar()
            return

        self.parent().tool_bar.editor_tool_bar.clearLayout()

    def delete_tab(self, index):
        # TODO : dodati pop up windo sa pitanjem da li da se sacuva
        self.main_tab_widget.removeTab(index)

    def save(self):
        # TODO: popo up error ako nema otvorernih fajlova
        if self.main_tab_widget.count() > 0:
            self.main_tab_widget.currentWidget().save()
            # TODO : dodati obaestenje u toolbar

    def find(self, parm):
        txt, _ = parm
        if self.main_tab_widget.count() > 0:
            self.main_tab_widget.currentWidget().find(txt)
            # TODO : dodati obaestenje u toolbar

    def reset_tables(self):
        if self.main_tab_widget.count() > 0:
            self.main_tab_widget.currentWidget().find('')

    def save_all(self, close=False):
        for i in range(self.main_tab_widget.count(), 0):  # prolazimo kroz sve glavne tabove fajlova
            self.main_tab_widget.widget(i).save()

            if close:
                self.main_tab_widget.removeTab(i)

    def is_file_open(self, file_path):
        for i in range(0, self.main_tab_widget.count()):  # prolazimo kroz sve glavne tabove fajlova
            if self.main_tab_widget.widget(i).check_path(file_path):
                self.main_tab_widget.setCurrentWidget(self.main_tab_widget.widget(i))
                return True

    def open_file(self, file_path, hide_current=False):
        if self.is_file_open(file_path):
            return

        path_c = Path(file_path)

        if path_c.get_extension() != "csv":
            Error("Invalid file path",
                 f"File {file_path} does not exist",
                 "1fx",
                 "")
            return

        file_c = File(path_c, False)
        index = self.main_tab_widget.count()

        if hide_current:
            index = self.main_tab_widget.indexOf(self.main_tab_widget.currentWidget())
            self.main_tab_widget.removeTab(index)

        if file_c.metadata_c.metadata["sequential_info"]["is_sequential"]:
            self.main_tab_widget.insertTab(index,
                                           SequentialEditor(self, SQFile(path_c, True), True),
                                           file_c.path_c.get_clear_file_name())
        else:
            file_c.load()
            self.main_tab_widget.insertTab(index,
                                           Table(self, file_c, True),
                                           file_c.path_c.get_clear_file_name())

        self.main_tab_widget.setCurrentWidget(self.main_tab_widget.widget(index))
