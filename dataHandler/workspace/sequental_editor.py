import os

from PySide2 import QtWidgets

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
        self.main_table_toolbar = self.parent().parent().tool_bar.editor_tool_bar

        self.main_layout = QtWidgets.QVBoxLayout()  # postavljanje main lyouta koji
        self.foreign_table_toolbar = EditorToolBar(self)
        self.foreign_table_tabs = QtWidgets.QTabWidget(self)  # pravljenje widgeta koji sadrzi child tabele
        self.foreign_table_tabs.currentChanged.connect(self.change_foregin_toolbar)
        # self.foreign_table_tabs.currentChanged.connect(self.change_tool_bar)

        self.main_table = Table(self, file_c, set_model)  # glavan tabela
        self.main_table.itemClicked.connect(self.find_relation)
        # self.input_w = Filter(self.main_table, self.filter)

        for foreign_table_path in self.model_c.metadata_c.metadata["sequential_info"]["child_relation"]:
            foreign_file_c = SQFile(Path(foreign_table_path["path_of_child_table"]), set_model)
            foreign_table = Table(self.foreign_table_tabs, foreign_file_c, set_model)
            self.foreign_table_tabs.addTab(foreign_table, foreign_file_c.get_file_name())

        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.foreign_table_toolbar)
        self.main_layout.addWidget(self.foreign_table_tabs)

        self.setLayout(self.main_layout)

    def change_foregin_toolbar(self):
        if self.foreign_table_tabs.currentWidget() is not None:
            self.foreign_table_toolbar.reset(self.foreign_table_tabs.currentWidget().toolbar())
            return

        self.parent().tool_bar.editor_tool_bar.clearLayout()

    def execute(self, item):
        self.sender().find_relation(item, self.find_relation_from_child, self.model_c.path_c)

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

    def open_child(self, path=None):
        self.parent().parent().parent().open_file(path)

    def open_parent(self, path):
        self.parent().parent().parent().open_file(path)

    def open_file(self, path):
        self.parent().parent().parent().open_file(path, True)

    def create_my_tool_bar(self):
        self.main_table_toolbar.reset(self.main_table.toolbar())
        # return self.main_table.toolbar()
        '''self.main_table_toolbar.reset({
            "title": self.model_c.path_c,
            "visible": True,
            "tools": {
                "options": [
                    {
                        "name": "",
                        "tool_tip": {
                            "have": True,
                            "txt": f'Save - "{self.model_c.path_c.get_file_name()}"'
                        },
                        "icon": f"assets{os.path.sep}img{os.path.sep}save.jpg",
                        "callback": self.save,
                        "signal": "",
                        "status_tip": f'Save changes on file {self.model_c.path_c.get_file_name()} .'
                    },
                    {
                        "name": "",
                        "tool_tip": {
                            "have": True,
                            "txt": f'Filter - "{self.model_c.path_c.get_file_name()}"'
                        },
                        "icon": f"assets{os.path.sep}img{os.path.sep}iconmonstr-filter-1-16.png",
                        "callback": self.input_w.show,
                        "signal": "",
                        "status_tip": f''
                    },
                    {
                        "name": "",
                        "tool_tip": {
                            "have": True,
                            "txt": f'Add new "{self.model_c.path_c.get_clear_file_name()}" to - "{self.model_c.path_c.get_file_name()}"'
                        },
                        "icon": f"assets{os.path.sep}img{os.path.sep}iconmonstr-database-10-16.png",
                        "callback": self._add,
                        "signal": "",
                        "status_tip": f''
                    },
                    {
                        "name": "",
                        "tool_tip": {
                            "have": False,
                            "txt": ""
                        },
                        "icon": f'assets{os.path.sep}img{os.path.sep}iconmonstr-link-1-16.png',
                        "callback": self.reset_tables,
                        "status_tip": f''
                    },
                    {
                        "name": "",
                        "tool_tip": {
                            "have": True,
                            "txt": "Save filtered data as new file"
                        },
                        "icon": f'assets{os.path.sep}img{os.path.sep}iconmonstr-save-5-16.png',
                        "callback": self.split,
                        "status_tip": f''
                    }
                ],
                "child": {
                    "child_relations": self.model_c.metadata_c.metadata["sequential_info"]["child_relation"],
                    "callback": self.open_child
                },
                "parent": {
                    "parent_relations": self.model_c.metadata_c.metadata["sequential_info"]["parent_relation"],
                    "callback": self.open_parent
                },
            }
        })'''
