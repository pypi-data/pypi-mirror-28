import random
import sys
import time

from PyQt5 import Qt, QtCore, QtWidgets

import form_contacts
import form_new_chat
import form_main


class ContactsDialog(QtWidgets.QDialog):
    handle_msg = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, user_list=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = form_contacts.Ui_dialog_contacts()
        self.ui.setupUi(self)

        self.data = {}

        user_list = user_list or []
        for user in user_list:
            self.createItem(user)

        self.ui.lw_contacts.itemDoubleClicked.connect(self.chat_with)
        self.ui.pb_add_contact.clicked.connect(self.add_contact)
        self.parent().redraw_contacts.connect(self.redraw)

    @QtCore.pyqtSlot(list)
    def redraw(self, data):
        self.ui.lw_contacts.clear()
        for user in data:
            self.createItem(user)

    def createItem(self, user):
        item = QtWidgets.QListWidgetItem(self.ui.lw_contacts)
        widget = QtWidgets.QWidget()
        widgetText = QtWidgets.QLabel(user["user_name"])
        widgetButton = QtWidgets.QPushButton("X")
        widgetButton.setProperty("id", user["user_id"])
        widgetButton.clicked.connect(self.del_contact)
        widgetButton.setFixedWidth(24)
        widgetLayout = QtWidgets.QHBoxLayout()
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(widgetButton)

        widget.setLayout(widgetLayout)
        item.setSizeHint(widget.sizeHint())
        self.ui.lw_contacts.setItemWidget(item, widget)

        item.setData(QtCore.Qt.UserRole, user["user_id"])

    def add_contact(self):
        user_name = self.ui.le_add_input.text()
        self.ui.le_add_input.setText("")
        self.ui.le_add_input.setFocus()
        if user_name:
            self.handle_msg.emit(
                {
                    "action": "add_contact",
                    "user_name": user_name
                })

    def del_contact(self):
        self.handle_msg.emit(
            {
                "action": "del_contact",
                "user_id": self.sender().property("id")
            })

    def chat_with(self):
        action = "new_chat"
        selected_id = []
        user = self.ui.lw_contacts.selectedItems()
        if user:
            selected_id = [
                i.data(QtCore.Qt.UserRole)
                for i in user
            ]
        self.data = {"action": action, "chat_name": "",
                     "chat_user_ids": selected_id}

        self.handle_msg.emit(self.data)
        self.close()


class NewChatDialog(QtWidgets.QDialog):
    handle_msg = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, user_list=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = form_new_chat.Ui_dialog_new_chat()
        self.ui.setupUi(self)
        self.chat_data = {}

        user_list = user_list or []
        for user in user_list:
            item = QtWidgets.QListWidgetItem(self.ui.lw_chat_contacts)
            item.setText(user["user_name"])
            item.setData(QtCore.Qt.UserRole, user["user_id"])

        self.ui.pb_chat_create.clicked.connect(self.chat_create)

    def chat_create(self):
        name = self.ui.le_chat_name.text()
        if not name:
            QtWidgets.QMessageBox.information(
                self, "info", "Пожалуйста, введите название чата")
            return
        users = self.ui.lw_chat_contacts.selectedItems()
        if not users:
            QtWidgets.QMessageBox.information(
                self, "info", "Пожалуйста, выберите минимум одного пользователя")
            return
        users_data = [i.data(QtCore.Qt.UserRole) for i in users]
        self.chat_data = {
            "action": "new_chat",
            "chat_name": name,
            "chat_user_ids": users_data
        }
        self.handle_msg.emit(self.chat_data)
        self.close()


###############################################################################
# ### MainWindow
###############################################################################
class MainWindow(QtWidgets.QMainWindow):
    """
    Класс представления главного окна.
    Методы для переопределения:
        get_handle_msg(self, data)
        get_chatlist(self) -> [{'chat_id': ..., 'chat_name': ...,}, ...]
        get_contactlist(self) -> [{'user_id': ..., 'user_name': ...}, ...]
        get_msgslist(self) -> [{'user_name':..., 'timestamp':..., 'message':...,}, ...]
    """
    redraw_contacts = QtCore.pyqtSignal(list)
    change_view = QtCore.pyqtSignal()
    handle_msg = QtCore.pyqtSignal(dict)
    model_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = form_main.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.main_stack.setCurrentIndex(0)

        self.newchat_dialog = NewChatDialog
        self.contacts_dialog = ContactsDialog

        self.current_user = {
            "user_id": 1,
            "user_name": "Max"
        }
        self.current_chat = {
            "chat_id": None,
            "chat_name": None
        }

        self.storage = {
            "contacts": [],
            "chats": [],
            "messages": []
        }

        contact_list = [
            {"user_id": i, "user_name": "contact_{}".format(i)}
            for i in range(10)
        ]
        self.storage["contacts"] = contact_list

        self.ui.pb_main_newchat.clicked.connect(self.show_newchat_dialog)
        self.ui.pb_main_contacts.clicked.connect(self.show_contacts_dialog)
        self.ui.lw_list_chats.itemClicked.connect(self.change_current_chat)
        self.ui.pb_send.clicked.connect(self.send_message)
        self.ui.te_input_msg.installEventFilter(self)
        self.ui.pb_login_submit.clicked.connect(self.login)
        self.handle_msg.connect(self.get_handle_msg)
        self.model_changed.connect(self.render)
        self.change_view.connect(self.change_current_view)

    def eventFilter(self, source, event):
        """ Фильтр событий """
        if (event.type() == QtCore.QEvent.KeyPress and
                event.key() == QtCore.Qt.Key_Return):
            self.send_message()
            return True
        return QtWidgets.QMainWindow.eventFilter(self, source, event)

    def model_is_changed(self):
        """ Оповестить о изменении данных """
        self.model_changed.emit()

    def render(self):
        """ Перерисовать внешний вид """
        if self.current_user:
            self.draw_chatlist()
            self.draw_msgslist()
            self.redraw_contacts.emit(self.get_contactlist())

    def change_current_view(self):
        self.ui.main_stack.setCurrentIndex(1)

    def change_current_chat(self):
        """ Изменить активный чат """
        item = self.ui.lw_list_chats.selectedItems()[0]
        chat_id = item.data(QtCore.Qt.UserRole)
        chat_name = item.text()
        self.current_chat = {
            "chat_id": chat_id,
            "chat_name": chat_name
        }
        self.model_is_changed()

    def login(self):
        self.ui.login_error.setText("")
        login = self.ui.le_login_input.text().strip()
        password = self.ui.le_login_password.text()
        if not login:
            self.ui.login_error.setText("Error: empty login")
            return

        msg = {
            "action": "authenticate",
            "user": {
                "login": login,
                "password": password
            }
        }
        self.handle_msg.emit(msg)

    @QtCore.pyqtSlot(dict)
    def get_handle_msg(self, data):
        """ Обработка управляющих сообщений.
            Данный метод нужно переопределить.
        """
        if data["action"] == "del_contact":
            #########################################
            _id = data["user_id"]
            self.storage["contacts"] = [
                i for i in self.storage["contacts"] if i["user_id"] != _id
            ]
            ###########################################
        elif data["action"] == "add_contact":
            _id = random.randint(100, 10000)
            self.storage["contacts"].append(
                {"user_id": _id, "user_name": data["user_name"]})
        elif data["action"] == "new_chat":
            if data["chat_name"]:
                chat = {"chat_id": random.randint(
                    1, 1000), "chat_name": data["chat_name"]}
            else:
                user_name = ""
                contacts = self.get_contactlist()
                for user in self.storage["contacts"]:
                    if user["user_id"] == data["contact_ids"][0]:
                        user_name = user["user_name"]
                chat = {"chat_id": random.randint(
                    1, 1000), "chat_name": user_name}
            self.storage["chats"].append(chat)
        elif data["action"] == "msg":
            data["user_id"] = self.current_user["user_id"]
            self.storage["messages"].append(data)
        elif data["action"] == "leave":
            chats = self.storage["chats"]
            chats = [i for i in chats if i["chat_id"] != data["chat_id"]]
            self.storage["chats"] = chats
        elif data["action"] == "authenticate":
            self.ui.main_stack.setCurrentIndex(1)
        self.model_is_changed()

    def show_newchat_dialog(self):
        """ Показать окно создания нового чата """
        dialog = self.newchat_dialog(self, self.get_contactlist())
        dialog.handle_msg.connect(self.get_handle_msg)
        dialog.exec_()

    def show_contacts_dialog(self):
        """ Показать окно контактов """
        dialog = self.contacts_dialog(self, self.get_contactlist())
        dialog.handle_msg.connect(self.get_handle_msg)
        dialog.exec_()

    def draw_chatlist(self):
        """ Перерисовать окно chatlist """
        self.ui.lw_list_chats.clear()
        data = self.get_chatlist()
        for chat in data:
            self.createItem(chat)

    def createItem(self, chat):
        item = QtWidgets.QListWidgetItem(self.ui.lw_list_chats)
        widget = QtWidgets.QWidget()
        widgetText = QtWidgets.QLabel(chat["chat_name"])
        widgetButton = QtWidgets.QPushButton("X")
        widgetButton.setProperty("id", chat["chat_id"])
        widgetButton.clicked.connect(self.del_chat)
        widgetButton.setFixedWidth(24)
        widgetLayout = QtWidgets.QHBoxLayout()
        widgetLayout.addWidget(widgetText)
        widgetLayout.addWidget(widgetButton)
        widget.setLayout(widgetLayout)
        item.setSizeHint(widget.sizeHint())
        self.ui.lw_list_chats.setItemWidget(item, widget)
        item.setData(QtCore.Qt.UserRole, chat["chat_id"])
        if self.current_chat["chat_id"] == chat["chat_id"]:
            self.ui.lw_list_chats.setCurrentItem(item)

    def del_chat(self):
        """ Сгенерировать сообщение о покидании чата. """
        msg = {
            "action": "leave",
            "chat_id": self.sender().property("id")
        }
        self.handle_msg.emit(msg)

    def get_chatlist(self):
        """ Получить список чатов.
            Данный метод нужно переопределить.
        """
        return self.storage["chats"]

    def get_contactlist(self):
        """ Получить список контактов.
            Данный метод нужно переопределить.
        """
        return self.storage["contacts"]

    def get_msgslist(self):
        """ Получить список сообщений для активного чата.
            Данный метод нужно переопределить.
        """
        cur_msgs = [
            i for i in self.storage["messages"]
            if i["chat_id"] == self.current_chat["chat_id"]
        ]
        return [
            {
                "user_id": i["user_id"],
                "user_name": self.current_user["user_name"],
                "timestamp": i["timestamp"],
                "message": i["message"]
            }
            for i in cur_msgs
        ]

    def send_message(self):
        """ Отправить сообщение. """
        text = self.ui.te_input_msg.toPlainText()
        self.ui.te_input_msg.setText("")
        self.ui.te_input_msg.setFocus()
        if text:
            message = {
                "action": "msg",
                "chat_id": self.current_chat["chat_id"],
                "timestamp": time.time(),
                "message": text
            }
            self.handle_msg.emit(message)

    def draw_msgslist(self):
        """ Перерисовать окно чата """
        messages = self.get_msgslist()
        chat_id = self.current_chat["chat_id"]
        chat_name = self.current_chat["chat_name"]
        self.ui.l_current_chat.setText(chat_name)
        curr_user_id = self.current_user["user_id"]
        curr_user_name = self.current_user["user_name"]

        arr = []
        for i, msg in enumerate(messages):
            formated_msg = self.format_msg(
                name=msg["user_name"],
                text=msg["message"],
                timestamp=msg["timestamp"],
                ident=msg["user_id"] == curr_user_id,
                add=msg["user_id"] == messages[i -
                                               1]["user_id"] if i > 0 else False
            )
            arr.append(formated_msg)
        msg_string = '<body bgcolor="#FFF">' + \
            "".join(arr) + '<a name="end" style="color:#FFF">a</a>' + '</html>'
        self.ui.te_list_msg.setHtml(msg_string)
        self.ui.te_list_msg.scrollToAnchor("end")

    def format_msg(self, name, text, timestamp, ident=False, add=False):
        """ Отформатировать текст для отображения. """
        template_text = '''
            <div style="margin:0 {right} 0 {left};">
                {text}
            </div>
            '''

        template_name = '''
            <div style="margin:15px {right} 0 {left};">
                <b style="color:{color};">
                    {name}
                </b>
                <i style="color:lightgrey;font-size:small;">
                    {timestamp}
                </i>
            </div>
            '''

        formated_name = template_name.format(
            left="5px" if ident else "25px",
            right="25px" if ident else "5px",
            color="orange" if ident else "blue",
            name=name,
            timestamp=time.ctime(timestamp),
        )
        formated_text = template_text.format(
            left="15px" if ident else "35px",
            right="25px" if ident else "5px",
            text=text.replace("\n", "<br>")
        )

        if add:
            return formated_text
        return formated_name + formated_text


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
