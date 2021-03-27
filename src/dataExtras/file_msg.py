class _FileMsg:
    def __init__(self, file):
        self.file = file

    def delete(self, success, data):
        if success:
            return f'You successfully deleted "{self.file.metadata_c.metadata["object_name"]}" :' \
                   f' {list(data.values())}'
        return f'You can not delete "{self.file.metadata_c.metadata["object_name"]}" :' \
               f' {list(data.values())}'

