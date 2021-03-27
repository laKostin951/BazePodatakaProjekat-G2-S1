from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide2.QtWidgets import QAction, QFileDialog

from config.settings import icon
from ui.pages.extra_window import ExtraWindow


class ToolBar(QtWidgets.QToolBar):
    def __init__(self):
        super().__init__()

        self.newAction = QAction(QIcon(icon.ADD_FILE_I()), "&New", self)
        self.openAction = QAction(QIcon(icon.FOLDER_I()), "&Open", self)
        self.printAction = QAction(QIcon(icon.PRINT_I()), "&Print", self)

        self.addAction(self.newAction)
        self.addAction(self.openAction)
        self.addAction(self.printAction)

        self.addSeparator()

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
        self.parent().workspace.open_file(filename[0])

    def print_preview_dialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)

        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec_()

    def print_preview(self, printer):
        self.textEdit.print_(printer)
