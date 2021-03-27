from PySide2.QtWidgets import QWidget, QVBoxLayout

from ui.widget.edit import HeaderInput
from ui.popUp.popup import Error


class HeadersInput(QWidget):
    def __init__(self, parent, headers, values=None):
        super().__init__(parent)
        self.values = {}
        self.inputs_arr = []
        self.headers = headers

        if values is None:
            for header in headers:
                self.values.update({header["name"]: ""})
        else:
            self.values = values

        self.inputLayout = QVBoxLayout()

        for header in headers:
            value = self.values[header["name"]]
            common_values = []
            if value is None or not value or len(value) == 0:
                common_values = self.parent().table.model_c.get_common_values(header["name"])
            header_input = HeaderInput(self, header, value, common_values)
            self.inputLayout.addWidget(header_input)
            self.inputs_arr.append(header_input)

        self.inputLayout.addStretch(1)
        self.setLayout(self.inputLayout)

    def get_values(self):
        item = {}
        for header_input in self.inputs_arr:
            value = header_input.get_value()
            if not value["is_valid"]:
                Error("Invalid input",
                      "You must fill all required fields",
                      "ii1",
                      f"You must fill filed '{value['name']}' ")
                return False
            item.update({value['name']: value['value']})

        return item

    def clear(self):
        for header_input in self.inputs_arr:
            header_input.clear()

    def set_parent(self, parent_relation_to_child_self):
        for relation in parent_relation_to_child_self:
            header_name = relation['header_name']
            header_value = relation['value']
            for index, header in enumerate(self.headers):
                if header["name"] == header_name:
                    self.inputs_arr[index].set_value(header_value)

