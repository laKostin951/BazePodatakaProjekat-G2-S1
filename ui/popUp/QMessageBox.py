from PySide2.QtWidgets import QMessageBox, QDialog

from assets.style import styles


class MessageBox(QMessageBox):
    def __init__(self, text, title, des):
        super().__init__()
        self.setStyleSheet(styles.msg_box)
        self.setIcon(QMessageBox.Information)
        self.setFixedWidth(600)
        self.setText(text)
        self.setWindowTitle(title)
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.setDetailedText(des)
