import os

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction

from component.edit_window import EditWindow
from component.filter import Filter
from dataHandler.dataExtras.abstract_table_model import AbstractTableModel

PROGRAMMATICALL = False


class Table(QtWidgets.QTableWidget, AbstractTableModel):
    def __init__(self, parent, model_c=None, set_model=False):
        super().__init__(parent)

        self.model_c = model_c
        self.input_w = Filter(self, self._filter)
        self.tool_bar = None
        self.change_flag = False

        if set_model:
            self.load()

    def load(self, model_c=None):
        if model_c is not None:
            self.model_c = model_c

        row_count = self.model_c.get_row_count()

        self.setColumnCount(self.model_c.get_column_count())
        self.setRowCount(row_count)

        self.set_horizontal_header_labels()
        self.setSelectionBehavior(self.SelectRows)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        for i in range(row_count):
            self.model_c.set_table_row(self, i)

        self.change_flag = False

        self.itemChanged.connect(self.change)
        self.customContextMenuRequested.connect(self.option_menu)
        self.horizontalHeader().sectionClicked.connect(self.sort_by_header)

    def save(self):
        self.model_c.save()

    def find(self, txt):
        self.filter_rows(self.model_c.find(txt))

    def change(self, item):
        if self.change_flag:
            self.change_flag = False
            return
        changed_item = item
        success, value = self.model_c.change(changed_item.row(), changed_item.column(), changed_item.text())
        if success:
            return
        self.change_flag = True
        item.setText(value)

    def delete(self, item=None):
        for index in sorted(self.selectionModel().selectedRows(), reverse=True):
            if self.model_c.delete(index.row()):
                self.removeRow(index.row())

    def open_add_window(self):
        self.e = EditWindow(self)

    def add(self, data):
        success, ad_data = self.model_c.add(data)
        if success:
            self.insertRow(self.rowCount())
            self.model_c.set_table_row(self, self.rowCount() - 1)
            return True, ad_data
        return False, ad_data

    def split(self, arr):
        if len(arr) == 0:
            arr = self.model_c.temp_data
        self.model_c.split(arr)

    def filter(self, parm):
        return self.model_c.filter(parm)

    def _filter(self, parm):
        self.filter_rows(self.filter(parm))

    def reset(self):
        for row in range(self.rowCount()):
            self.showRow(row)

    def toolbar(self):
        return {
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
                        "callback": self.open_add_window,
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
                        "callback": self.reset,
                        "status_tip": f''
                    }
                ],
                "child": {
                    "child_relations": self.model_c.metadata_c.metadata["sequential_info"]["child_relation"],
                    "callback": self.open_file
                },
                "parent": {
                    "parent_relations": self.model_c.metadata_c.metadata["sequential_info"]["parent_relation"],
                    "callback": self.open_file
                },
            }
        }

    def option_menu(self, pos):
        selected_rows_ln = len(self.get_selected_rows_indexes())

        if selected_rows_ln == 1:
            self.single_row_selected_options(pos)
        if selected_rows_ln > 1:
            self.multiple_row_selected(pos)
        if selected_rows_ln == 0:
            self.null_row_selected(pos)

    def null_row_selected(self, pos):
        ...

    def multiple_row_selected(self, pos):
        ...

    def single_row_selected_options(self, pos):
        menu = QtWidgets.QMenu(self)

        delete_selected_rows = QAction('Delete', self)

        menu.addAction(delete_selected_rows)

        action = menu.exec_(self.viewport().mapToGlobal(pos))

        if action == delete_selected_rows:
            self.delete()

    def get_value(self, row, col):
        if not isinstance(col, int):
            col, _ = self.get_header_meta(col)

        if col is None or col >= self.columnCount():
            print("Coll does not exist")
            # super(Table, self).info("Column does not exist")

        return self.item(row, col).text()

    def get_header_meta(self, header_name):
        return self.model_c.metadata_c.get_header_meta(header_name)

    def set_horizontal_header_labels(self):
        for i in range(0, self.model_c.get_column_count()):
            self.setHorizontalHeaderItem(i, self.model_c.get_header_label(i))

    def sort_by_header(self, header):
        ...

    def get_selected_rows_indexes(self):
        return self.selectionModel().selectedRows()

    def check_path(self, file_path):
        return self.model_c.path_c.is_same(file_path)

    def filter_rows(self, arr):
        self.model_c.temp_data = arr
        for row in range(self.rowCount()):
            self.showRow(row) if row in arr else self.hideRow(row)

    def get_min_max(self, header_name):
        return self.model_c.get_min(header_name), self.model_c.get_max(header_name)

    def open_child(self, path=None):
        self.parent().open_file(path)

    def open_parent(self, path):
        self.parent().open_file(path)

    def open_file(self, path):
        self.parent().open_file(path)