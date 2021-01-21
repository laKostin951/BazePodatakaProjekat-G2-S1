import sys

from PySide2 import QtWidgets

from component.main_window import MainWindow

WIDTH = 1920
HEIGHT = 1080


def main():
    app = QtWidgets.QApplication(sys.argv)

    screen_resolution = app.desktop().screenGeometry()
    global WIDTH
    global HEIGHT
    WIDTH = screen_resolution.width(), screen_resolution.height()

    mainwindow = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
