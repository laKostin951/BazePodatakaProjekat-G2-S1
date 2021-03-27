from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QLineEdit, QPushButton, QCheckBox, QLabel, QTableWidget, \
    QTableWidgetItem, QFrame


class ExtraWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
    
     

        self.setWindowTitle("customer - Table")
        self.setWindowIcon(QtGui.QIcon("assets/img/icons8-edit-file-64.png"))
        
        self.resize(662, 438)
        self.save_talble_changes = QPushButton("Save table changes",self)
        self.save_talble_changes.setGeometry(390, 290, 251, 31)

        self.add_table_main = QPushButton("Add Column ",self)
        self.add_table_main.setGeometry(390, 260, 251, 28)
        #self.add_table_main.clicked.connect(self.add_column)
    

        self.delet_table_column = QPushButton("Delet table column",self)
        self.delet_table_column.setGeometry(390, 330, 251, 31)

        self.not_null_box = QCheckBox("Not Null",self)
        self.not_null_box.setGeometry(220, 330, 81, 61)

        self.colm_name_label = QLabel("Column Name:",self)
        self.colm_name_label.setGeometry(10, 250, 111, 41)
        
        self.table_name_label_2 = QLabel("Table Name",self)
        self.table_name_label_2.setGeometry(10, 10, 91, 21)

        self.comn_name_line_edit = QLineEdit(self)
        self.comn_name_line_edit.setGeometry(110, 260, 151, 22)
        
        self.data_type_label = QLabel("Data Type",self)
        self.data_type_label.setGeometry(10, 300, 61, 16)

        self.data_type_line_edit = QLineEdit(self)
        self.data_type_line_edit.setGeometry(110, 300, 151, 22)

        self.table_name_line_edit = QLineEdit(self)
        self.table_name_line_edit.setGeometry(110, 10, 391, 22)

        self.foreign_key_box = QCheckBox("Foreign Key",self)
        self.foreign_key_box.setGeometry(120, 330, 91, 61)

        self.primary_key_box = QCheckBox("Primary Key",self)
        self.primary_key_box.setGeometry(20, 330, 111, 61)
        
        self.table_widget = QTableWidget(self)

    

        if (self.table_widget.columnCount() < 6):
            self.table_widget.setColumnCount(6)


        __qtablewidgetitem = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(5, __qtablewidgetitem5)


        self.table_widget.setGeometry(0, 40, 661, 201)
        self.table_widget.setColumnWidth(2,85)
        self.table_widget.setColumnWidth(3,85)
        self.table_widget.setColumnWidth(4,85)

        self.frame = QFrame(self)
        self.frame.setGeometry(0, 390, 661, 51)
        self.frame.setStyleSheet(u"background-color: rgb(45,45,45);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.cancel_button = QPushButton("Cancel button",self.frame)
        self.cancel_button.setGeometry(550, 10, 111, 28)
        
        self.cancel_button.setStyleSheet(u"background-color: rgb(255,255,255);")
        self.add_table_button = QPushButton("Add table",self.frame)

        self.add_table_button.setGeometry(442, 10, 101, 28)
        self.add_table_button.setStyleSheet(u"background-color: rgb(255,255,255);")
        
    
        self.tables()
    

        self.show()

    def tables(self):
        '''
        self.setWindowTitle(QCoreApplication.translate("ExtraWindow", u"Dialog", None))
        self.save_talble_changes.setText(QCoreApplication.translate("ExtraWindow", u"Save Table Changes", None))
        self.add_table_main.setText(QCoreApplication.translate("ExtraWindow", u"Add Table", None))
        self.delet_table_column.setText(QCoreApplication.translate("ExtraWindow", u"Delete Table Column", None))
        self.not_null_box.setText(QCoreApplication.translate("ExtraWindow", u"Not null", None))
        self.colm_name_label.setText(QCoreApplication.translate("ExtraWindow", u"Colomn Name", None))
        self.table_name_label_2.setText(QCoreApplication.translate("ExtraWindow", u"Table Name", None))
        self.data_type_label.setText(QCoreApplication.translate("ExtraWindow", u"Data Type", None))
        self.foreign_key_box.setText(QCoreApplication.translate("ExtraWindow", u"Foreign key", None))
        self.primary_key_box.setText(QCoreApplication.translate("ExtraWindow", u"Primary key", None))
        '''
        ___qtablewidgetitem = self.table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ExtraWindow", u"Column Name", None))
        ___qtablewidgetitem1 = self.table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ExtraWindow", u"Data Type", None))
        ___qtablewidgetitem2 = self.table_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ExtraWindow", u"Primary key", None))
        ___qtablewidgetitem3 = self.table_widget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ExtraWindow", u"Foreign key", None))
        ___qtablewidgetitem4 = self.table_widget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ExtraWindow", u"Not Null", None))
        ___qtablewidgetitem5 = self.table_widget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ExtraWindow", u"Default", None))


        '''
        self.cancel_button.setText(QCoreApplication.translate("ExtraWindow", u"Cancel", None))
        self.add_table_button.setText(QCoreApplication.translate("ExtraWindow", u"Add table", None))
        '''
        