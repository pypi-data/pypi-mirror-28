# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_forms/contacts.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_contacts(object):
    def setupUi(self, dialog_contacts):
        dialog_contacts.setObjectName("dialog_contacts")
        dialog_contacts.resize(364, 575)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(dialog_contacts)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_add_input = QtWidgets.QLineEdit(dialog_contacts)
        self.le_add_input.setObjectName("le_add_input")
        self.horizontalLayout.addWidget(self.le_add_input)
        self.pb_add_contact = QtWidgets.QPushButton(dialog_contacts)
        self.pb_add_contact.setObjectName("pb_add_contact")
        self.horizontalLayout.addWidget(self.pb_add_contact)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.l_contacts = QtWidgets.QLabel(dialog_contacts)
        self.l_contacts.setObjectName("l_contacts")
        self.verticalLayout.addWidget(self.l_contacts)
        self.lw_contacts = QtWidgets.QListWidget(dialog_contacts)
        self.lw_contacts.setObjectName("lw_contacts")
        self.verticalLayout.addWidget(self.lw_contacts)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(dialog_contacts)
        QtCore.QMetaObject.connectSlotsByName(dialog_contacts)

    def retranslateUi(self, dialog_contacts):
        _translate = QtCore.QCoreApplication.translate
        dialog_contacts.setWindowTitle(_translate("dialog_contacts", "Contacts"))
        self.le_add_input.setPlaceholderText(_translate("dialog_contacts", "Enter name"))
        self.pb_add_contact.setText(_translate("dialog_contacts", "Add"))
        self.l_contacts.setText(_translate("dialog_contacts", "Contacts:"))
        self.lw_contacts.setSortingEnabled(True)

