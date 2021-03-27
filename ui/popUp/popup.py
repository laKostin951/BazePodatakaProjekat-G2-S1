import os

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMessageBox

from assets.style import styles


class MessageBox(QMessageBox):
    def __init__(self, title, text, des):
        super().__init__()
        self.setStyleSheet(styles.msg_box)
        self.setWindowTitle(title)
        self.setText(text)
        self.setDetailedText(des)
        self.setFixedWidth(600)
        self.setStandardButtons(QMessageBox.Ok)

        execute = self.exec_()


class Error(MessageBox):
    def __init__(self, title, text, des, err_code):
        super().__init__(title, text, des)
        self.setInformativeText(f"Error code = {err_code}")
        self.setIcon(QMessageBox.Critical)


class Success(MessageBox):
    def __init__(self, title, text, information_txt, des=""):
        super().__init__(title, text, des)
        self.setIconPixmap(QIcon(f"assets{os.path.sep}img{os.path.sep}iconmonstr-check-mark-14-64.png").pixmap(32, 32))
        self.setInformativeText(information_txt)


class Info(MessageBox):
    def __init__(self, title, text, information_txt, des=""):
        super().__init__(title, text, des)
        self.setIcon(QMessageBox.Warning)
        self.setInformativeText(information_txt)

