class Changes:
    def __init__(self):
        self.saved = True
        self.unsaved_no = 0
        self.changes = []
        self.auto_save = 999

    def save(self):
        self.write_log()
        self.saved = True
        self.unsaved_no = 0
        self.changes = []

    def write_log(self):
        pass

    def add(self): ...

