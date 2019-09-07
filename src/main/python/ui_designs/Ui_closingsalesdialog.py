# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jackson/Documents/projectempire/src/main/python/ui_designs/closingsalesdialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 124)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.to_datetime_edit = QtWidgets.QDateTimeEdit(Dialog)
        self.to_datetime_edit.setCalendarPopup(True)
        self.to_datetime_edit.setObjectName("to_datetime_edit")
        self.gridLayout.addWidget(self.to_datetime_edit, 3, 1, 1, 1, QtCore.Qt.AlignTop)
        self.from_datetime_edit = QtWidgets.QDateTimeEdit(Dialog)
        self.from_datetime_edit.setCurrentSection(QtWidgets.QDateTimeEdit.YearSection)
        self.from_datetime_edit.setCalendarPopup(True)
        self.from_datetime_edit.setObjectName("from_datetime_edit")
        self.gridLayout.addWidget(self.from_datetime_edit, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.to_datetime_edit)
        self.label.setBuddy(self.from_datetime_edit)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.to_datetime_edit.setDisplayFormat(_translate("Dialog", "yyyy-mm-dd h:mm AP"))
        self.from_datetime_edit.setDisplayFormat(_translate("Dialog", "yyyy:mm:dd h:mm AP"))
        self.label_2.setText(_translate("Dialog", "&To"))
        self.label.setText(_translate("Dialog", "&From"))
