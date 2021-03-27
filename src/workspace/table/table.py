from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction, QVBoxLayout, QInputDialog

import ui.widget.edit.add_window as EditWindow
from config.settings import icon
from ui.widget.filter import Filter
from ui.widget.split import Split
from ui.widget.toolbar import EditorToolBar
from global_F.global_func import SelectFiles

PROGRAMMATICALL = False


class Table(QtWidgets.QWidget):
    def __init__(self, parent, model_c=None, set_model=False):
        super().__init__(parent)

        self.change_flag = False
        self.table = QtWidgets.QTableWidget(parent)
        self.table.change_flag = False
        self.model_c = model_c

        self.input_w = Filter(self, self._filter)
        self.tool_bar = EditorToolBar(self, None)
        self.merge = None
        self.split = None

        self.v_layout = QVBoxLayout()

        self.v_layout.addWidget(self.tool_bar)
        self.v_layout.addWidget(self.table)
        self.v_layout.setSpacing(0)

        self.table.setContentsMargins(0, 0, 0, 0)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("background-color: rgb(0,26,51);"
                                 "border:none;"
                                 "gridline-color: rgb(0,85,102);"
                                 "padding-top: 0px;"
                                 "padding-right: 2px;"
                                 "padding-bottom: 2px;"
                                 "padding-left: 0px;"
                                 "margin: 0x;")
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().sizeHint().setHeight(25)

        self.setLayout(self.v_layout)

        if set_model:
            self.load()

    def load(self, model_c=None):
        if model_c is not None:
            self.model_c = model_c

        row_count = self.model_c.get_row_count()

        self.table.setColumnCount(self.model_c.get_column_count())
        self.table.setRowCount(row_count)

        self.set_horizontal_header_labels()
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)

        for i in range(row_count):
            self.model_c.set_table_row(self.table, i)

        self.table.change_flag = False

        self.table.itemChanged.connect(self.change)
        self.table.customContextMenuRequested.connect(self.option_menu)
        self.table.horizontalHeader().sectionClicked.connect(self.sort_by_header)

    def save(self):
        self.model_c.save()

    def find(self, txt=None):
        if txt is None or txt is False:
            txt, _ = QInputDialog.getText(self, 'Input Dialog', "Quick Search:")
        self.filter_rows(self.model_c.find(txt))

    def change(self, item):
        if self.table.change_flag:
            self.table.change_flag = False
            return
        changed_item = item
        success, value = self.model_c.change(changed_item.row(), changed_item.column(), changed_item.text())
        if success:
            return
        self.table.change_flag = True
        item.setText(value)

    def delete(self, item=None):
        for index in sorted(self.table.selectionModel().selectedRows(), reverse=True):
            if self.model_c.delete(index.row()):
                self.table.removeRow(index.row())

    def open_add_window(self):
        self.e = EditWindow.AddNew(self)

    def add(self, data):
        success, ad_data = self.model_c.add(data)
        if success:
            self.table.insertRow(self.table.rowCount())
            self.model_c.set_table_row(self.table, self.table.rowCount() - 1)
            self.table.selectRow(self.table.rowCount() - 1)
            return True, ad_data
        return False, ad_data

    def save_as(self, arr=None):
        if arr is None or arr is False:
            arr = []

        if len(arr) == 0:
            arr = self.model_c.temp_data
        self.model_c.split(arr)

    def split_by(self):
        if self.split is None:
            self.split = Split(self, self.model_c.possible_split(), self.model_c.split_by,
                               self.model_c.path_c.get_clear_file_name())
            return
        self.split.show()

    def merge_with(self):
        if self.merge is None:
            folder_path = SelectFiles("Select files", "*.csv")
            if folder_path.exec_() == QtWidgets.QDialog.Accepted:
                if self.model_c.merge(folder_path.selectedFiles()):
                    for index in range(self.table.rowCount(), len(self.model_c.data)):
                        self.table.insertRow(self.table.rowCount())
                        self.model_c.set_table_row(self.table, self.table.rowCount() - 1)
                    self.table.selectRow(self.table.rowCount() - 1)
            return
        self.split.show()

    def filter(self, parm):
        return self.model_c.filter(parm)

    def _filter(self, parm):
        self.filter_rows(self.filter(parm))

    def reset(self):
        for row in range(self.table.rowCount()):
            self.table.showRow(row)

    def toolbar(self, parm=None):
        if parm is None:
            parm = {
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
                "parent_relation": True,
                "child_relation": True
            }

        toolbar_set_u = {
            "title": "",
            "visible": True,
            "tools": {
                "options": [],
                "child": {
                    "child_relations": [],
                    "callback": self.open_file
                },
                "parent": {
                    "parent_relations": [],
                    "callback": self.open_file
                },
            }
        }

        if parm["save"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": f'Save - "{self.model_c.path_c.get_file_name()}"'
                },
                "icon": icon.SAVE_I(),
                "callback": self.save,
                "signal": "",
                "status_tip": f'Save changes on file {self.model_c.path_c.get_file_name()} .'
            })
        if parm["save_as"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": f'Save current filtered rows as new file'
                },
                "icon": icon.SAVE_AS_I(),
                "callback": self.save_as,
                "signal": "",
                "status_tip": f'Save changes on file {self.model_c.path_c.get_file_name()} .'
            })
        if parm["split"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": f'Split File'
                },
                "icon": icon.SPLIT_I(),
                "callback": self.split_by,
                "signal": "",
                "status_tip": f'Save changes on file {self.model_c.path_c.get_file_name()} .'
            })
        if parm["merge"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": f'Merge Files'
                },
                "icon": icon.MERGE_I(),
                "callback": self.merge_with,
                "signal": "",
                "status_tip": f'Save changes on file {self.model_c.path_c.get_file_name()} .'
            })
        if parm["filter"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": f'Filter - "{self.model_c.path_c.get_file_name()}"'
                },
                "icon": icon.FILTER_I(),
                "callback": self.input_w.show,
                "signal": "",
                "status_tip": f''
            })
        if parm["search"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": f'Search in file  - "{self.model_c.path_c.get_file_name()}"'
                },
                "icon": icon.SEARCH_I(),
                "callback": self.find,
                "signal": "",
                "status_tip": f''
            })
        if parm["add"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": f'Add new "{self.model_c.metadata_c.metadata["object_name"]}" to - "{self.model_c.path_c.get_file_name()}"'
                },
                "icon": icon.PLUS_MATH_I(),
                "callback": self.open_add_window,
                "signal": "",
                "status_tip": f''
            })
        if parm["reset"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": False,
                    "txt": ""
                },
                "icon": icon.RESET_I(),
                "callback": self.reset,
                "status_tip": f''
            })
        if parm["page_up"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": "PageUp"
                },
                "icon": icon.DOUBLE_UP(),
                "callback": self.go_to_first,
                "status_tip": f''
            })
        if parm["page_down"]:
            toolbar_set_u["tools"]["options"].append({
                "name": "",
                "tool_tip": {
                    "have": True,
                    "txt": "PageDown"
                },
                "icon": icon.DOUBLE_DOWN(),
                "callback": self.go_to_last,
                "status_tip": f''
            })
        if parm["parent_relation"]:
            toolbar_set_u["tools"]["parent"]["parent_relations"] = self.model_c.metadata_c.metadata["sequential_info"][
                "parent_relation"]
        if parm["child_relation"]:
            toolbar_set_u["tools"]["child"]["child_relations"] = self.model_c.metadata_c.metadata["sequential_info"][
                "child_relation"]

        return toolbar_set_u

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

        action = menu.exec_(self.table.viewport().mapToGlobal(pos))

        if action == delete_selected_rows:
            self.delete()

    def get_value(self, row, col):
        if not isinstance(col, int):
            col, _ = self.get_header_meta(col)

        if col is None or col >= self.table.columnCount():
            print("Coll does not exist")
            # super(Table, self).info("Column does not exist")

        return self.table.item(row, col).text()

    def get_header_meta(self, header_name):
        return self.model_c.metadata_c.get_header_meta(header_name)

    def set_horizontal_header_labels(self):
        for i in range(0, self.model_c.get_column_count()):
            self.table.setHorizontalHeaderItem(i, self.model_c.get_header_label(i))

    def sort_by_header(self, header):
        ...

    def get_selected_rows_indexes(self):
        return self.table.selectionModel().selectedRows()

    def check_path(self, file_path):
        return self.model_c.path_c.is_same(file_path)

    def filter_rows(self, arr):
        self.model_c.temp_data = arr
        for row in range(self.table.rowCount()):
            self.table.showRow(row) if row in arr else self.table.hideRow(row)

    def get_min_max(self, header_name):
        return self.model_c.get_min(header_name), self.model_c.get_max(header_name)

    def open_file(self, path):
        self.parent().open_file(path)

    def go_to_first(self):
        self.table.selectRow(0)

    def go_to_last(self):
        self.table.selectRow(self.table.rowCount() - 1)
