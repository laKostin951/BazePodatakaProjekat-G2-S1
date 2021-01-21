import os

from dataHandler.dataExtras.metadata import METADATA_EXTRA_NAME


class Path:
    def __init__(self, path):
        self.path = path
        self.extension = self.get_extension()

    def is_same(self, other_path):
        this_path = self.path.split(os.path.sep)[-2:]
        other_path = other_path.split(os.path.sep)[-2:]

        return this_path[0] == other_path[0] and this_path[1] == other_path[1]

    def get_file_name(self):
        return self.path.split('/')[-1]
        # path        : /home/igork/singi/BazePodataka-S1G1/bp-projekat/podaci/student_data.csv
        # .split('/') : ["home","igork","singi" .... "student_data.csv"]
        # [-1]        : vracamo poslednji element gore navedenog niza - "student_data.csv"

    def get_clear_file_name(self):
        return self.get_file_name().split('.')[0]

    def get_extension(self):
        return self.get_file_name().split('.')[-1]
        # .split('.') : delimo "student_data.csv" na ["student_data", "csv"]
        # [-1]        : vracamo poslednji element gore navedenog niza - "csv" koji je ujedno i ekstenzija tog fajla

    def is_file(self):
        return self.get_extension() in ['csv', 'txt']
        # proveravamo da li je ekstanezija ".csv", ".txt" ....

    def get_metadata_path(self):
        return self.path.replace(('.' + self.extension), METADATA_EXTRA_NAME, 1)
        # zamenjujemo deo patha
        # ".csv" od "/home/igork/singi/BazePodataka-S1G1/bp-projekat/podaci/student_data.csv"
        # sa globalnom "METADATA_EXTRA_NAME"( _metadata.json ) kako bi dobili path do metadata poataka
        # tako da dobijamo path za metadata koji glasi
        # "/home/igork/singi/BazePodataka-S1G1/bp-projekat/podaci/student_data_metadata.json"
        # Ovo imenovanje metadata podataka je konvencija ustanovljena za rad sa datotekama na ovom
        # projektu

    def get_folder(self):
        return ""
