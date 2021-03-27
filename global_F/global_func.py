import os

from PySide2 import QtWidgets
from PySide2.QtCore import QDir


def create_dir(dir_path, n, org_dir):
    dir_path.replace(",", "").replace(" ", "")
    try:
        os.mkdir(dir_path)
        return dir_path
    except FileExistsError:
        return create_dir(org_dir + str(n), n + 1, org_dir)


def SelectFolder(title, name_filter, default_suffix):
    dialog = QtWidgets.QFileDialog()
    dialog.setWindowTitle(title)
    dialog.setNameFilter(name_filter)
    dialog.setDefaultSuffix(default_suffix)
    dialog.setDirectory(QDir.currentPath())
    dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
    return dialog


def SelectFiles(title, name_filter):
    dialog = QtWidgets.QFileDialog()
    dialog.setWindowTitle(title)
    dialog.setNameFilter(name_filter)
    dialog.setDirectory(QDir.currentPath())
    dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
    return dialog


def format_dict(item):
    s = ''
    keys = item.keys()
    values = item.values()

    for key, value in zip(keys, values):
        s += f" {key} : {value}\n"

    return s