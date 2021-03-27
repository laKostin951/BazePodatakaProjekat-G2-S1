from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QLabel, \
    QVBoxLayout, QAction

from config.settings import icon
from assets.style import styles


class MenuButton(QtWidgets.QWidget):
    def __init__(self, parent, text, options):
        super().__init__(parent)

        self.options = options
        self.text = text
        self.value = None

        self.setStyleSheet("color:white;")

        self.h_layout = QHBoxLayout()

        self.label = QLabel(self.text)

        self.combo_box = QPushButton('', self)
        self.combo_box.clicked.connect(self.combo_box.showMenu)

        self.menu = QtWidgets.QMenu(self)

        for header in self.options:
            button = QAction(header["name"], self)
            button.parm = header["name"]
            button.valid = header['split_by']
            if header['split_by']:
                button.triggered.connect(self.change_combo_box)
            else:
                button.setIcon(QIcon(icon.UNAVAILABLE_I()))

            self.menu.addAction(button)
        self.combo_box.setMenu(self.menu)

        def set_default():
            for action in self.menu.actions():
                if action.valid:
                    action.trigger()
                    return

        set_default()

        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.combo_box)

        self.setLayout(self.h_layout)

    def _call_callback_for_parm(self):
        self.sender().callback(self.sender().parm)

    def change_combo_box(self):
        self.value = self.sender().parm
        self.combo_box.setText(self.value)


class Split(QtWidgets.QDialog):
    def __init__(self, parent, headers, callback, file_name):
        super().__init__(parent)
        self.file_name = file_name
        self.callback = callback
        self.headers = headers

        self.setFixedWidth(500)
        self.setStyleSheet(styles.split)

        self.v_layout = QVBoxLayout()
        self.button_h_layout = QHBoxLayout()

        self.split_by_btn = MenuButton(self, "Split By : ", self.headers)

        # CUSTOMIZE OPTIONS
        # SELECT FOLDER
        # DEFAULT OPTIONS
        # BUTTONS
        self.split_btn = QPushButton(QIcon(icon.SPLIT_I()), "Split", self)
        self.split_btn.clicked.connect(self.split)

        self.cancel_btn = QPushButton(QIcon(icon.DELETE_I()), "Cancel", self)
        self.cancel_btn.clicked.connect(self.close)

        self.button_h_layout.addWidget(self.split_btn)
        self.button_h_layout.addWidget(self.cancel_btn)

        # SET UP
        self.v_layout.addWidget(self.split_by_btn)
        self.v_layout.addSpacing(20)
        self.v_layout.addLayout(self.button_h_layout)

        self.setLayout(self.v_layout)
        self.show()

    def cancel(self):
        self.close()

    def split(self):
        parm = {
            "Split by": self.split_by_btn.value
        }

        self.callback(parm)
