import os

from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide2.QtWidgets import QAction, QPushButton, QFileDialog, \
    QHBoxLayout, QWidgetItem, QSpacerItem

from component.extra_window import ExtraWindow

CHILD_RELATION = f"assets{os.path.sep}img{os.path.sep}iconmonstr-generation-2-16.png"
PARENT_RELATION = f"assets{os.path.sep}img{os.path.sep}iconmonstr-generation-11-16.png"


class ToolBar(QtWidgets.QToolBar):
    def __init__(self):
        super().__init__()

        self.newAction = QAction(QIcon(f"assets{os.path.sep}img{os.path.sep}new.png"), "&New", self)
        self.openAction = QAction(QIcon(f"assets{os.path.sep}img{os.path.sep}open.png"), "&Open", self)
        self.printAction = QAction(QIcon(f"assets{os.path.sep}img{os.path.sep}print.png"), "&Print", self)

        self.editor_tool_bar = EditorToolBar(self)

        self.addAction(self.newAction)
        self.addAction(self.openAction)
        self.addAction(self.printAction)

        self.addSeparator()

        self.addWidget(self.editor_tool_bar)

        self.newAction.setStatusTip('New file')
        self.openAction.setStatusTip('Open file')
        self.printAction.setStatusTip('Print file')

        self.newAction.triggered.connect(self.open_new_table_dialog)
        self.openAction.triggered.connect(self.open_dialog_box)
        self.printAction.triggered.connect(self.print_preview_dialog)

    def open_new_table_dialog(self):
        extra_window = ExtraWindow(self)

    def open_dialog_box(self, file_path):
        filename = QFileDialog.getOpenFileName()
        self.parent().workspace._search_file(filename[0])

    def print_preview_dialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)

        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec_()

    def print_preview(self, printer):
        self.textEdit.print_(printer)


class EditorToolBar(QtWidgets.QGroupBox):
    def __init__(self, parent, parm=None):
        super().__init__(parent)

        self.main_title = f'Editor tool bar : '

        self.vbox = QHBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.setSpacing(10)

        self.setLayout(self.vbox)

        self.set_parm(parm)
        self.setTitle(self.main_title)
        self.set_options()

    def add_widget(self, widget):
        self.vbox.addWidget(widget)

    def show(self):
        self.setVisible(True)

    def set_current_file(self, file_path_c):
        self.setTitle(f'{self.main_title} {file_path_c.get_file_name()} |')

    def set_options(self):
        layout = self.layout()

        for option in self.parm["tools"]["options"]:
            button = QPushButton(QIcon(option["icon"]), option["name"], self.parent())
            if option["tool_tip"]["have"]:
                button.setToolTip(option["tool_tip"]["txt"])
            layout.insertWidget(-1, button)
            button.clicked.connect(option["callback"])

        layout.insertSpacing(self.layout().count(), 50)

        for index, child_relation in enumerate(self.parm["tools"]["child"]["child_relations"]):
            button = QPushButton(QIcon(CHILD_RELATION), child_relation["name_of_child_table"], self.parent())
            button.setToolTip(f'Go to CHILD table - "{child_relation["name_of_child_table"]}')
            button.parm = str(child_relation["path_of_child_table"])
            button.callback = self.parm["tools"]["child"]["callback"]

            layout.insertWidget(-1, button)

            button.clicked.connect(self.call_callback_for_parm)

        layout.insertSpacing(self.layout().count(), 20)

        for index, parent_relation in enumerate(self.parm["tools"]["parent"]["parent_relations"]):
            button = QPushButton(QIcon(PARENT_RELATION), parent_relation["name_of_child_table"], self.parent())
            button.setToolTip(f'Go to PARENT table - "{parent_relation["name_of_child_table"]}')
            button.parm = str(parent_relation["path_of_child_table"])
            button.callback = self.parm["tools"]["parent"]["callback"]

            layout.insertWidget(-1, button)

            button.clicked.connect(self.call_callback_for_parm)

    def print_m(self, txt):
        print(txt)

    def call_callback_for_parm(self):
        self.sender().callback(self.sender().parm)

    def set_parm(self, parm):
        if parm is None:
            parm = {
                "title": "",
                "visible": False,
                "tools": {
                    "options": [],
                    "child": {
                        "child_relations": [],
                        "callback": None
                    },
                    "parent": {
                        "parent_relations": [],
                        "callback": None
                    }
                }
            }

            """
            :arg :self.tools - python_dict
            [
                {
                    "name":"Save",
                    "tool_tip":"{
                        "have":False,
                        "txt":""
                    },
                    "icon":None,
                    "action": - pointer to mehod,
                    "status_tip:"Some status tip"
                }
            ]
            """

        self.parm = parm

    def reset(self, parm=None):
        layout = self.layout()

        self.clearLayout(layout)
        layout.setSpacing(1)

        self.set_parm(parm)
        self.set_options()
        layout.addStretch(1)

        self.set_current_file(self.parm["title"])

    def clearLayout(self, layout=None):
        if layout is None:
            layout = self.layout()
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                item.widget().close()
            elif isinstance(item, QSpacerItem):
                pass
            else:
                self.clearLayout(item.layout())

            print

            # remove the item from layout
            layout.removeItem(item)

        self.setTitle(self.main_title)
