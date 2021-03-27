from PySide2 import QtWidgets

from config.settings import icon
from ui.widget.edit.add_window import AddNew
from dataHandler.dataExtras.abstract_table_model import AbstractTableModel
from dataHandler.dataExtras.path import MySqlPath
from dataHandler.mySql.mysql_file import MYSQLFile
from dataHandler.workspace.table.table import Table


class SQLSequentialTableEditor(QtWidgets.QTabWidget, AbstractTableModel):
    def __init__(self, parent, file_c, set_model=False):
        super().__init__(parent)
        self.model_c = file_c

        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QtWidgets.QVBoxLayout()  # postavljanje main lyouta koji
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.foreign_table_tabs = QtWidgets.QTabWidget(self)  # pravljenje widgeta koji sadrzi child tabele

        self.main_table = Table(self, file_c, set_model)
        self.main_table .tool_bar.set_parm((self.main_table .toolbar({
            "save": False,
            "save_as": False,
            "split": False,
            "merge": False,
            "filter": True,
            "search": True,
            "add": True,
            "reset": True,
            "page_up": True,
            "page_down": True,
            "parent_relation": True,
            "child_relation": True
        })))

        self.main_table.tool_bar.insert_widget({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": f'Save table as csv"'
                },
                "icon": icon.EXPORT_CSV_I(),
                "callback": self.model_c.export_as_csv,
                "signal": "",
                "status_tip": f''
        })

        self.main_table.table.itemClicked.connect(self.find_relation)

        for forgin_table_name in self.model_c.metadata_c.metadata["sequential_info"]["child_relation"]:
            foreign_file_c = MYSQLFile(MySqlPath(forgin_table_name["path_of_child_table"]), None, None)
            foreign_table = Table(self.foreign_table_tabs, foreign_file_c, set_model)
            foreign_table.tool_bar.set_parm((foreign_table.toolbar({
                "save": False,
                "save_as": False,
                "split": False,
                "merge": False,
                "filter": True,
                "search": True,
                "add": True,
                "reset": True,
                "page_up": True,
                "page_down": True,
                "parent_relation": False,
                "child_relation": False
            })))
            self.foreign_table_tabs.addTab(foreign_table, foreign_file_c.get_file_name())

        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.foreign_table_tabs)

        self.setLayout(self.main_layout)

    def execute(self, item):
        self.sender().find_relation(item)

    def load(self, file_c=False):
        if file_c:
            self.model_c = file_c

        self.main_table.load(self.model_c)

        for i in range(0, len(self.model_c.metadata_c.metadata["sequential_info"]["child_relation"])):
            self.foreign_table_tabs.widget(i).setModel()

    def save(self):
        pass

    def find(self, txt=None):
        if txt is None:
            pass
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
        self.e = AddNew(self.main_table)

    def split(self):
        pass

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
        self.parent().parent().parent().open_file(None, False, True, path)