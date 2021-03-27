from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QPushButton, QMenu, QAction


class ButtonOptions(QPushButton):
    def __init__(self, parent, options, main_icon_path):
        super().__init__(parent)
        self.main_icon_path = main_icon_path
        self.options = options

        self.menu = QMenu(self)

        self.setIcon(QIcon(self.main_icon_path))
        self.setIconSize(QSize(22, 22))

        self.clicked.connect(self.showMenu)

        self.set_menu()

    def set_menu(self):
        for option in self.options:
            button = QAction(QIcon(option["icon"]), option["text"], self.parent())
            button.setToolTip(option['tooltip'])
            button.parm = str(option["parm"])
            button.callback = option["callback"]
            button.triggered.connect(self._call_callback_for_parm)

            self.menu.addAction(button)

        self.setMenu(self.menu)

    def _call_callback_for_parm(self):
        sender = self.sender()
        sender.callback(sender.parm)