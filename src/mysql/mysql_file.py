import re

import mysql
from PySide2 import QtWidgets

from assets.config import cnxpool
from mysql.connector import  errorcode

from cache.server.connections import Connections
from ui.popUp.popup import Success, Error
from dataHandler.dataExtras.file import File
from dataHandler.dataExtras.metadata import MetaData
from dataHandler.dataExtras.path import Path
from global_F.global_func import format_dict

connections = Connections()

#cnxpool = make_pool_party(connections[0])


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def format_mysql(cursor_results):
    arr = []
    for row in cursor_results:
        for data in row.fetchall():
            arr.append(data)
    return arr


class MYSQLFile(File):
    def __init__(self, path_c, metadata_c=None, structure_dock=None):
        self.metadata_c = metadata_c
        if metadata_c is None:
            self.metadata_c = MetaData(None, None, False)

        super().__init__(path_c, False, self.metadata_c, structure_dock)

        self.pool = cnxpool
        self.load_metadata()
        self.load()

    def load(self):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc("load_table", [self.path_c.path])
            raw_data = format_mysql(cursor.stored_results())
            headers_name = self.metadata_c.get_headers_names()
            for data in raw_data:
                self.data.append(data)
        except :
            pass
        finally:
            cursor.close()

    def load_metadata(self):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        metadata = {
            "headers": [],
            "headers_count": 0,
            "object_name": "",
            "sequential_info": {
                "is_sequential": True,
                "child_relation": None,
                "parent_relation": None,
                "bridge_relation": []
            }
        }

        cursor.callproc('getChildRelation', [self.path_c.path])
        child_relation_raw = format_mysql(cursor.stored_results())
        child_relation = []
        if len(child_relation_raw) != 0:

            curent_table_relation = None

            for row in child_relation_raw:
                if row[1] == curent_table_relation:
                    child_relation[len(child_relation) - 1]["relation_on"].append({
                        "this_table_key": row[5],
                        "child_table_key": row[2]
                    })
                    continue
                child_relation.append({
                    "name_of_relation": row[1],
                    "name_of_child_table": f"{row[1]}",
                    "path_of_child_table": f"{row[1]}",
                    "relation_on": [{
                        "this_table_key": row[5],
                        "child_table_key": row[2]
                    }]
                })
                curent_table_relation = row[1]
        metadata["sequential_info"]["child_relation"] = child_relation

        cursor.callproc('getParentRelation', [self.path_c.path])
        parent_relation_raw = format_mysql(cursor.stored_results())
        parent_relation = []
        forgin_headers_arr = []
        if len(child_relation_raw) != 0:

            curent_table_relation = None

            for row in parent_relation_raw:
                if row[1] == curent_table_relation:
                    parent_relation[len(parent_relation) - 1]["relation_on"].append({
                        "this_table_key": row[2],
                        "child_table_key": row[5]
                    })
                    forgin_headers_arr.append(row[2])
                    continue
                parent_relation.append({
                    "name_of_relation": row[4],
                    "name_of_child_table": f"{row[4]}",
                    "path_of_child_table": f"{row[4]}",
                    "relation_on": [{
                        "this_table_key": row[2],
                        "child_table_key": row[5]
                    }]
                })
                forgin_headers_arr.append(row[2])
                curent_table_relation = row[4]
        metadata["sequential_info"]["parent_relation"] = parent_relation

        cursor.callproc('describeTable', [self.path_c.path])
        headers_raw = format_mysql(cursor.stored_results())
        for header in headers_raw:
            metadata["headers"].append({
                "name": header[0],
                "is_primary": header[3] == "PRI",
                "is_foreign_key": header[0] in forgin_headers_arr,
                "data_type": None,
                "predefined_values": None,
                "not_null": header[2] == "NO"
            })

            if re.match(r"varchar\([0-9]+\)", header[1]):
                max_value = int(header[1].split("(")[-1].split(")")[0])
                metadata["headers"][-1]["data_type"] = {
                    "type": "str",
                    "min_value": 1,
                    "max_value": max_value
                }
                continue

            if re.match(r"smallint\([0-9]+\)", header[1]):
                max_value = int(header[1].split("(")[-1].split(")")[0])
                metadata["headers"][-1]["data_type"] = {
                    "type": "int",
                    "min_value": max_value,
                    "max_value": max_value
                }
                continue

            if re.match(r"char\([0-9]+\)", header[1]):
                max_value = int(header[1].split("(")[-1].split(")")[0])
                metadata["headers"][-1]["data_type"] = {
                    "type": "str",
                    "min_value": max_value,
                    "max_value": max_value
                }
                continue

            if re.match(r"date", header[1]):
                metadata["headers"][-1]["data_type"] = {
                    "type": "date",
                    "min_value": 10,
                    "max_value": 10,
                    "date_format": {
                        "day": [
                            0,
                            3
                        ],
                        "month": [
                            5,
                            6
                        ],
                        "year": [
                            8,
                            9
                        ],
                        "format": "yyyy-mm-dd"
                    },
                    "date_delimiter": "-",
                    "max_possible_date": "",
                    "min_possible_date": ""
                }

        metadata["headers_count"] = len(metadata["headers"])
        # print(self.metadata_c)
        self.metadata_c.metadata = metadata
        cursor.close()

    def filter(self, parm):
        pass
        # print(parm)

    def find(self, txt):
        matches = []
        txt = str.upper(str(txt))
        try:
            for index, value in enumerate(self.data):
                if txt in str.upper(str(value)):
                    matches.append(index)
            return matches
        except:
            pass
        finally:
            if len(matches) == 0:...
            ''' super(File, self).info(
                    f"We couldn’t find any data matching '{txt}' in folder '{self.path_c.get_folder()}'")'''
            # super(File, self).write_log(_LogDate.find, {"txt": txt})

    def change(self, row, col, value):

        data_row = self.data[row]
        headers = self.metadata_c.get_headers_names()

        sql = f"UPDATE `{self.path_c.path}` " \
              f"SET " \
              f"`{headers[col]}` = '{value}' " \
              f"WHERE "
        for index, header in enumerate(self.metadata_c.metadata["headers"]):
            if header["is_primary"]:
                sql += f"(`{header['name']}` = '{data_row[index]}')  AND "
                
        sql = sql[:-4]
        sql += ";"
        cursor = None
        onn = None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()

            cursor.execute(sql)
            conn.commit()

            return True, None
        except mysql.connector.Error as err:
            contains_in_self = False
            have_child = True
            if err.errno == errorcode.ER_DUP_ENTRY:
                contains_in_self = True

            if err.errno == errorcode.ER_ROW_IS_REFERENCED_2:
                have_child = False

            err_code = ''
            desc = f"You can't change object: \n\n{data_row} \n "

            if not have_child:
                err_code += "1fcohc"
                desc += f"!! Can't change object that is referenced in another table - error code : 1fcohc\n"

            if contains_in_self:
                err_code += ", 1fcnax"
                desc += "!! Object with entered index already exist - error code : 1fcnax\n"

            Error("Failed",
                  "You can not change this object",
                  desc,
                  err_code)

            return False, data_row[col]
        finally:
            if cursor is not None:
                cursor.close()

    def delete(self, index):
        data_row = self.data[index]
        headers = self.metadata_c.get_headers_names()

        sql = f"DELETE FROM `{self.path_c.path}` " \
              f"WHERE "
        for index, header in enumerate(self.metadata_c.metadata["headers"]):
            if header["is_primary"]:
                sql += f"(`{header['name']}` = '{data_row[index]}')  AND "

        sql = sql[:-4]
        sql += ";"
        cursor = None
        conn = None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()

            cursor.execute(sql)
            conn.commit()

            self.data.pop(index)
            Success("Successfully deleted",
                    "You successfully deleted object",
                    "",
                    f"You successfully deleted object : \n\n {data_row}\n"
                    f"from table '{self.path_c.path}'\n")
            return True
        except mysql.connector.Error as err:
            # print(err)
            Error("Failed",
                  "You can not delete this object",
                  f"!! Can't delete object that is referenced in another table - error code : 1fcohc\n",
                  "1fdohc")

            return False
        finally:
            if cursor is not None:
                cursor.close()

    def add(self, data):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        # {'Ustanova': '1c', 'nivo': '14', 'Oznaka programa': 'ddd', 'Naziv programa': 'an'}
        header_names = self.metadata_c.get_headers_names()
        str_arr = ""
        for header in header_names:
            str_arr += f"'{data[header]}',"
        if str_arr != "":
            str_arr = str_arr[:-1]

        try:
            cursor.callproc('addNewRecord', [self.path_c.path, str_arr])
            conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            contains_in_self = False
            have_parent = True
            # print(err.errno)
            if err.errno == errorcode.ER_DUP_ENTRY:
                contains_in_self = True

            if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                have_parent = False

            err_code = ''
            desc = f"You can't add object: \n\n{format_dict(data)} \n "

            # print(have_parent, contains_in_self)
            if not have_parent:
                err_code += "1fanonp"
                desc += f"!! Parent Index invalid - error code : 1fanonp\n"

            if contains_in_self:
                err_code += ", 1fanax"
                desc += "!! Object with entered index already exist - error code : 1fanax\n"

            Error("Failed",
                  "You can not add this object",
                  desc,
                  err_code)

            return False, (have_parent, contains_in_self)
        finally:
            if cursor is not None:
                cursor.close()

        self.data.append(list(data.values()))

        Success("New",
                "You successfully added new object",
                "",
                f"You successfully added object : \n\n {format_dict(data)}\n"
                f"in Table '{self.path_c.path}'\n")
        return True, None

    def split(self, arr, file_path=None):
        pass

    def possible_split(self):
        pass

    def split_by(self, parm):
        pass

    def merge(self, arr):
        pass

    def set_table_row(self, table, row):
        row_objet = self.data[row]
        headers = self.metadata_c.get_headers_names()

        for col in range(self.get_column_count()):
            value = row_objet[col]
            table.change_flag = True
            table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    def get_file_name(self):
        return self.path_c.get_file_name()

    def get_common_values(self, header):
        header_index = self.metadata_c.get_header_position_by_name(header)
        _list = (list(map(lambda data: data[header_index], self.data)))
        arr2 = []
        for item in _list:
            if item in arr2:
                continue
            arr2.append(item)
        if len(arr2) > 4:
            arr2 = arr2[:4]
        return arr2

    def get_min(self, header_name):
        if len(self.data) <= 0:
            return False

        header_index = self.metadata_c.get_header_position_by_name(header_name)

        min_v = self.data[0][header_index]

        for row in self.data:
            if row[header_index] < min_v:
                min_v = row[header_index]

        return int(min_v)

    def get_max(self, header_name):
        if len(self.data) <= 0:
            return False
        header_index = self.metadata_c.get_header_position_by_name(header_name)
        max_v = self.data[0][header_index]

        for row in self.data:
            if row[header_index] > max_v:
                max_v = row[header_index]

        return int(max_v)

    def filter(self, parm):
        matches = []

        for index, data_row in enumerate(self.data):
            def check():
                for condition in parm:
                    if condition is None:
                        continue
                    if condition["exact"]:
                        if condition["value"] != data_row[condition["header_meta"]["index"]]:
                            return
                        else:
                            continue

                    if not condition["value"] in data_row[condition["header_meta"]["index"]]:
                        return

                    if condition["header_meta"]["meta"]["data_type"]["type"] == "str":
                        continue

                    if int(condition["value_additional_info"]["min_value"]) > int(data_row[condition["header_name"]]) or \
                            int(condition["value_additional_info"]["max_value"]) < int(
                        data_row[condition["header_name"]]):
                        return

                matches.append(index)

            check()

        return matches

    def export_as_csv(self):
        super(MYSQLFile, self).split([], None)

    def _split_file(self, arr, file_path):
        new_file_full_path = Path(str(file_path))

        new_file_metadata = MetaData(new_file_full_path.get_metadata_path(),
                                     new_file_full_path.path,
                                     False)
        new_file_metadata.metadata = self.metadata_c.metadata.copy()
        new_file_metadata.metadata["sequential_info"] = {
            "is_sequential": False,
            "child_relation": [],
            "parent_relation": [],
            "bridge_relation": []}
        new_file_metadata.metadata["dialect"] = {
            "skip_first_line": False,
            "delimiter": ",",
            "quoting": 0
            }

        new_file = File(new_file_full_path, False, new_file_metadata)

        headers = new_file_metadata.get_headers_names()
        csv_object = {}
        # print(headers)
        for header in headers:
            csv_object.update({header: ""})

        for row in self.data:
            csv_object_blanc = csv_object.copy()
            for index, value in enumerate(row):
                csv_object_blanc[headers[index]] = value

            new_file.data.append(csv_object_blanc)

        new_file.save()
        new_file.metadata_c.save()

        self.structure_dock.file_system.refresh()

