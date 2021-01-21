import re

from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor, QIcon
from PySide2.QtWidgets import QWidget, QGridLayout, QGroupBox, QVBoxLayout, QLabel, QLineEdit, QPushButton

from component.popup import Error, Success
from dataHandler.dataExtras.file import BOLD, PRIMARY_KEY_ICON, FOREIGN_KEY_ICON, PRIMARY_FOREIGN_KEY
from dataHandler.nesto.func import format_dict

WIDTH = 1920
HEIGHT = 1020


class EditWindow(QWidget):
    def __init__(self, table):
        super(EditWindow, self).__init__()
        self.table = table

        self.setWindowTitle(f'Add New - {self.table.model_c.path_c.get_file_name()}')
        self.setWindowState(Qt.WindowFullScreen)

        self.grid = QGridLayout()
        self.inputLayout = QVBoxLayout()

        for header in self.table.model_c.metadata_c.metadata["headers"]:
            self.inputLayout.addWidget(_InputHeader(self, header))

        self.button_add = QPushButton("ADD", self)
        self.button_add.clicked.connect(self.get_value)

        self.button_clear = QPushButton("Clear", self)
        self.button_clear.clicked.connect(self.clear)

        self.inputLayout.addStretch(1)

        self.grid.addLayout(self.inputLayout, 0, 0)
        self.grid.addWidget(self.button_add, 1, 0)
        self.grid.addWidget(self.button_clear, 1, 1)

        self.setLayout(self.grid)

        self.show()

    def get_value(self):
        item = {}
        for header_input in self.children():
            if not type(header_input).__name__ == '_InputHeader':
                continue
            value = header_input.get_value()
            if not value["is_valid"]:
                Error("Invalid input",
                     "You must fill all required fields",
                     "ii1",
                     f"You must fill filed '{value['name']}' ")
                return
            item.update({value['name']: value['value']})

        success, (have_valid_parent, contains_in_self) = self.table.add(item)
        if success:
            '''Success(f"New",
                    f"New ' {self.table.model_c.metadata_c.metadata['object_name']} ' successfully added .",
                    f"",
                    f"New ' {self.table.model_c.metadata_c.metadata['object_name']}' - \n\n{format_dict(item)} \n"
                    f" successfully added to file '{self.table.model_c.path_c.path}'")'''
            return

    def clear(self):
        for header_input in self.children():
            if not type(header_input).__name__ == '_InputHeader':
                continue
            header_input.clear()

    def check(self):
        for header_input in self.children():
            if not type(header_input).__name__ == '_InputHeader':
                continue
            header_input.clear()


class _InputHeader(QGroupBox):
    def __init__(self, parent, header):
        super().__init__(parent)
        self.header = header
        self.valid = not self.header["not_null"]

        self.header_index, _ = self.parent().table.model_c.metadata_c.get_header_meta(self.header["name"])
        self.common_values = self.parent().table.model_c.get_common_values(self.header["name"])

        # self.setFixedWidth(WIDTH*0.5)

        # LAYOUTS
        self.grid = QGridLayout()
        self.v_layout = QVBoxLayout()

        # FIELDS
        self.header_label = QLabel(f'{self.header["name"]} : ', self)
        self.header_label.setFixedWidth(WIDTH * 0.08)

        self.info_label = QLabel('')
        self.info_label.hide()

        self.type_label = QLabel('')
        self.type_label.hide()

        self.pixmap_label = QLabel()
        self.pixmap_label.setFixedWidth(16)

        pal = QPalette()
        pal.setColor(QPalette.Base, Qt.white)
        self.input = QLineEdit(self)
        self.input.setMaxLength(self.header["data_type"]["max_value"])
        self.input.textEdited.connect(self.check_input)
        self.input.editingFinished.connect(self.finish_editing)
        self.setPalette(pal)
        self.input.setPlaceholderText(
            "Some examples : " + str(self.common_values).replace("'", '').replace('[', '').replace(']', ''))

        self.validator = None
        if self.header["data_type"]["type"] == 'int':
            self.validator = _IntValidator(self.valid, self.header, self.info_label, self.type_label)

        if self.header["data_type"]["type"] == 'str':
            self.validator = HeaderValidator(self.valid, self.header, self.info_label, self.type_label)

        if self.header["data_type"]["type"] == 'date':
            self.validator = _DataValidator(self.valid, self.header, self.info_label, self.type_label)

        # SET UP

        self.icon = None
        if self.header["not_null"]:
            self.set_invalid()
            self.header_label.setFont(BOLD)

        if self.header["is_primary"]:
            self.icon = QIcon(PRIMARY_KEY_ICON)

        if self.header["is_foreign_key"]:
            self.icon = QIcon(FOREIGN_KEY_ICON)

        if self.header["is_primary"] and self.header["is_foreign_key"]:
            self.icon = QIcon(PRIMARY_FOREIGN_KEY)

        self.v_layout.addWidget(self.input)
        self.v_layout.addWidget(self.info_label)
        self.v_layout.addWidget(self.type_label)

        if self.icon is not None:
            pixmap = self.icon.pixmap(16, 16)
            self.pixmap_label.setPixmap(pixmap)

        self.grid.addWidget(self.pixmap_label, 0, 0)
        self.grid.addWidget(self.header_label, 0, 1)
        self.grid.addLayout(self.v_layout, 0, 2)

        self.setLayout(self.grid)

    def check_input(self, txt):
        if self.validator.validate(txt):
            self.set_valid()
        else:
            self.set_invalid()

    def set_valid(self):
        self.valid = True
        pal = QPalette()
        pal.setColor(QPalette.Base, QColor(152, 251, 152, 95))
        self.input.setPalette(pal)

    def set_invalid(self):
        self.valid = False
        pal = QPalette()
        pal.setColor(QPalette.Base, QColor(220, 20, 60, 55))
        self.input.setPalette(pal)

    def finish_editing(self):
        self.info_label.hide()
        self.type_label.hide()
        if not self.header["not_null"] and self.valid:
            self.set_valid()

    def get_value(self):
        return {"is_valid": self.valid,
                "name": self.header["name"],
                "value": self.input.text()}

    def clear(self):
        self.input.setText('')
        self.valid = not self.header["not_null"]
        if self.valid:
            self.set_valid()
        else:
            self.set_invalid()


class HeaderValidator:
    def __init__(self, valid, header, label1, label2):
        self.valid = valid
        self.header = header
        self.label1 = label1
        self.label2 = label2
        self.min = re.compile("^.{" + str(self.header["data_type"]["min_value"]) + ",}$")
        self.type = re.compile('^[a-zA-Z0-9_ ]*$')

    def show1(self, txt):
        self.label1.setText(txt)
        self.label1.show()

    def show2(self, txt):
        self.label2.setText(txt)
        self.label2.show()

    def hide1(self):
        self.label1.hide()

    def hide2(self):
        self.label2.hide()

    def validate(self, txt):
        self.valid = True
        if not self.header["not_null"] and len(txt) == 0:
            self.valid = True
            return True

        if self.min.match(txt) is None:
            self.show1(self.min_msg())
            self.valid = False
        else:
            self.hide1()

        if self.type.match(txt) is None:
            self.show2(self.type_msg())
            self.valid = False
        else:
            self.hide2()

        if self.valid:
            return True

        return False

    def min_msg(self):
        return f" * Minimum length of  '{self.header['name']}' is : {self.header['data_type']['min_value']}"

    def type_msg(self):
        return f" * '{self.header['name']}' must be STRING"


class _IntValidator(HeaderValidator):
    def __init__(self, valid, header, label1, label2):
        super().__init__(valid, header, label1, label2)
        self.type = re.compile('^\d+$')

    def type_msg(self):
        return f" * '{self.header['name']}' must be INTEGER"


class _DataValidator(HeaderValidator):
    def __init__(self, valid, header, label1, label2):
        super().__init__(valid, header, label1, label2)
        self.type = re.compile('^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$')

    def type_msg(self):
        return f" * '{self.header['name']}' must be DATE ( dd/mm/yyyy ) "
