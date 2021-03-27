import os

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea

from config.settings import HEIGHT, icon
from assets.style import styles
from dataHandler.dataExtras.metadata import MetaData
from dataHandler.dataExtras.path import Path, MySqlPath
from dataHandler.mySql.mysql_file import format_mysql


class FileSystemModel(QWidget):
    def __init__(self, open_file_call, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.open_file_call = open_file_call

        self.setStyleSheet(styles.file_path_button)
        self.setMaximumHeight(HEIGHT)

        self.v_layout = QVBoxLayout()

        self.area = QScrollArea(self)
        self.area.setWidgetResizable(True)

        self.refresh_btn = QPushButton(QIcon(icon.RESET_I()), '', self)
        self.refresh_btn.clicked.connect(self.refresh)

        self.v_layout.addWidget(self.refresh_btn)
        self.v_layout.addWidget(self.area)

        self.set_scroll_area()

        self.setLayout(self.v_layout)

    def refresh(self):
        w = self.area.widget()
        w.setParent(None)
        del w
        self.set_scroll_area()

    def set_scroll_area(self):

        scroll_content = QWidget(self.area)
        scroll_layout = QVBoxLayout(scroll_content)

        scroll_content.setLayout(scroll_layout)

        _list = sorted(os.listdir(self.folder_path))

        for file in _list:
            file_absolute_path = self.folder_path + os.path.sep + file

            if os.path.isdir(file_absolute_path):
                scroll_layout.addWidget(Folder(scroll_content,
                                               self.open_file_call,
                                               self.folder_path + os.path.sep + file))
                continue

            if os.path.splitext(file_absolute_path)[1] != '.csv':
                continue

            scroll_layout.addWidget(FilePathButton(scroll_content,
                                                   file,
                                                   file_absolute_path,
                                                   self.open_file_call))

        scroll_layout.addStretch(1)

        self.area.setWidget(scroll_content)


class FilePathButton(QWidget):
    def __init__(self, parent, file_name, file_path, callback):
        super().__init__(parent)
        self.file_path = file_path
        self.callback = callback

        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(0)
        self.v_layout.setMargin(0)

        file_icon = QIcon(icon.TABLE_I())
        file_paht_c = Path(file_path)
        file_metadata_path = file_paht_c.get_metadata_path()
        file_metadata_c = None
        if os.path.isfile(file_metadata_path):
            file_metadata_c = MetaData(file_metadata_path, file_paht_c, True)
            if file_metadata_c.metadata["sequential_info"]["is_sequential"]:
                file_icon = QIcon(icon.RELATION_TABLE_I())

        self.btn = QPushButton(file_icon, file_name, self)
        self.btn.clicked.connect(self.send)

        self.v_layout.addWidget(self.btn)
        self.setLayout(self.v_layout)

    def send(self):
        self.callback(self.file_path)


class Folder(QWidget):
    def __init__(self, parent, open_file_call, folder_path):
        super().__init__(parent)
        self.folder_path = folder_path
        self.folder_open = False

        self.setStyleSheet(styles.file_path_button)

        self.main_v_layout = QVBoxLayout()
        self.main_v_layout.setSpacing(2)
        self.main_v_layout.setMargin(0)

        self.files = QWidget(self)
        self.files.hide()
        self.files.setStyleSheet(styles.files_list)
        self.files.setContentsMargins(15, 0, 0, 0)
        self.files_v_layout = QVBoxLayout()

        self.folder_btn = QPushButton(QIcon(icon.FOLDER_I()),
                                      self.folder_path.split(os.path.sep)[-1],
                                      self)
        self.folder_btn.clicked.connect(self.open_folder)

        self.main_v_layout.addWidget(self.folder_btn)

        _list = sorted(os.listdir(self.folder_path))

        for file in _list:
            file_absolute_path = self.folder_path + os.path.sep + file

            if os.path.isdir(file_absolute_path):
                self.files_v_layout.addWidget(Folder(
                    self.files,
                    open_file_call,
                    self.folder_path + os.path.sep + file))
                continue

            if os.path.splitext(file_absolute_path)[1] != '.csv':
                continue
            file_btn = FilePathButton(self.files, file, file_absolute_path, open_file_call)
            self.files_v_layout.addWidget(file_btn)

        self.files.setLayout(self.files_v_layout)

        self.main_v_layout.addWidget(self.files)

        self.setLayout(self.main_v_layout)

    def open_folder(self):
        self.close() if self.folder_open else self.open()
        self.folder_open = not self.folder_open

    def open(self):
        self.files.show()
        self.folder_btn.setIcon(QIcon(icon.OPENED_FOLDER_I()))

    def close(self):
        self.files.hide()
        self.folder_btn.setIcon(QIcon(icon.FOLDER_I()))


class ServerDatabaseSystem(QWidget):
    def __init__(self, open_file_call, conn):
        super().__init__()
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.open_file_call = open_file_call

        self.setStyleSheet(styles.file_path_button)
        self.setMaximumHeight(HEIGHT)

        self.v_layout = QVBoxLayout()

        self.area = QScrollArea(self)
        self.area.setWidgetResizable(True)

        self.refresh_btn = QPushButton(QIcon(icon.RESET_I()), '', self)
        self.refresh_btn.clicked.connect(self.refresh)

        self.v_layout.addWidget(self.refresh_btn)
        self.v_layout.addWidget(self.area)

        self.set_scroll_area()

        self.setLayout(self.v_layout)

    def refresh(self):
        w = self.area.widget()
        w.setParent(None)
        del w
        self.set_scroll_area()

    def set_scroll_area(self):
        scroll_content = QWidget(self.area)
        scroll_layout = QVBoxLayout(scroll_content)

        scroll_content.setLayout(scroll_layout)

        self.cursor.callproc('getAllTablesFromSchema', ["sistem_visokoskolske_ustanove"])
        _list = sorted(format_mysql(self.cursor.stored_results()))

        for table in _list:
            '''if os.path.isdir(file_absolute_path):
                scroll_layout.addWidget(Folder(scroll_content,
                                               self.open_file_call,
                                               self.connection + os.path.sep + table))
                continue

            if os.path.splitext(file_absolute_path)[1] != '.csv':
                continue
            '''
            scroll_layout.addWidget(SQLTable(scroll_content,
                                             table[1],
                                             table[1],
                                             self.open_file_call))

        scroll_layout.addStretch(1)

        self.area.setWidget(scroll_content)
        self.cursor.close()
        #self.conn.close()


class SQLTable(QWidget):
    def __init__(self, parent, file_name, file_path, callback):
        super().__init__(parent)
        self.file_path = file_path
        self.callback = callback

        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(0)
        self.v_layout.setMargin(0)

        file_icon = QIcon(icon.RELATION_TABLE_I())
        file_paht_c = MySqlPath(file_path)

        self.btn = QPushButton(file_icon, file_name, self)
        self.btn.clicked.connect(self.send)

        self.v_layout.addWidget(self.btn)
        self.setLayout(self.v_layout)

    def send(self):
        self.callback(self.file_path)
