import os

from PySide2 import QtWidgets, QtGui
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel, \
    QVBoxLayout, QGroupBox, QGridLayout, QSlider

from assets.style import styles


class Filter(QtWidgets.QDialog):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.table = parent
        self.callback = callback

        self.setWindowTitle(f'Filter Table - {self.table.model_c.path_c.get_file_name()}')
        self.setWindowIcon(QtGui.QIcon(f'assets{os.path.sep}img{os.path.sep}iconmonstr-filter-1-16.png'))
        self.setFixedWidth(600)

        self.main_v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.button_ok = QPushButton("Filter", self)
        self.button_ok.clicked.connect(self.doneR)

        self.button_cancel = QPushButton("Cancel", self)
        self.button_cancel.clicked.connect(self.cancel)

        self.h_layout.addWidget(self.button_ok)
        self.h_layout.addWidget(self.button_cancel)

        for header in self.table.model_c.metadata_c.metadata["headers"]:
            self.main_v_layout.addWidget(_InputHeader(self, header))

        self.main_v_layout.addLayout(self.h_layout)

        self.setLayout(self.main_v_layout)

    def doneR(self):
        conditions = []
        if self.callback is not None:
            for header_condition in self.children():
                if not type(header_condition).__name__ == '_InputHeader':
                    continue
                conditions.append(header_condition.get_condition())

            self.callback(conditions)
            self.hide()

    def cancel(self):
        self.hide()


class _InputHeader(QGroupBox):
    def __init__(self, parent, header):
        super().__init__(parent)
        self.header = header
        self.header_index, _ = self.parent().table.model_c.metadata_c.get_header_meta(self.header["name"])

        self.setStyleSheet(styles.filter_line_edit)

        # LAYOUTS
        self.grid = QGridLayout()
        self.v_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        # FIELDS
        self.header_label = QLabel(f'{self.header["name"]} : ', self)
        self.header_label.setFixedWidth(100)

        self.input = QLineEdit(self)
        self.input.setMaxLength(self.header["data_type"]["max_value"])
        self.input.setPlaceholderText(str(self.parent().table.model_c.get_common_values(header["name"])))

        self.exact = QCheckBox("Exact", self)
        self.exact.setToolTip(f"Value in '{self.header['name']}' must be exacly '{self.input.text()}'")
        self.exact.stateChanged.connect(self.exact_checked)

        # SLIDER SET UP
        self.slider = None

        if self.header["data_type"]["type"] == "int":
            self.slider = QSlider(Qt.Horizontal, self)
            (self.slider.min_v, self.slider.max_v) = self.parent().table.get_min_max(self.header["name"])
            self.slider.setMinimum(self.slider.min_v)
            self.slider.setMaximum(self.slider.max_v)
            self.slider.valueChanged.connect(self.slider_value_changed)
            self.slider.hint = QLabel(f'{self.slider.minimum()} - {self.slider.value()}', self)

        # SET UP
        self.h_layout.addWidget(self.input)
        self.h_layout.addWidget(self.exact)

        self.v_layout.addLayout(self.h_layout)
        if self.slider is not None:
            self.v_layout.addWidget(self.slider.hint)
            self.v_layout.addWidget(self.slider)

        self.grid.addWidget(self.header_label, 0, 0)
        self.grid.addLayout(self.v_layout, 0, 1)

        self.setLayout(self.grid)

    def get_condition(self):
        if self.input.text() == "" and self.slider is None:
            return None

        if self.slider is not None:
            if self.input.text() == "" and \
                    (self.slider.value() == self.slider.maximum() or
                     self.slider.value() == self.slider.minimum()):
                return None

        return {
            "header_name": self.header["name"],
            "value": self.input.text(),
            "exact": self.exact.isChecked(),
            "header_meta": {
                "index": self.header_index,
                "meta": self.header
            },
            "value_additional_info": {
                "contains": not self.exact.isChecked(),
                "min_value": self.slider.min_v if self.slider is not None else "",
                "max_value": self.slider.value() if self.slider is not None else ""
            }
        }

    def exact_checked(self):
        if self.slider is None:
            return
        self.slider.hide() if self.exact.isChecked() else self.slider.show()

    def slider_value_changed(self):
        self.slider.hint.setText(f'{self.slider.minimum()} - {self.slider.value()}')
