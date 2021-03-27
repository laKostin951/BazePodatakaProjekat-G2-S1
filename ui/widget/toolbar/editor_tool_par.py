from PySide2 import QtWidgets
from PySide2.QtCore import QSize
from PySide2.QtGui import Qt, QIcon
from PySide2.QtWidgets import QHBoxLayout, QPushButton

from config.settings import icon
from assets.style import styles
from ui.component.button_option import ButtonOptions


class EditorToolBar(QtWidgets.QGroupBox):
    def __init__(self, parent, parm=None):
        super().__init__(parent)

        self.setStyleSheet(styles.tool_bar_groupbox_dark)

        self.parm = parm

        self.vbox = QHBoxLayout()

        self.vbox.setSpacing(1)
        self.vbox.setAlignment(Qt.AlignRight)
        self.vbox.setContentsMargins(10, 0, 0, 0)

        self.setLayout(self.vbox)

        self.set_options()

    def set_parm(self, parm):
        self.parm = parm
        self.set_options()

    def set_options(self):
        if self.parm is None:
            return
        layout = self.layout()

        for option in self.parm["tools"]["options"]:
            button = QPushButton(QIcon(option["icon"]), option["name"], self.parent())
            if option["tool_tip"]["have"]:
                button.setToolTip(option["tool_tip"]["txt"])
            layout.insertWidget(-1, button)
            button.clicked.connect(option["callback"])
            button.setIconSize(QSize(22, 22))

        layout.insertSpacing(self.layout().count(), 50)

        if len(self.parm["tools"]["child"]["child_relations"]) > 0:
            child_relation_option = (list(map(lambda relation: {
                "text": relation["name_of_child_table"],
                "parm": relation["path_of_child_table"],
                "icon": icon.DOWN_ARROW_I(),
                "callback": self.parm["tools"]["child"]["callback"],
                "tooltip": f"Go to - {relation['path_of_child_table']}"
            }, self.parm["tools"]["child"]["child_relations"])))

            button = ButtonOptions(self, child_relation_option, icon.DOWN_BUTTON_I())
            layout.insertWidget(-1, button)

        if len(self.parm["tools"]["parent"]["parent_relations"]) > 0:

            parent_relation_option = (list(map(lambda relation: {
                "text": relation["name_of_child_table"],
                "parm": relation["path_of_child_table"],
                "icon": icon.UP_ARROW_I(),
                "callback": self.parm["tools"]["child"]["callback"],
                "tooltip": f"Go to - {relation['path_of_child_table']}"
            }, self.parm["tools"]["parent"]["parent_relations"])))

            button = ButtonOptions(self, parent_relation_option, icon.SLIDE_UP() )
            layout.insertWidget(-1, button)

        self.vbox.addStretch(1)

    def call_callback_for_parm(self):
        self.sender().callback(self.sender().parm)

    def insert_widget(self, parm, index=-1):
        button = QPushButton(QIcon(parm["icon"]), parm["name"], self.parent())
        if parm["tool_tip"]["have"]:
            button.setToolTip(parm["tool_tip"]["txt"])
        self.layout().insertWidget(index, button)
        button.clicked.connect(parm["callback"])
        button.setIconSize(QSize(22, 22))
