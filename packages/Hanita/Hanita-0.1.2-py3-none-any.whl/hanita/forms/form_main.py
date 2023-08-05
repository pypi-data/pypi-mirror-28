# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_forms/login_form03.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(806, 650)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: #fff;\n"
"}\n"
"QScrollBar:vertical {\n"
"     border: none;\n"
"     background: #fff;\n"
"     width: 8px;\n"
"     margin: 0;\n"
" }\n"
" QScrollBar::handle:vertical {\n"
"    border: 1px solid #F3F4F5;\n"
"    border-radius: 4px;\n"
"     background: lightgrey;\n"
"     min-height: 20px;\n"
" }\n"
"QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"     background: #fff;\n"
"     height: 20px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::sub-line:vertical {\n"
"     border: none;\n"
"     background: #fff;\n"
"     height: 20px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" \n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"QSplitter::handle {\n"
"    background-color: #fff;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #66BB6A;\n"
"    border: 1px solid #66BB6A;\n"
"    border-radius: 4px;\n"
"    color: #fafafa;\n"
"    padding: 8px 24px;\n"
"\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #81C784;\n"
"}\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"    border: 1px solid #4caf50;\n"
"    text-decoration: underline;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4CAF50;\n"
"}\n"
"\n"
"QListWidget {\n"
"    border: none;\n"
"}\n"
"QListWidget QWidget {\n"
"    margin: 0;\n"
"    padding: 0;\n"
"}\n"
"\n"
"QListWidget QPushButton {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    margin: 0;\n"
"    padding: 3px;\n"
"    background-color: #fff;\n"
"    border: none;\n"
"    color: orange;\n"
"}\n"
"QListWidget QPushButton:hover {\n"
"    background-color: orange;\n"
"    color: white;\n"
"}\n"
"\n"
"QTextEdit {\n"
"        border: 1px solid #66BB6A;\n"
"    border-radius: 4px;\n"
"    padding-left: 5px;\n"
"}\n"
"QTextEdit:focus {\n"
"    border: 3px solid #66bb6a;\n"
"}\n"
"\n"
"QListView::item:alternate {\n"
"    background: #EEEEEE;\n"
"}\n"
"\n"
"QListView::item:selected {\n"
"    border: 1px solid #66BB6A;\n"
"    color: #000;\n"
"    font-weight: 800;\n"
"    background-color: #fff;\n"
"}\n"
"\n"
"QListView::item:selected:!active {\n"
"    border: 1px solid lightgrey;\n"
"}\n"
"\n"
"QListView::item:hover {\n"
"    border: 1px solid lightgrey;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid #66BB6A;\n"
"    border-radius: 4px;\n"
"    padding: 7px 5px;\n"
"}\n"
"\n"
"QLineEdit[echoMode=\"2\"] {\n"
"    lineedit-password-character: 9679;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #66bb6a;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_stack = QtWidgets.QStackedWidget(self.centralwidget)
        self.main_stack.setLineWidth(0)
        self.main_stack.setObjectName("main_stack")
        self.login_page = QtWidgets.QWidget()
        self.login_page.setObjectName("login_page")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.login_page)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame = QtWidgets.QFrame(self.login_page)
        self.frame.setStyleSheet("QFrame {\n"
"    background-color: #66bb6a;\n"
"    border: none;\n"
"    max-height: 200px;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.login_greet = QtWidgets.QLabel(self.frame)
        self.login_greet.setAlignment(QtCore.Qt.AlignCenter)
        self.login_greet.setWordWrap(True)
        self.login_greet.setObjectName("login_greet")
        self.verticalLayout_8.addWidget(self.login_greet)
        self.verticalLayout_5.addWidget(self.frame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.login_page)
        self.frame_2.setStyleSheet("QFrame {\n"
"    max-width: 270px;\n"
"    border: none;\n"
"    margin-top: 60px;\n"
"}\n"
"\n"
"QFrame#login_frame {\n"
"    margin-top: 0px;\n"
"    max-height: 150px;\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.login_frame = QtWidgets.QFrame(self.frame_2)
        self.login_frame.setObjectName("login_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.login_frame)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.le_login_input = QtWidgets.QLineEdit(self.login_frame)
        self.le_login_input.setObjectName("le_login_input")
        self.verticalLayout_6.addWidget(self.le_login_input)
        self.le_login_password = QtWidgets.QLineEdit(self.login_frame)
        self.le_login_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.le_login_password.setObjectName("le_login_password")
        self.verticalLayout_6.addWidget(self.le_login_password)
        self.pb_login_submit = QtWidgets.QPushButton(self.login_frame)
        self.pb_login_submit.setObjectName("pb_login_submit")
        self.verticalLayout_6.addWidget(self.pb_login_submit)
        self.verticalLayout_7.addWidget(self.login_frame)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setStyleSheet("QFrame {\n"
"    margin: 0;\n"
"    padding: 0;\n"
"}\n"
"\n"
"#login_error {\n"
"    color: red;\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.login_error = QtWidgets.QLabel(self.frame_3)
        self.login_error.setText("")
        self.login_error.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.login_error.setWordWrap(True)
        self.login_error.setObjectName("login_error")
        self.verticalLayout_9.addWidget(self.login_error)
        self.verticalLayout_7.addWidget(self.frame_3)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.main_stack.addWidget(self.login_page)
        self.main_page = QtWidgets.QWidget()
        self.main_page.setObjectName("main_page")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.main_page)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.splitter_2 = QtWidgets.QSplitter(self.main_page)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.splitter_2)
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lw_list_chats = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_list_chats.sizePolicy().hasHeightForWidth())
        self.lw_list_chats.setSizePolicy(sizePolicy)
        self.lw_list_chats.setMinimumSize(QtCore.QSize(200, 300))
        self.lw_list_chats.setMaximumSize(QtCore.QSize(300, 16777215))
        self.lw_list_chats.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lw_list_chats.setObjectName("lw_list_chats")
        item = QtWidgets.QListWidgetItem()
        self.lw_list_chats.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.lw_list_chats.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.lw_list_chats.addItem(item)
        self.verticalLayout_2.addWidget(self.lw_list_chats)
        self.pb_main_newchat = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_main_newchat.sizePolicy().hasHeightForWidth())
        self.pb_main_newchat.setSizePolicy(sizePolicy)
        self.pb_main_newchat.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pb_main_newchat.setObjectName("pb_main_newchat")
        self.verticalLayout_2.addWidget(self.pb_main_newchat)
        self.pb_main_contacts = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pb_main_contacts.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pb_main_contacts.setObjectName("pb_main_contacts")
        self.verticalLayout_2.addWidget(self.pb_main_contacts)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.l_main_avatar = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_main_avatar.sizePolicy().hasHeightForWidth())
        self.l_main_avatar.setSizePolicy(sizePolicy)
        self.l_main_avatar.setMinimumSize(QtCore.QSize(64, 64))
        self.l_main_avatar.setMaximumSize(QtCore.QSize(64, 64))
        self.l_main_avatar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.l_main_avatar.setText("")
        self.l_main_avatar.setPixmap(QtGui.QPixmap("Drawing.png"))
        self.l_main_avatar.setScaledContents(True)
        self.l_main_avatar.setObjectName("l_main_avatar")
        self.horizontalLayout_3.addWidget(self.l_main_avatar)
        self.l_main_uname = QtWidgets.QLabel(self.layoutWidget)
        self.l_main_uname.setObjectName("l_main_uname")
        self.horizontalLayout_3.addWidget(self.l_main_uname)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.l_current_chat = QtWidgets.QLabel(self.layoutWidget)
        self.l_current_chat.setTextFormat(QtCore.Qt.RichText)
        self.l_current_chat.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.l_current_chat.setWordWrap(True)
        self.l_current_chat.setObjectName("l_current_chat")
        self.verticalLayout.addWidget(self.l_current_chat)
        self.te_list_msg = QtWebEngineWidgets.QWebEngineView(self.layoutWidget)
        self.te_list_msg.setUrl(QtCore.QUrl("about:blank"))
        self.te_list_msg.setObjectName("te_list_msg")
        self.verticalLayout.addWidget(self.te_list_msg)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.f_main_tools = QtWidgets.QFrame(self.layoutWidget1)
        self.f_main_tools.setMaximumSize(QtCore.QSize(16777215, 25))
        self.f_main_tools.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    border: none;\n"
"    color: #333;\n"
"    max-width: 33px;\n"
"    margin: 0;\n"
"    padding: 0;\n"
"}\n"
"QPushButton:hover {\n"
"    border: 1px solid #66BB6A;\n"
"}\n"
"QFrame {\n"
"    background: none;\n"
"    border: none;\n"
"    margin: 0;\n"
"    padding: 0;\n"
"}\n"
"#f_main_tools {\n"
"    margin-bottom: -0px;\n"
"    border-top: 1px solid #66BB6A;\n"
"}\n"
"#pb_bold {\n"
"    font-weight: bold;\n"
"}\n"
"#pb_italic {\n"
"    font-style: italic;\n"
"}\n"
"#pb_underline {\n"
"    text-decoration: underline;\n"
"}")
        self.f_main_tools.setObjectName("f_main_tools")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.f_main_tools)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pb_bold = QtWidgets.QPushButton(self.f_main_tools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_bold.sizePolicy().hasHeightForWidth())
        self.pb_bold.setSizePolicy(sizePolicy)
        self.pb_bold.setMinimumSize(QtCore.QSize(24, 24))
        self.pb_bold.setMaximumSize(QtCore.QSize(33, 24))
        self.pb_bold.setWhatsThis("")
        self.pb_bold.setObjectName("pb_bold")
        self.horizontalLayout_6.addWidget(self.pb_bold)
        self.pb_italic = QtWidgets.QPushButton(self.f_main_tools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_italic.sizePolicy().hasHeightForWidth())
        self.pb_italic.setSizePolicy(sizePolicy)
        self.pb_italic.setMinimumSize(QtCore.QSize(24, 24))
        self.pb_italic.setMaximumSize(QtCore.QSize(33, 24))
        self.pb_italic.setObjectName("pb_italic")
        self.horizontalLayout_6.addWidget(self.pb_italic)
        self.pb_underline = QtWidgets.QPushButton(self.f_main_tools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_underline.sizePolicy().hasHeightForWidth())
        self.pb_underline.setSizePolicy(sizePolicy)
        self.pb_underline.setMinimumSize(QtCore.QSize(24, 24))
        self.pb_underline.setMaximumSize(QtCore.QSize(33, 24))
        self.pb_underline.setObjectName("pb_underline")
        self.horizontalLayout_6.addWidget(self.pb_underline)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_4.addWidget(self.f_main_tools)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.te_input_msg = QtWidgets.QTextEdit(self.layoutWidget1)
        self.te_input_msg.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        self.te_input_msg.setFont(font)
        self.te_input_msg.setUndoRedoEnabled(False)
        self.te_input_msg.setObjectName("te_input_msg")
        self.horizontalLayout.addWidget(self.te_input_msg)
        self.pb_send = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_send.sizePolicy().hasHeightForWidth())
        self.pb_send.setSizePolicy(sizePolicy)
        self.pb_send.setMaximumSize(QtCore.QSize(16777215, 200))
        self.pb_send.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pb_send.setObjectName("pb_send")
        self.horizontalLayout.addWidget(self.pb_send)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addWidget(self.splitter_2)
        self.main_stack.addWidget(self.main_page)
        self.verticalLayout_3.addWidget(self.main_stack)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.main_stack.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hanita"))
        self.login_greet.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600; color:#ffffff;\">Welcome to Hanita</span></p></body></html>"))
        self.le_login_input.setPlaceholderText(_translate("MainWindow", "Enter your login"))
        self.le_login_password.setPlaceholderText(_translate("MainWindow", "Enter your password"))
        self.pb_login_submit.setText(_translate("MainWindow", "Login"))
        self.label.setText(_translate("MainWindow", "Chats:"))
        __sortingEnabled = self.lw_list_chats.isSortingEnabled()
        self.lw_list_chats.setSortingEnabled(False)
        item = self.lw_list_chats.item(0)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.lw_list_chats.item(1)
        item.setText(_translate("MainWindow", "New Item"))
        item = self.lw_list_chats.item(2)
        item.setText(_translate("MainWindow", "New Item"))
        self.lw_list_chats.setSortingEnabled(__sortingEnabled)
        self.pb_main_newchat.setText(_translate("MainWindow", "New Chat"))
        self.pb_main_contacts.setText(_translate("MainWindow", "Contacts"))
        self.l_main_uname.setText(_translate("MainWindow", "uname"))
        self.l_current_chat.setText(_translate("MainWindow", "all"))
        self.pb_bold.setToolTip(_translate("MainWindow", "Bold"))
        self.pb_bold.setText(_translate("MainWindow", "B"))
        self.pb_italic.setToolTip(_translate("MainWindow", "Italic"))
        self.pb_italic.setText(_translate("MainWindow", "I"))
        self.pb_underline.setToolTip(_translate("MainWindow", "Underline"))
        self.pb_underline.setText(_translate("MainWindow", "U"))
        self.te_input_msg.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pb_send.setText(_translate("MainWindow", "Send"))

from PyQt5 import QtWebEngineWidgets
