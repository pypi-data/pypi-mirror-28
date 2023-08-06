# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_forms/new_chat.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog_new_chat(object):
    def setupUi(self, dialog_new_chat):
        dialog_new_chat.setObjectName("dialog_new_chat")
        dialog_new_chat.resize(336, 538)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog_new_chat.sizePolicy().hasHeightForWidth())
        dialog_new_chat.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(dialog_new_chat)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_chat_name = QtWidgets.QLineEdit(dialog_new_chat)
        self.le_chat_name.setObjectName("le_chat_name")
        self.horizontalLayout.addWidget(self.le_chat_name)
        self.pb_chat_create = QtWidgets.QPushButton(dialog_new_chat)
        self.pb_chat_create.setObjectName("pb_chat_create")
        self.horizontalLayout.addWidget(self.pb_chat_create)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(dialog_new_chat)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lw_chat_contacts = QtWidgets.QListWidget(dialog_new_chat)
        self.lw_chat_contacts.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lw_chat_contacts.setObjectName("lw_chat_contacts")
        self.verticalLayout.addWidget(self.lw_chat_contacts)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(dialog_new_chat)
        QtCore.QMetaObject.connectSlotsByName(dialog_new_chat)

    def retranslateUi(self, dialog_new_chat):
        _translate = QtCore.QCoreApplication.translate
        dialog_new_chat.setWindowTitle(_translate("dialog_new_chat", "New Chat"))
        self.le_chat_name.setPlaceholderText(_translate("dialog_new_chat", "Name of chat"))
        self.pb_chat_create.setText(_translate("dialog_new_chat", "Create"))
        self.label.setText(_translate("dialog_new_chat", "Select users:"))
        self.lw_chat_contacts.setSortingEnabled(True)

