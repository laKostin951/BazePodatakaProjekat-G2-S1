import sys

from PySide2 import QtWidgets

from assets.config import icon
from assets.style import styles
from ui.pages.main_window import MainWindow

WIDTH = 1920
HEIGHT = 1080


def main():
    app = QtWidgets.QApplication(sys.argv)

    screen_resolution = app.desktop().screenGeometry()
    global WIDTH
    global HEIGHT
    WIDTH = screen_resolution.width(), screen_resolution.height()

    mainwindow = MainWindow()
    app.setStyleSheet("QCheckBox::indicator {"
                      " border : none;}"
                      "QCheckBox::indicator:checked {"
                      f"image: url({icon.CHECKMARK_I()});"
                      "width:16px;"
                      "height:16px;"
                      "}"
                      "QCheckBox::indicator:unchecked {"
                      f"image: url({icon.DELETE_I()});"
                      "width:16px;"
                      "height:16px;"
                      "}"
                      )
    mainwindow.setStyleSheet(styles.main_dark_QWidget)

    '''mainwindow.setStyleSheet(
        " background-color: rgb(0,17,26);"
        " color: white ;"
    )'''

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
