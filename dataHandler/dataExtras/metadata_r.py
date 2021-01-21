import json


# file sa podacima : "student_data.csv"
# file sa metaData : "student_data_metadata.json"


def _make_blank_metadata():
    return {
        "headers": [],
        "header_name": [],
        "headers_count": 0,
        "dialect": {
            "skip_first_line": False,
            "delimiter": ",",
            "quoting": 0
        },
        "sequential_info": {
            "is_sequential": False,
            "child_relation": [
            ],
            "parent_relation": [
            ],
            "bridge_relation": []
        }
    }

    #   Ako prvi elemetn nije "Column 1" znaci
    # nasao je nazive kolona i treba preskocit prvi red(header line)
    # u suprotnom nije nasao nazive kolona i treba prikzati prvi red
    #   Postoji moguce da je doslo do greske da u fajlu postoje
    # nazivi kolona(U prvom redu) ali ih program nije pronaoso,
    # ali rezultat te greske ce biti samo
    # prkzaivanje naziva kolona kao 1. reda u tabeli


class MetaData:
    def __init__(self, metadata_path):
        self.metadata_path = metadata_path
        self.metadata = self.get_metadata()

    def get_metadata(self):
        try:
            metadata_file = open(self.metadata_path, 'r')  # otvarmo metadata file ako ne postoji detaljnije dole u "except"
            metadata = json.load(metadata_file)            # parsiaramo metadata file u object
            metadata_file.close()
            return metadata
        except IOError:
            blank_metadata = _make_blank_metadata()  # u open funkciji kreira se prazna fajl na zadatom pathu
            try:
                return blank_metadata
            finally:

                metadata_file = open(self.metadata_path, 'w')
                json.dump(blank_metadata, metadata_file)
                metadata_file.close()

    def save(self):
        try:
            metadata_file = open(self.metadata_path, 'w')
            json.dump(self.metadata, metadata_file)
            metadata_file.close()
        finally:
            metadata_file.close()


