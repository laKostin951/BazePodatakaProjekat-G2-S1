import os

from PySide2 import QtWidgets, QtCore


class StructureDock(QtWidgets.QDockWidget):
    clicked = QtCore.Signal(str)  # class attribute

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.currentPath())
        self.model.setNameFilters(['*.csv'])

        self.tree = QtWidgets.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QtCore.QDir.currentPath() + os.path.sep + "data"))
        self.tree.clicked.connect(self.file_clicked)

        self.setWidget(self.tree)

    def file_clicked(self, index):
        path = self.model.filePath(index)
        self.clicked.emit(path)
