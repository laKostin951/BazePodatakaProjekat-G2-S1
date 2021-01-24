import os

from PySide2 import QtWidgets
from PySide2.QtGui import QTextFrameFormat

from component.edit_window import EditWindow
from component.filter import Filter
from component.tool_bar import EditorToolBar
from dataHandler.dataExtras.abstract_table_model import AbstractTableModel
from dataHandler.dataExtras.path import Path
from dataHandler.dataExtras.sq_file import SQFile
from dataHandler.workspace.table.table import Table


class SequentialEditor(QtWidgets.QTabWidget, AbstractTableModel):
    def __init__(self, parent, file_c, set_model=False):
        super().__init__(parent)
        self.model_c = file_c

        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QtWidgets.QVBoxLayout()  # postavljanje main lyouta koji
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)


        self.foreign_table_toolbar = EditorToolBar(self)
        self.main_table_toolbar = EditorToolBar(self)
        self.foreign_table_tabs = QtWidgets.QTabWidget(self)  # pravljenje widgeta koji sadrzi child tabele
        self.foreign_table_tabs.currentChanged.connect(self.change_foreign_toolbar)

        self.main_table = Table(self, file_c, set_model)  # glavan tabela
        self.main_table.itemClicked.connect(self.find_relation)

        for foreign_table_path in self.model_c.metadata_c.metadata["sequential_info"]["child_relation"]:
            foreign_file_c = SQFile(Path(foreign_table_path["path_of_child_table"]), set_model)
            foreign_table = Table(self.foreign_table_tabs, foreign_file_c, set_model)
            self.foreign_table_tabs.addTab(foreign_table, foreign_file_c.get_file_name())

        self.main_layout.addWidget(self.main_table_toolbar)
        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.foreign_table_toolbar)
        self.main_layout.addWidget(self.foreign_table_tabs)

        self.setLayout(self.main_layout)

    def change_foreign_toolbar(self):
        if self.foreign_table_tabs.currentWidget() is not None:
            self.foreign_table_toolbar.reset(self.foreign_table_tabs.currentWidget().toolbar(False))
            return

        self.parent().tool_bar.editor_tool_bar.clearLayout()

    def execute(self, item):
        self.sender().find_relation(item)

    def load(self, file_c=False):
        if file_c:
            self.model_c = file_c

        self.main_table.load(self.model_c)

        for i in range(0, len(self.model_c.metadata_c.metadata["sequential_info"]["child_relation"])):
            self.foreign_table_tabs.widget(i).setModel()

    def save(self):
        self.main_table.save()

        for i in range(0, self.foreign_table_tabs.count()):
            self.foreign_table_tabs.widget(i).save()

    def find(self, txt=None):
        if txt is None:
            print("nema txt :((((")
            # TODO: open input widget
        self.main_table.find(txt)

        for i in range(0, self.foreign_table_tabs.count()):
            self.foreign_table_tabs.widget(i).find(txt)

    def filter(self, parm):
        self.main_table.filter_rows(self.main_table.filter(parm))

    def change(self, row, col, value):
        ...

    def delete(self, index):
        ...

    def add(self, arr):
        ...

    def _add(self):
        self.e = EditWindow(self.main_table)

    def split(self):
        self.main_table.split([])

    def check_path(self, file_path):
        return self.model_c.path_c.is_same(file_path)

    def find_relation(self, item):  # item je selekrovani row koji sadrzi index
        for i in range(0, len(self.model_c.metadata_c.metadata["sequential_info"][
                                  "child_relation"])):

            ft = self.foreign_table_tabs.widget(i)
            matches = ft.filter(self.main_table.model_c.get_relation_point(i, self.model_c.data[item.row()]))
            ft.filter_rows(matches)

    def reset_tables(self, _):
        self.main_table.reset()

        for i in range(0, self.foreign_table_tabs.count()):
            self.foreign_table_tabs.widget(i).reset()

    def open_file(self, path):
        self.parent().parent().parent().open_file(path, True)

    def create_my_tool_bar(self):
        self.main_table_toolbar.reset(self.main_table.toolbar(True))