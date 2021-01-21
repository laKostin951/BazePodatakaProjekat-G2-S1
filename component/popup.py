import os

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMessageBox


class Error(QMessageBox):
    def __init__(self, title, msg, err_code, des=""):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(f"Error code = {err_code}")
        self.setIcon(QMessageBox.Critical)
        self.setStandardButtons(QMessageBox.Ok)
        self.setInformativeText(msg)
        self.setDetailedText(des)

        execute = self.exec_()


class Success(QMessageBox):
    def __init__(self, title, msg, information_txt, des=""):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(msg)
        self.setIconPixmap(QIcon(f"assets{os.path.sep}img{os.path.sep}iconmonstr-check-mark-14-64.png").pixmap(32, 32))
        self.setStandardButtons(QMessageBox.Ok)
        self.setInformativeText(information_txt)
        self.setDetailedText(des)

        execute = self.exec_()


class Info(QMessageBox):
    def __init__(self, title, msg, information_txt, des=""):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(msg)
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)
        self.setInformativeText(information_txt)
        self.setDetailedText(des)

        execute = self.exec_()
