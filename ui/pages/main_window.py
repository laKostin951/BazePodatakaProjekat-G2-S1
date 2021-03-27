from PySide2 import QtWidgets, QtGui, QtCore

from ui.widget.menu_bar import MenuBar
from ui.widget.status_bar import StatusBar
from ui.widget.structure_dock import StructureDock
from ui.widget.toolbar.tool_bar import ToolBar
from dataHandler.workspace.workspaceWidget import WorkspaceWidget


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.resize(600, 480)
        self.setWindowTitle("Editor generickih podataka")
        self.setWindowIcon(QtGui.QIcon("../../assets/img/icons8-edit-file-64.png"))

        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

        self.structure_dock = StructureDock("Structure dock", self)

        self.workspace = WorkspaceWidget(self, self.status_bar, self.structure_dock)

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.toggle_structure_dock_action = self.structure_dock.toggleViewAction()
        self.menu_bar.view_menu.addAction(self.toggle_structure_dock_action)

        self.structure_dock.clicked.connect(self.workspace.open_file)
        self.structure_dock.sql_clicked.connect(self.workspace.open_file)

        self.tool_bar = ToolBar()
        self.addToolBar(self.tool_bar)

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.structure_dock)
        self.setCentralWidget(self.workspace)

        self.show()
