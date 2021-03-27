import csv
import os
from abc import ABC
from collections import Counter

from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QDir
from PySide2.QtGui import QFont, QIcon

from assets.config import DEFAULT_DATA_FOLDER
from ui.popUp.QMessageBox import MessageBox
from dataHandler.dataExtras._log_data import _LogDate
from dataHandler.dataExtras.abstract_table_model import AbstractTableModel
from dataHandler.dataExtras.changes import Changes
from dataHandler.dataExtras.file_msg import _FileMsg
from dataHandler.dataExtras.metadata import MetaData
from dataHandler.dataExtras.path import Path
from global_F.global_func import create_dir

BOLD = QFont()
BOLD.setBold(True)
PRIMARY_KEY_ICON = f'assets{os.path.sep}img{os.path.sep}primary-key.png'
FOREIGN_KEY_ICON = f'assets{os.path.sep}img{os.path.sep}foreign-key.png'
PRIMARY_FOREIGN_KEY = f'assets{os.path.sep}img{os.path.sep}primary_foreign_key.png'


def _dialog(title, name_filter, default_suffix):
    dialog = QtWidgets.QFileDialog()
    dialog.setWindowTitle(title)
    dialog.setNameFilter(name_filter)
    dialog.setDefaultSuffix(default_suffix)
    dialog.setDirectory(QDir.currentPath())
    dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
    return dialog


class File(AbstractTableModel, ABC):
    def __init__(self, path_c, auto_load=True, metadata_c=None, structure_dock=None):
        super().__init__()
        self.structure_dock = structure_dock
        if metadata_c is None:
            self.metadata_c = MetaData(path_c.get_metadata_path(), path_c)
        else:
            self.metadata_c = metadata_c

        self.path_c = path_c
        self.data = []
        self.temp_data = []
        self.changes = Changes()
        self.msg = _FileMsg(self)

        if auto_load:
            self.load()

    def __getitem__(self, index):
        return self.data[0]

    def load(self, file=None):
        try:
            data_file = open(self.path_c.path, 'r')

            reader = csv.DictReader(data_file,
                                    delimiter=self.metadata_c.metadata["dialect"]["delimiter"],
                                    fieldnames=self.metadata_c.get_headers_names(),
                                    quoting=self.metadata_c.metadata["dialect"]["quoting"])

            if self.metadata_c.metadata["dialect"]["skip_first_line"]:
                next(reader)

            for row in reader:
                self.data.append(row)

            data_file.close()
            del reader
        except:
            # print("Greska prilikom ucitavanaj")
            return
            super(File, self).info(f"We couldn’t find file '{self.path_c.get_file_name()}' "
                                   f"in '{self.path_c.get_absoulte_path()}'")
            super(File, self).write_log(_LogDate.load, None)

    def save(self):
        try:
            with open(self.path_c.path, 'w') as file:
                writer = csv.DictWriter(file,
                                        fieldnames=self.metadata_c.get_headers_names(),
                                        delimiter=self.metadata_c.metadata["dialect"]["delimiter"],
                                        quoting=self.metadata_c.metadata["dialect"]["quoting"])

                writer.writerows(self.data)
        except:
            # print("FILE  err")
            pass
        finally:
            ...
        # self.changes.save()

    def find(self, txt):
        matches = []
        txt = str.upper(str(txt))
        try:
            for index, value in enumerate(self.data):
                if txt in str.upper(str(value.values())):
                    matches.append(index)
            return matches
        except:
            pass
        finally:
            if len(matches) == 0:...
            ''' super(File, self).info(
                    f"We couldn’t find any data matching '{txt}' in folder '{self.path_c.get_folder()}'")'''
            # super(File, self).write_log(_LogDate.find, {"txt": txt})

    def filter(self, parm):
        matches = []
        try:
            for index, data_row in enumerate(self.data):
                def check():
                    for condition in parm:
                        if condition is None:
                            continue
                        if condition["exact"]:
                            if condition["value"] != data_row[condition["header_name"]]:
                                return
                            else:
                                continue

                        if not condition["value"] in data_row[condition["header_name"]]:
                            return

                        if condition["header_meta"]["meta"]["data_type"]["type"] == "str":
                            continue

                        if int(condition["value_additional_info"]["min_value"]) > int(
                                data_row[condition["header_name"]]) or \
                                int(condition["value_additional_info"]["max_value"]) < int(
                            data_row[condition["header_name"]]):
                            return

                    matches.append(index)

                check()

            return matches

        except:
            pass
        finally:
            super(File, self).write_log(_LogDate.filter, {"parm": parm})

    def change(self, row, col, value):
        data_row = self.data[row]
        try:

            header = self.metadata_c.metadata['headers'][col]

            changed_value = data_row[header["name"]]

            if not self._check_input(row, col, value, data_row, header):
                return False, data_row[header["name"]]

            data_row[header["name"]] = value

            return True, None
        except:
            return False, data_row
        finally:
            ...
            # TODO: LOG
            '''super(File, self).write_log(_LogDate.change, {
                "row": row,
                "col": col,
                "value": value
            })
            self.changes.add()'''

    def _check_input(self, row, col, value, data_row, header):
        try:
            if 0 > row or row >= self.get_row_count() or 0 > col or col >= self.get_column_count():
                return False, data_row[header["name"]]

            if header["data_type"]["type"] == "int":
                if not value.isdigit():
                    # TODO: POPUP vrednost koja je pokusana da se nije zadatog tipa
                    return False

            if len(value) < header["data_type"]["min_value"]:
                # TODO: POPUP vrednost koja je pokusana da se unse je manja od dozvoljene
                return False

            if len(value) > header["data_type"]["max_value"]:
                # TODO: POPUP vrednost koja je pokusana da se unse je veca od dozvoljene
                return False

            return True

        except:
            return False

    def delete(self, index):
        del self.data[index]
        self.write_log(_LogDate.delete, {"index": index})

    def add(self, data):
        ...

    def split(self, arr, file_path=None):
        if len(arr) == 0:
            arr = [index for index, _ in enumerate(self.data)]

        if file_path is not None:
            self._split_file(arr, file_path)
            return

        dialog = _dialog("Save File AS", "*.csv", ".csv")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._split_file(arr, f"{dialog.selectedFiles()[0]}.csv")

    def _split_file(self, arr, file_path):
        new_file_full_path = Path(str(file_path))

        new_file_metadata = MetaData(new_file_full_path.get_metadata_path(),
                                     new_file_full_path.path,
                                     False)
        new_file_metadata.metadata = self.metadata_c.metadata.copy()

        new_file = self.__class__(new_file_full_path, False, new_file_metadata)

        new_file.data = [data for index, data in enumerate(self.data) if index in arr]

        new_file.save()
        new_file.metadata_c.save()

        self.structure_dock.file_system.refresh()

    def possible_split(self):
        arr = (
            list(map(lambda header: {"name": header["name"], "split_by": False}, self.metadata_c.metadata["headers"])))

        for header_arr in arr:
            arr2 = (list(map(lambda data: data[header_arr["name"]], self.data)))
            counter = Counter(arr2)
            most_common = counter.most_common()
            for common in most_common:
                _, count = common
                if count > 1:
                    header_arr["split_by"] = True
                    continue

        return arr

    def split_by(self, parm):
        header = parm['Split by']
        folder_path = f"{DEFAULT_DATA_FOLDER}" \
                      f"{os.path.sep}" \
                      f"{self.path_c.get_clear_file_name()}_SPLIT_BY_{header}"

        current = self.data[0][header]
        current_index = 0
        file_path = f'{os.path.sep}' \
                    f'{self.path_c.get_clear_file_name()}' \
                    f'{self.data[0][header].replace(", ", "").replace(" ", "")}' \
                    f'.csv'
        arr = [{
            "file_path": file_path,
            "index_arr": []
        }]
        msg = f'CREATE folder {folder_path}\n'

        for index, v in enumerate(self.data):

            if v[parm['Split by']] == current:
                arr[current_index]["index_arr"].append(index)
                continue

            msg += f'CREATE file "{arr[current_index]["file_path"]}" ({len(arr[current_index]["index_arr"])})records\n'
            current_index += 1
            current = v[header]
            file_path = f'{os.path.sep}' \
                        f'{self.path_c.get_clear_file_name()}' \
                        f'{v[header].replace(", ", "").replace(" ", "")}' \
                        f'.csv'
            arr.append({
                "file_path": file_path,
                "index_arr": [index]
            })

        msg_box = MessageBox("Save changes",
                             "nista",
                             msg)
        result = msg_box.exec_()
        if result == 1024:
            folder_path = create_dir(folder_path, 0, folder_path)
            # print(folder_path)
            for file in arr:
                self._split_file(file["index_arr"], folder_path + file["file_path"])
        else:
            return

    def merge(self, arr):
        file_arr = []
        for file_path in arr:
            file = File(Path(file_path))
            if self.metadata_c.metadata != file.metadata_c.metadata:
                return
            file_arr.append(file)
        msg = ''
        for file in file_arr:
            msg += f"Merge with - {file.path_c.path} ({len(file.data)}Records)\n"

        msg_box = MessageBox("Merge Files",
                             "Do You want to merge this files",
                             msg)

        result = msg_box.exec_()
        if result == 1024:
            for file in file_arr:
                for data in file.data:
                    self.data.append(data.copy())
                file.delete()

            self.structure_dock.file_system.refresh()
            return True
        else:
            return

    def get_element(self, index):
        return self.data[index]

    def get_row_count(self):
        return len(self.data)

    def get_column_count(self):
        return len(self.metadata_c.metadata["headers"])

    def get_header_label(self, col):

        if col < 0 or col >= self.get_column_count():
            return False

        header_data = self.metadata_c.metadata['headers'][col]
        header = header_data["name"]

        header_item = QtWidgets.QTableWidgetItem(str(header))

        if header_data["is_primary"]:
            header_item.setIcon(QIcon(PRIMARY_KEY_ICON))
            header_item.setFlags(Qt.ItemIsSelectable)

        if header_data["is_foreign_key"]:
            header_item.setIcon(QIcon(FOREIGN_KEY_ICON))

        if header_data["is_primary"] and header_data["is_foreign_key"]:
            header_item.setIcon(QIcon(PRIMARY_FOREIGN_KEY))

        if header_data["not_null"]:
            header_item.setFont(BOLD)

        return header_item

    def set_table_row(self, table, row):
        row_objet = self.data[row]
        headers = self.metadata_c.get_headers_names()

        for col in range(0, self.get_column_count()):
            value = row_objet[headers[col]]
            table.change_flag = True
            table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    def get_file_name(self):
        return self.path_c.get_file_name()

    def get_min(self, header_name):
        if len(self.data) <= 0:
            return False

        min_v = self.data[0][header_name]

        for row in self.data:
            if row[header_name] < min_v:
                min_v = row[header_name]

        return int(min_v)

    def get_max(self, header_name):
        if len(self.data) <= 0:
            return False

        max_v = self.data[0][header_name]

        for row in self.data:
            if row[header_name] > max_v:
                max_v = row[header_name]

        return int(max_v)

    def create_change_log(self):

        pass

    def set_status_tip(self, txt):
        ...

    def get_common_values(self, header):
        _list = (list(map(lambda data: data[header], self.data)))
        arr2 = []
        for item in _list:
            if item in arr2:
                continue
            arr2.append(item)
        if len(arr2) > 4:
            arr2 = arr2[:4]
        return arr2

    def delete(self):
        self.metadata_c.delete()
        os.remove(self.path_c.path)

