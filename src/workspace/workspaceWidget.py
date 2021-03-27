from PySide2 import QtWidgets

from ui.popUp.popup import Error
from dataHandler.dataExtras.file import File
from dataHandler.dataExtras.path import Path, MySqlPath
from dataHandler.dataExtras.sq_file import SQFile
from dataHandler.mySql.mysql_file import MYSQLFile
from dataHandler.workspace.SQLSequentalTableEditor import SQLSequentialTableEditor
from dataHandler.workspace.sequental_editor import SequentialEditor
from dataHandler.workspace.table.table import Table


class WorkspaceWidget(QtWidgets.QWidget):
    def __init__(self, parent, status_bar, structure_dock):
        super().__init__(parent)
        self.structure_dock = structure_dock
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_tab_widget = None

        self.create_main_tab_widget()

        self.setStyleSheet(" border:none;"
                           "            border-left:1px solid white;")

        self.main_layout.addWidget(self.main_tab_widget)

        self.setLayout(self.main_layout)
        self.status_bar = status_bar
        self.status_bar.showMessage("Workspace created")

    def create_main_tab_widget(self):
        self.main_tab_widget = QtWidgets.QTabWidget(self)

        self.main_tab_widget.setTabsClosable(True)
        self.main_tab_widget.setMovable(True)
        self.main_tab_widget.setContentsMargins(0, 0, 0, 0)
        self.main_tab_widget.setStyleSheet("border:none;")

        self.main_tab_widget.tabCloseRequested.connect(self.delete_tab)

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

    def open_file(self, file_path, hide_current=False, mysql=False, mysqlTableName=None):
        if mysql:
            if self.is_file_open(mysqlTableName):
                return

            mysql_file = MYSQLFile(MySqlPath(mysqlTableName))
            self.main_tab_widget.insertTab(-1,
                                           SQLSequentialTableEditor(self, mysql_file, True),
                                           mysql_file.get_file_name())

            self.main_tab_widget.setCurrentWidget(self.main_tab_widget.widget(self.main_tab_widget.count()-1))
            return

        if self.is_file_open(file_path):
            return

        path_c = Path(file_path)

        if path_c.get_extension() != "csv":
            Error("Invalid file path",
                  f"File {file_path} does not exist",
                  "1fx",
                  "")
            return

        file_c = File(path_c, False, None, self.structure_dock)
        index = self.main_tab_widget.count()

        if hide_current:
            index = self.main_tab_widget.indexOf(self.main_tab_widget.currentWidget())
            self.main_tab_widget.removeTab(index)

        if file_c.metadata_c.metadata["sequential_info"]["is_sequential"]:
            self.main_tab_widget.insertTab(index,
                                           SequentialEditor(self, SQFile(path_c, True, None, self.structure_dock),
                                                            True),
                                           file_c.path_c.get_clear_file_name())
        else:
            file_c.load()
            table = Table(self, file_c, True)
            table.tool_bar.set_parm((table.toolbar({
                "save": True,
                "save_as": True,
                "split": True,
                "merge": True,
                "filter": True,
                "search": True,
                "add": True,
                "reset": True,
                "page_up": True,
                "page_down": True,
                "parent_relation": False,
                "child_relation": False
            })))
            self.main_tab_widget.insertTab(index,
                                           table,
                                           file_c.path_c.get_clear_file_name())

        self.main_tab_widget.setCurrentWidget(self.main_tab_widget.widget(index))
