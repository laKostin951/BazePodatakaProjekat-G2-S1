from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QVBoxLayout, QWidget

from config.settings import cnxpool
from config.settings import DEFAULT_DATA_FOLDER
from ui.widget.file_system.file_system_model import FileSystemModel, ServerDatabaseSystem


class StructureDock(QtWidgets.QDockWidget):
    clicked = QtCore.Signal(str)  # class attribute
    sql_clicked = QtCore.Signal(str, bool,  bool, str)  # class attribute

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.main_widget = QWidget(self)
        self.main_v_layout = QVBoxLayout()

        self.file_system = FileSystemModel(self.file_clicked, DEFAULT_DATA_FOLDER)
        self.server_database_system = ServerDatabaseSystem(self.sql_table_file_clicked, cnxpool.get_connection())

        self.main_v_layout.addWidget(self.file_system)
        self.main_v_layout.addWidget(self.server_database_system)

        self.main_widget.setLayout(self.main_v_layout)

        self.setWidget(self.main_widget)

    def file_clicked(self, path):
        self.clicked.emit(path)

    def sql_table_file_clicked(self, path):
        self.sql_clicked.emit(None, False, True, path)
