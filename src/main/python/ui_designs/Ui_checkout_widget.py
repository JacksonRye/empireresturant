# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/jackson/Documents/projectempire/src/main/python/ui_designs/checkout_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_checkout_frame(object):
    def setupUi(self, checkout_frame):
        checkout_frame.setObjectName("checkout_frame")
        checkout_frame.resize(443, 69)
        checkout_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        checkout_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(checkout_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.no_label = QtWidgets.QLabel(checkout_frame)
        self.no_label.setText("")
        self.no_label.setObjectName("no_label")
        self.horizontalLayout.addWidget(self.no_label)
        self.name_label = QtWidgets.QLabel(checkout_frame)
        self.name_label.setText("")
        self.name_label.setObjectName("name_label")
        self.horizontalLayout.addWidget(self.name_label)
        self.price_label = QtWidgets.QLabel(checkout_frame)
        self.price_label.setText("")
        self.price_label.setObjectName("price_label")
        self.horizontalLayout.addWidget(self.price_label)
        self.quantity_widget = QtWidgets.QWidget(checkout_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantity_widget.sizePolicy().hasHeightForWidth())
        self.quantity_widget.setSizePolicy(sizePolicy)
        self.quantity_widget.setMaximumSize(QtCore.QSize(314, 16777215))
        self.quantity_widget.setObjectName("quantity_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.quantity_widget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_qty_btn = QtWidgets.QPushButton(self.quantity_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_qty_btn.sizePolicy().hasHeightForWidth())
        self.add_qty_btn.setSizePolicy(sizePolicy)
        self.add_qty_btn.setMaximumSize(QtCore.QSize(85, 27))
        self.add_qty_btn.setObjectName("add_qty_btn")
        self.horizontalLayout_2.addWidget(self.add_qty_btn, 0, QtCore.Qt.AlignLeft)
        self.qty_line_edit = QtWidgets.QLineEdit(self.quantity_widget)
        self.qty_line_edit.setReadOnly(True)
        self.qty_line_edit.setObjectName("qty_line_edit")
        self.horizontalLayout_2.addWidget(self.qty_line_edit)
        self.sub_qty_btn = QtWidgets.QPushButton(self.quantity_widget)
        self.sub_qty_btn.setObjectName("sub_qty_btn")
        self.horizontalLayout_2.addWidget(self.sub_qty_btn, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.quantity_widget, 0, QtCore.Qt.AlignHCenter)
        self.subtotal_label = QtWidgets.QLabel(checkout_frame)
        self.subtotal_label.setText("")
        self.subtotal_label.setObjectName("subtotal_label")
        self.horizontalLayout.addWidget(self.subtotal_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(checkout_frame)
        QtCore.QMetaObject.connectSlotsByName(checkout_frame)

    def retranslateUi(self, checkout_frame):
        _translate = QtCore.QCoreApplication.translate
        checkout_frame.setWindowTitle(_translate("checkout_frame", "Frame"))
        self.add_qty_btn.setText(_translate("checkout_frame", "+"))
        self.sub_qty_btn.setText(_translate("checkout_frame", "-"))
