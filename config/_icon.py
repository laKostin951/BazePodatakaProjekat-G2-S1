import os


class _Icon:
    def __init__(self, config):
        self.config = config.get_icon_config()
        self.path = f"assets{os.path.sep}img{os.path.sep}{self.config['icon_source']}{os.path.sep}{self.config['icon_collection']}{os.path.sep}"

    def SAVE_I(self):
        return f"{self.path}icons8-save-32.png"

    def SAVE_ALL_I(self):
        return f"{self.path}icons8-save-all-32.png"

    def SAVE_AS_I(self):
        return f"{self.path}icons8-save-as-32.png"

    def SAVE_CLOSE_I(self):
        return f"{self.path}icons8-save-close-32.png"

    def ADD_FILE_I(self):
        return f"{self.path}icons8-add-file-32.png"

    def CLOUD_CHECKED_I(self):
        return f"{self.path}icons8-cloud-checked-32.png"

    def COPY_I(self):
        return f"{self.path}icons8-copy-32.png"

    def PASTE_I(self):
        return f"{self.path}icons8-paste-32.png"

    def CUT_I(self):
        return f"{self.path}icons8-cut-32.png"

    def SEARCH_MORE_I(self):
        return f"{self.path}icons8-search-more-32.png"

    def UNDO_I(self):
        return f"{self.path}icons8-undo-32.png"

    def REDO_I(self):
        return f"{self.path}icons8-redo-32.png"

    def PRINT_I(self):
        return f"{self.path}icons8-print-32.png"

    def DAY_NIGHT_I(self):
        return f"{self.path}icons8-day-and-night-32.png"

    def DOWN_BUTTON_I(self):
        return f"{self.path}icons8-down-button-32.png"

    def DOWN_ARROW_I(self):
        return f"{self.path}icons8-down-arrow-32.png"

    def UP_ARROW_I(self):
        return f"{self.path}icons8-up-arrow-32.png"

    def EDIT_I(self):
        return f"{self.path}icons8-edit-32.png"

    def EDIT_FILE_I(self):
        return f"{self.path}icons8-edit-file-32.png"

    def FILTER_I(self):
        return f"{self.path}icons8-filter-32.png"

    def FOLDER_I(self):
        return f"{self.path}icons8-folder-32.png"

    def PLUS_MATH_I(self):
        return f"{self.path}icons8-plus-math-32.png"

    def SHUTDOWN_I(self):
        return f"{self.path}icons8-shutdown-32.png"

    def SLIDE_UP(self):
        return f"{self.path}icons8-slide-up-32.png"

    def SPLIT_I(self):
        return f"{self.path}icons8-split-32.png"

    def MERGE_I(self):
        return f"{self.path}icons8-merge-32.png"

    def UPDATE_I(self):
        return f"{self.path}icons8-update-32.png"

    def CHECKMARK_I(self):
        return f"{self.path}icons8-checkmark-32.png"

    def DELETE_I(self):
        return f"{self.path}icons8-delete-32.png"

    def UNAVAILABLE_I(self):
        return f"{self.path}icons8-unavailable-32.png"

    def DOUBLE_DOWN(self):
        return f"{self.path}icons8-double-down-32.png"

    def DOUBLE_UP(self):
        return f"{self.path}icons8-double-up-32.png"

    def HOME_SCREEN_I(self):
        return f"{self.path}icons8-home-screen-32.png"

    def MULTICAST_I(self):
        return f"{self.path}icons8-multicast-32.png"

    def SEARCH_I(self):
        return f"{self.path}icons8-search-32.png"

    def RESET_I(self):
        return f"{self.path}icons8-reset-32.png"

    def OPENED_FOLDER_I(self):
        return f"{self.path}icons8-opened-folder-32.png"

    def MULTICAST_I(self):
        return f"{self.path}icons8-multicast-32.png"

    def TABLE_I(self):
        return f"{self.path}icons8-table-32.png"

    def RELATION_TABLE_I(self):
        return f"{self.path}icons8-relation-table-32.png"

    def EXPORT_CSV_I(self):
        return f"{self.path}icons8-export-csv-32.png"
