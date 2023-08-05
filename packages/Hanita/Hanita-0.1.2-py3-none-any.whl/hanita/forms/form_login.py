# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_forms/login_form02.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 465)
        Dialog.setMinimumSize(QtCore.QSize(300, 465))
        Dialog.setMaximumSize(QtCore.QSize(300, 465))
        Dialog.setStyleSheet("QDialog {\n"
"    background-color: #fff;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid #66BB6A;\n"
"    border-radius: 4px;\n"
"    padding-left: 5px;\n"
"    selection-color: blue;\n"
"}\n"
"\n"
"QLineEdit[echoMode=\"2\"] {\n"
"    lineedit-password-character: 9679;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #66bb6a;\n"
"}")
        self.le_login_input = QtWidgets.QLineEdit(Dialog)
        self.le_login_input.setGeometry(QtCore.QRect(50, 240, 200, 29))
        self.le_login_input.setObjectName("le_login_input")
        self.le_login_pass = QtWidgets.QLineEdit(Dialog)
        self.le_login_pass.setGeometry(QtCore.QRect(50, 280, 200, 29))
        self.le_login_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_login_pass.setObjectName("le_login_pass")
        self.pb_login_submit = QtWidgets.QPushButton(Dialog)
        self.pb_login_submit.setGeometry(QtCore.QRect(50, 340, 200, 30))
        self.pb_login_submit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pb_login_submit.setStyleSheet("QPushButton {\n"
"    background-color: #66BB6A;\n"
"    border: 1px solid #66BB6A;\n"
"    border-radius: 4px;\n"
"    color: #fafafa;\n"
"\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #81C784;\n"
"}\n"
"QPushButton:focus {\n"
"    outline: 1px dotted white;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4CAF50;\n"
"}")
        self.pb_login_submit.setObjectName("pb_login_submit")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(-10, -40, 321, 211))
        self.frame.setStyleSheet("QFrame {\n"
"    background-color: #66BB6A;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.l_login_greet = QtWidgets.QLabel(self.frame)
        self.l_login_greet.setGeometry(QtCore.QRect(70, 80, 181, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.l_login_greet.setFont(font)
        self.l_login_greet.setStyleSheet("QLabel {\n"
"    color: #fafafa;\n"
"}")
        self.l_login_greet.setAlignment(QtCore.Qt.AlignCenter)
        self.l_login_greet.setWordWrap(True)
        self.l_login_greet.setObjectName("l_login_greet")
        self.l_login_error = QtWidgets.QLabel(Dialog)
        self.l_login_error.setGeometry(QtCore.QRect(20, 410, 261, 51))
        self.l_login_error.setStyleSheet("QLabel {\n"
"    color: red;\n"
"}")
        self.l_login_error.setText("")
        self.l_login_error.setTextFormat(QtCore.Qt.RichText)
        self.l_login_error.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.l_login_error.setWordWrap(True)
        self.l_login_error.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.l_login_error.setObjectName("l_login_error")
        self.l_login_register = QtWidgets.QLabel(Dialog)
        self.l_login_register.setGeometry(QtCore.QRect(50, 380, 201, 20))
        self.l_login_register.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.l_login_register.setStyleSheet("QLabel {\n"
"    color: #388E3C;\n"
"    text-decoration: underline;\n"
"}\n"
"QLabel:hover {\n"
"    color: #81C784;\n"
"    text-decoration: none;\n"
"}")
        self.l_login_register.setTextFormat(QtCore.Qt.RichText)
        self.l_login_register.setAlignment(QtCore.Qt.AlignCenter)
        self.l_login_register.setObjectName("l_login_register")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Hanita"))
        self.le_login_input.setPlaceholderText(_translate("Dialog", "Enter your login"))
        self.le_login_pass.setPlaceholderText(_translate("Dialog", "Enter your password"))
        self.pb_login_submit.setText(_translate("Dialog", "Submit"))
        self.l_login_greet.setText(_translate("Dialog", "Welcom to Hanita"))
        self.l_login_register.setText(_translate("Dialog", "Register"))

