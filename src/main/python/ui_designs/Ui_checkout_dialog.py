# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jackson/Documents/projectempire/src/main/python/ui_designs/checkout_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_checkout_dialog(object):
    def setupUi(self, checkout_dialog):
        checkout_dialog.setObjectName("checkout_dialog")
        checkout_dialog.resize(400, 123)
        self.verticalLayout = QtWidgets.QVBoxLayout(checkout_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(checkout_dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.buttonBox = QtWidgets.QDialogButtonBox(checkout_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(checkout_dialog)
        self.buttonBox.accepted.connect(checkout_dialog.accept)
        self.buttonBox.rejected.connect(checkout_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(checkout_dialog)

    def retranslateUi(self, checkout_dialog):
        _translate = QtCore.QCoreApplication.translate
        checkout_dialog.setWindowTitle(_translate("checkout_dialog", "Dialog"))
        self.label.setText(_translate("checkout_dialog", "Are you sure you want to perform this transaction?"))
