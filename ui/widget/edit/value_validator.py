import re


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


class TypeValidInt(HeaderValidator):
    def __init__(self, valid, header, label1, label2):
        super().__init__(valid, header, label1, label2)
        self.type = re.compile('^\d+$')

    def type_msg(self):
        return f" * '{self.header['name']}' must be INTEGER"


class TypeValidDate(HeaderValidator):
    def __init__(self, valid, header, label1, label2):
        super().__init__(valid, header, label1, label2)
        self.type = re.compile('^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$')

    def type_msg(self):
        return f" * '{self.header['name']}' must be DATE ( dd/mm/yyyy ) "