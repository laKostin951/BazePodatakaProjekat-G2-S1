from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, \
    QAbstractItemView, QSplitter, QGroupBox

import dataHandler.workspace.table.table as table
from config.settings import icon
from assets.style import styles
from ui.component.button_option import ButtonOptions
from ui.widget.edit import HeadersInput
from dataHandler.dataExtras.path import Path
from dataHandler.dataExtras.sq_file import SQFile


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.button_h_layout())


class AddNew(QWidget):
    def __init__(self, main_table):
        super(AddNew, self).__init__()
        self.table = main_table
        self.headers = main_table.model_c.metadata_c.metadata["headers"]
        self.title = f'Add New - {self.table.model_c.path_c.get_file_name()}'

        # DESCRIPTION
        self.setWindowTitle(self.title)
        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet(styles.main_dark)
        # MAIN LAYOUT
        self.main_v_layout = QVBoxLayout()

        # SPLITTER
        self.splitter = QSplitter(self)

        # MAIN TOOL BAR
        self.toolbar = QGroupBox(self)
        self.set_up_toolbar()

        # SIDE WORKSPACE
        self.side_widget = None

        # MAIN WORKSPACE
        main_workspace_layout = QVBoxLayout()
        self.main_widget = QWidget(self)
        self.headers_inputs = HeadersInput(self, self.headers)

        # MAIN WORKSPACE BUTTONS
        button_h_layout = QHBoxLayout()

        self.button_add = QPushButton("ADD", self)
        self.button_add.clicked.connect(self.add_new)

        self.button_clear = QPushButton("Clear", self)
        self.button_clear.clicked.connect(self.clear)

        button_h_layout.addWidget(self.button_add)
        button_h_layout.addWidget(self.button_clear)

        # SET UP
        main_workspace_layout.addWidget(self.headers_inputs)
        main_workspace_layout.addLayout(button_h_layout)

        self.main_widget.setLayout(main_workspace_layout)

        self.splitter.addWidget(self.main_widget)

        self.main_v_layout.addWidget(self.toolbar)
        self.main_v_layout.addWidget(self.splitter)

        self.setLayout(self.main_v_layout)

        self.show()

    def add_new(self):
        item = self.headers_inputs.get_values()
        if not item:
            return
        _, contains_in_self = self.table.add(item)

        self.open_home_table()


    def clear(self):
        self.headers_inputs.clear()

    def open_home_table(self):
        if self.side_widget is not None:
            self.side_widget.close()

        self.side_widget = SideTable(self, self.table.model_c)

        self.splitter.insertWidget(-1, self.side_widget)

    def set_up_toolbar(self):
        vbox = QHBoxLayout()

        self.toolbar.setStyleSheet(styles.tool_bar_groupbox_dark)
        vbox.setAlignment(Qt.AlignLeft)
        vbox.setContentsMargins(10, 0, 0, 0)
        self.toolbar.setLayout(vbox)
        self.toolbar.setFixedHeight(40)

        home_table = QPushButton(QIcon(icon.HOME_SCREEN_I()), "", self.toolbar)

        vbox.addWidget(home_table)

        parent_relation_option = (list(map(lambda relation: {
                "text": relation["name_of_child_table"],
                "parm": relation["path_of_child_table"],
                "icon": icon.MULTICAST_I(),
                "callback": self.open_parent,
                "tooltip": relation["name_of_relation"]
            }, self.table.model_c.metadata_c.metadata["sequential_info"]["parent_relation"])))

        if len(parent_relation_option) > 0:
            select_parent = ButtonOptions(self.toolbar,
                                          parent_relation_option,
                                          icon.MULTICAST_I())

            vbox.addWidget(select_parent)

        child_relations_options = (list(map(lambda relation: {
            "text": relation["name_of_child_table"],
            "parm": relation["path_of_child_table"],
            "icon": icon.MULTICAST_I(),
            "callback": self.open_parent,
            "tooltip": relation["name_of_relation"]
        }, self.table.model_c.metadata_c.metadata["sequential_info"]["child_relation"])))

        if len(child_relations_options) > 0:
            add_child = ButtonOptions(self.toolbar,
                                      child_relations_options,
                                      icon.DOWN_BUTTON_I())

            vbox.addWidget(add_child)

        home_table.setStatusTip(f"Open '{self.table.model_c.path_c.path}'")
        home_table.clicked.connect(self.open_home_table)

    def open_parent(self, path):
        if self.side_widget is not None:
            self.side_widget.close()

        self.side_widget = SideTableSelectParent(self,
                                                 SQFile(Path(path), True),
                                                 self.headers_inputs.set_parent,
                                                 self.table.model_c.path_c)

        self.splitter.insertWidget(-1, self.side_widget)

    def open_child(self, path):
        ...


class SideTable(QWidget):
    def __init__(self, parent, model_c):
        super().__init__(parent)
        self.model_c = model_c

        side_workspace_v_layout = QVBoxLayout()

        button_close = QPushButton("Close", parent)
        button_close.clicked.connect(self.close)

        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.addWidget(button_close)

        self.table = table.Table(parent, model_c, True)
        self.table.tool_bar.set_parm(self.table.toolbar({
            "save": False,
            "save_as": False,
            "split": False,
            "merge": False,
            "filter": True,
            "search": True,
            "add": False,
            "reset": True,
            "page_up": True,
            "page_down": True,
            "parent_relation": False,
            "child_relation": False
        }))
        self.table.table.setSelectionMode(QAbstractItemView.SingleSelection)

        side_workspace_v_layout.addWidget(self.table)
        side_workspace_v_layout.addLayout(self.button_h_layout)

        self.setLayout(side_workspace_v_layout)

    def close(self):
        self.setParent(None)


class SideTableSelectParent(SideTable):
    def __init__(self, parent, model_c, callback, child_path_c):
        super().__init__(parent, model_c)
        self.child_index = self.model_c.get_relation_index_by_path(child_path_c, "child_relation")
        self.callback = callback

        button_select = QPushButton("Select", parent)
        button_select.clicked.connect(self.select)

        self.button_h_layout.addWidget(button_select)

    def select(self):
        data = self.model_c.data[self.table.table.selectionModel().selectedRows()[0].row()]
        relation = self.model_c.get_relation_point(self.child_index, data)
        self.callback(relation)
