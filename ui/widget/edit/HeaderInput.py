from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QIcon
from PySide2.QtWidgets import QGroupBox, QGridLayout, QVBoxLayout, QLabel, QLineEdit

from config.settings import WIDTH
from assets.style import styles
from ui.widget.edit import HeaderValidator, TypeValidInt, TypeValidDate
from dataHandler.dataExtras.file import BOLD, PRIMARY_KEY_ICON, FOREIGN_KEY_ICON, PRIMARY_FOREIGN_KEY


class HeaderInput(QGroupBox):
    def __init__(self, parent, header, value, common_values):
        super().__init__(parent)
        self.header = header
        self.valid = not self.header["not_null"]

        self.setStyleSheet(styles.header_input_groupbox_dark)

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
        if value is None or not value or len(value) == 0:
            self.input.setPlaceholderText(
                "Some examples : " + str(common_values).replace("'", '').replace('[', '').replace(']', ''))
        else:
            self.input.setText(value)

        self.validator = None
        if self.header["data_type"]["type"] == 'int':
            self.validator = TypeValidInt(self.valid, self.header, self.info_label, self.type_label)

        if self.header["data_type"]["type"] == 'str':
            self.validator = HeaderValidator(self.valid, self.header, self.info_label, self.type_label)

        if self.header["data_type"]["type"] == 'date':
            self.validator = TypeValidDate(self.valid, self.header, self.info_label, self.type_label)

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
            self.pixmap_label.setPixmap(self.icon.pixmap(16, 16))

        self.grid.addWidget(self.pixmap_label, 0, 0)
        self.grid.addWidget(self.header_label, 0, 1)
        self.grid.addLayout(self.v_layout, 0, 2)

        self.setLayout(self.grid)

    def check_input(self, txt):
        self.set_valid() if self.validator.validate(txt) else self.set_invalid()

    def set_valid(self):
        self.valid = True
        self.input.setStyleSheet(styles.input_valid)

    def set_invalid(self):
        self.valid = False
        self.input.setStyleSheet(styles.input_invalid)

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
        self.set_valid() if self.valid else self.set_invalid()

    def set_value(self, value):
        self.check_input(value)
        self.input.setText(value)
