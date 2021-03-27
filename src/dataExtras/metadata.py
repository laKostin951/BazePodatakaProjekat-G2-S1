import csv
import json

import os

METADATA_EXTRA_NAME = "_metadata.json"


class MetaData:
    def __init__(self, metadata_path, data_path_c, auto_generate=True):
        self.metadata_path = metadata_path
        self._data_path_c = data_path_c
        if auto_generate:
            self.metadata = self.get_metadata()
        else:
            self.metadata = None

    def get_metadata(self):
        try:
            metadata_file = open(self.metadata_path,
                                 'r')  # otvarmo metadata file ako ne postoji detaljnije dole u "except"
            metadata = json.load(metadata_file)  # parsiaramo metadata file u object
            metadata_file.close()
            return metadata
        except IOError:
            blank_metadata = self._make_blank_metadata()  # u open funkciji kreira se prazna fajl na zadatom pathu
            try:
                return blank_metadata
            finally:

                metadata_file = open(self.metadata_path, 'w')
                json.dump(blank_metadata, metadata_file)
                metadata_file.close()

    def get_headers_names(self):
        return list(map(lambda header: header["name"], self.metadata["headers"]))

    def get_header_meta(self, header_name):
        for index, header in enumerate(self.metadata["headers"]):
            if header["name"] == header_name:
                return index, header
        return None

    def get_header_position_by_name(self, col_name):
        for pos, header in enumerate(self.metadata["headers"]):
            if header["name"] == col_name:
                return pos

    def save(self):
        try:
            metadata_file = open(self.metadata_path, 'w')
            json.dump(self.metadata, metadata_file)
            metadata_file.close()
        finally:
            pass

    def delete(self):
        os.remove(self.metadata_path)

    def _make_blank_metadata(self):
        dialect = self._get_dialect()
        headers = self._get_data_headers(dialect)

        # TODO: ako je dialect.delimiter = ''( nije nadjen ) ne otvoriti file ili ga otvoriti kao txt

        return {
            'is_sequential': False,
            'headers': headers,
            'skip_first_line': (True if headers[0] != 'Column 1' else False),
            'header_name': [],
            'delimiter': dialect.delimiter,
            'quoting': dialect.quoting,
            'headers_count': len(headers)
        }

        #   Ako prvi elemetn nije "Column 1" znaci
        # nasao je nazive kolona i treba preskocit prvi red(header line)
        # u suprotnom nije nasao nazive kolona i treba prikzati prvi red
        #   Postoji moguce da je doslo do greske da u fajlu postoje
        # nazivi kolona(U prvom redu) ali ih program nije pronaoso,
        # ali rezultat te greske ce biti samo
        # prkzaivanje naziva kolona kao 1. reda u tabeli

    def _get_dialect(self):
        data_file = None
        try:
            data_file = open(self._data_path_c.path, 'r')
            return csv.Sniffer().sniff(data_file.read(2048))  # sinifer pravi dialect
        except:
            # TODO: error slucaj ako dataExtras file ne postoji
            pass
        finally:
            if data_file is not None:
                data_file.close()

    def _get_data_headers(self, dialect):
        data_file = open(self._data_path_c.path, 'r')
        buffer = data_file.read(2048)  # citamo prvih 2048

        possible_header_arr = list(filter(None, buffer.split('\n')))
        # delimo file po novom redu,
        # possible_header_arr sada izgleda ["",
        #                                   ""Broj Indeksa" ,"Ime i prezime"",
        #                                   "",
        #                                   ""20606903", "Marko Markovic"", .....]
        # do praznoh elemenata moze doci ako fajl sadrzi prazna polja
        # zata iz niza izbacujemo prazne redove, odnosno prazne strignove
        # pomocu funkcije list(filter(None, arr)
        possible_header_arr = possible_header_arr[0].split(dialect.delimiter)
        # possible_header_arr sada izgleda [""Broj Indeksa"",""Ime i prezime""]

        possible_header_arr = [header_name.strip('\"') for header_name in possible_header_arr]
        # prolazimo for petljom kroz 'possible_header_arr' i za
        # brisemo dodatne znake navodnika odnosno ako je csv fajl upian sa nekim dodatnim "quoting"

        default_header = []

        for i in range(0, len(possible_header_arr)):
            default_header.append(
                "Column " + str(i + 1))  # pravimo default_header da bude ["Kolona 1", "Kolona 2" .... ]

        for header_name in possible_header_arr:
            if header_name.isdigit():  # proveravamo da li je 'pure digit' jer ime kolone ne moze da bude samo broj
                return default_header
            if type(header_name) == bool:  # proveravamo da li je "bolean" jer ime kolone ne moze da bude "boolean"
                return default_header

        data_file.seek(0)
        data_file.close()
        return possible_header_arr
