from abc import ABC
from concurrent.futures._base import as_completed
from concurrent.futures.process import ProcessPoolExecutor

from component.popup import Error, Info, Success
from dataHandler.dataExtras.file import File
from dataHandler.dataExtras.path import Path
from dataHandler.nesto.func import format_dict


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


class SQFile(File, ABC):
    def __init__(self, path_c, auto_load=False, metadata_c=None):  # path_c = Path 'Class'(path of file
        super().__init__(path_c, auto_load, metadata_c)

    def change(self, row, col, value):
        try:
            data_row = self.data[row]
            data = self.data[row].copy()
            header = self.metadata_c.metadata['headers'][col]

            data[header["name"]] = value

            if not self._check_input(row, col, value, data_row, header):
                return False, data_row[header["name"]]
            if header["is_primary"] or header["is_foreign_key"]:
                if self._sf_filter(self._self_relation_to_self(data)):
                    # print("Sadrzi se u sebi")
                    Info("Unsuccessful changes",
                         "Failed to change object",
                         "",
                         "You cannot change the index of this object because new entered index already exist")
                    return False, data_row[header["name"]]
                if self.sf_have_relative_data(data_row):
                    # print("Ima child podatke")
                    Info("Unsuccessful changes",
                         "Failed to change object",
                         "",
                         "You cannot change the index of this object because object have child data")
                    return False, data_row[header["name"]]
                if not self.have_valid_relative_data(data, "parent_relation"):
                    # print("Nema validnog roditeja")
                    Info("Unsuccessful changes",
                         "Failed to change object",
                         "",
                         "You cannot change the index of this object because parent object index is invalid")
                    return False, data_row[header["name"]]

            Success("Successfully changed",
                    "You successfully changed object",
                    "",
                    f"You successfully changed object : \n\n {format_dict(data)}\n"
                    f"from file '{self.path_c.path}'\n"
                    f"* Changes will not have effect until you save file")
            data_row[header["name"]] = value
            return True, None
        except:
            return False, data_row[header["name"]]
        finally:
            ...
            # TODO: LOG
            '''super(File, self).write_log(_LogDate.change, {
                    "row": row,
                    "col": col,
                    "value": value
                })
                self.changes.add()'''

    def delete(self, index):
        try:
            data = self.data[index]
            if not self.have_child_data(index):
                self.data.remove(data)
                Success("Successfully deleted",
                        "You successfully deleted object",
                        "",
                        f"You successfully deleted object : \n\n {format_dict(data)}\n"
                        f"from file '{self.path_c.path}'\n"
                        f"* Changes will not have effect until you save file")
                return True
            Error("Failed",
                  "You can not delete this object",
                  "1fdhc",
                  f"You can not delete \n\n{format_dict(data)} \n "
                  f"Object have child data")
            return False
        except:
            print("Error")
        finally:
            ...
        # TODO: LOG napisati log sa podacima akcije

    def add(self, data):
        have_parent, contains_is_self = self._is_adding_possible(data)

        if have_parent and not contains_is_self:
            self.data.append(data)
            Success("New",
                    "You successfully added new object",
                    "",
                    f"You successfully added object : \n\n {format_dict(data)}\n"
                    f"in file '{self.path_c.path}'\n"
                    f"* Changes will not have effect until you save file")
            return True, (have_parent, contains_is_self)

        err_code = ''
        desc = f"You can't add object: \n\n{format_dict(data)} \n "

        if not have_parent:
            err_code += "1fanonp"
            desc += "!! Parent Index \n"

        if contains_is_self:
            err_code += ", 1fanax"
            desc += "!! Object with entered index already exist \n"

        Error("Failed",
              "You can not add this object",
              err_code,
              desc)
        return False, (have_parent, contains_is_self)

    def _is_adding_possible(self, data):
        have_parent = True if len(self.metadata_c.metadata["sequential_info"]["parent_relation"]) == 0 \
            else self.have_valid_relative_data(data, "parent_relation")
        contains_is_self = self._sf_filter(self._self_relation_to_self(data))
        # print(f"have_valid_parent(True): {have_parent} - contains_is_self(false): {contains_is_self}")
        return have_parent, contains_is_self

    def filter(self, parm):
        matches = []

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

                    if int(condition["value_additional_info"]["min_value"]) > int(data_row[condition["header_name"]]) or \
                            int(condition["value_additional_info"]["max_value"]) < int(
                        data_row[condition["header_name"]]):
                        return

                matches.append(index)

            check()

        return matches

    def have_child_data(self, row):
        with ProcessPoolExecutor() as executor:
            res = []
            for index, relation_meta in enumerate(self.metadata_c.metadata["sequential_info"]["child_relation"]):
                res.append(
                    executor.submit(self._search_file, relation_meta["path_of_child_table"], index, self.data[row]))

            for f in as_completed(res):
                if f.result():
                    return True

        return False

    def sf_have_relative_data(self, data, relative="child_relation"):
        with ProcessPoolExecutor() as executor:
            res = []
            for index, relation_meta in enumerate(self.metadata_c.metadata["sequential_info"][relative]):
                res.append(
                    executor.submit(self._search_file, relation_meta["path_of_child_table"], index, data, relative))

            for f in as_completed(res):
                print(f.result())
                if f.result():
                    return True

        return False

    def have_valid_relative_data(self, data, relative="child_relation"):
        with ProcessPoolExecutor() as executor:
            res = []
            for index, relation_meta in enumerate(self.metadata_c.metadata["sequential_info"][relative]):
                res.append(
                    executor.submit(self._search_file, relation_meta["path_of_child_table"], index, data, relative))

            for f in as_completed(res):
                if not f.result():
                    return False

        return True

    def _sf_filter(self, parm):
        ln = len(parm)
        # print(self.path_c.path)
        for data_row in self.data:
            match = 0
            for condition in parm:
                if condition["value"] != data_row[condition["header_name"]]:
                    # print(f' -{condition["header_name"]}- {condition["value"]} != {data_row[condition["header_name"]]} - match : {match}')
                    continue
                else:
                    match += 1
                    # print(f' -{condition["header_name"]}- {condition["value"]} == {data_row[condition["header_name"]]}- match : {match}')

                if match == ln:
                    # print("NASAO")
                    return True
        # print("NIJE NASAO")
        return False

    def _search_file(self, path, index, data, relative="child_relation"):
        file = SQFile(Path(path), True)
        return file._sf_filter(self.get_relation_point(index, data, relative))

    def _self_relation_to_self(self, data):
        headers = self.metadata_c.metadata['headers']

        parms = []
        for index, header in enumerate(headers):
            if header['is_primary']:
                parms.append({
                    "header_name": header["name"],
                    "value": data[header["name"]],
                    "exact": True,
                    "header_meta": {
                        "index": index,
                        "meta": header
                    },
                    "value_additional_info": {
                        "contains": False,
                        "min_value": "",
                        "max_value": ""
                    }
                })

        return parms

    def get_relation_point(self, index, data, relative="child_relation"):
        relation_meta = self.metadata_c.metadata["sequential_info"][relative][index]

        relations = []

        for relation in relation_meta["relation_on"]:
            _, meta = self.metadata_c.get_header_meta(relation["this_table_key"])
            relations.append({
                "header_name": relation["child_table_key"],
                "value": data[relation["this_table_key"]],
                "exact": True,
                "header_meta": {
                    "index": index,
                    "meta": meta
                },
                "value_additional_info": {
                    "contains": False,
                    "min_value": "",
                    "max_value": ""
                }
            })

        return relations
