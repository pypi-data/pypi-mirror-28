import base64
import os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal

from .forms.app_ui import MainWindow


class QtClientView(MainWindow):
    """ Класс представления пользовательского интерфейса """
    app = QtWidgets.QApplication([])
    model_changed = pyqtSignal()

    def __init__(self, client=None, parent=None):
        super().__init__(parent)
        self.controller = client
        self.client_db = None
        self.thread = None
        self.default_avatar = None
        self._inited = False
        self.load_default_avatar()

    def set_client_db(self, client_db):
        """ Передать объект хранилища, откуда будет браться инфо
        для отображения
        """
        self.client_db = client_db
        if self.client_db:
            self.client_db.add_observer(self)

    def run(self):
        """ Запускает цикл интерфейса """
        ################
        self.thread = QThread()
        self.controller.moveToThread(self.thread)
        self.thread.started.connect(self.render)
        self.thread.started.connect(self.controller.receive)
        self.thread.start()
        ################
        self.show()
        self.app.exec_()

    def render_info(self, info):
        """ Отрисовывает информационное окно. """
        msg = QtWidgets.QMessageBox()
        msg.setText(str(info))
        msg.exec()

    def input(self, msg):
        """ Отрисовывает окно с вопросом и полем ввода для ответа. """
        text, ok = QtWidgets.QInputDialog.getText(self, "Login",
                                                  "Enter your name")
        return text

    def get_chatlist(self):
        """ Получить список чатов. """
        chats = []
        if self.client_db:
            chat_ids = self.client_db.get_chats()
            for _id in chat_ids:
                chat = self.client_db.get_chat(_id)
                chats.append(chat)
        return chats

    def get_contactlist(self, filter_str=""):
        """ Получить список контактов. """
        # if filter_str:
        #     print("get_contactlist filter_str", filter_str)
        contacts = []
        if self.client_db:
            contacts = self.client_db.get_contacts(
                self.current_user["user_id"], filter_str)
        return contacts

    def get_msgslist(self):
        """ Возвращает список сообщений чата.
        {
            "user_id": ...,
            "user_name": ...,
            "timestamp": ...,
            "message": ...
        }
        """
        msgs_ids = self.client_db.get_msgs(self.current_chat["chat_id"])
        msgs = []
        for _id in msgs_ids:
            msg = self.client_db.get_msg(_id)
            user_id = msg["user_id"]
            user_name = self.client_db.get_user(user_id)["user_name"]
            timestamp = msg["timestamp"]
            message = msg["message"]
            msg_out = {
                "user_id": user_id,
                "user_name": user_name,
                "timestamp": timestamp,
                "message": message
            }
            msgs.append(msg_out)
        return msgs

    def update_avatar(self):
        """ Получить из бд аватарку. """
        self.avatar = self.client_db.get_user_avatar(
            self.current_user["user_id"])
        pixmap = QtGui.QPixmap()
        if self.avatar:
            pixmap.loadFromData(base64.b64decode(self.avatar))
        else:
            pixmap.loadFromData(base64.b64decode(self.default_avatar))

        self.ui.l_main_avatar.setPixmap(pixmap)

    def get_avatar(self, user_id):
        """ Получить из бд аватарку для пользователя user_id. """
        avatar_str = self.client_db.get_user_avatar(user_id)
        if avatar_str:
            return avatar_str
        else:
            return self.default_avatar

    def load_default_avatar(self):
        avatar_path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ), "forms", "templates", "default_avatar.png"
        )
        with open(avatar_path, "rb") as avatar_file:
            avatar_raw = avatar_file.read()
            avatar_encoded_bytes = base64.b64encode(avatar_raw).decode()
            self.default_avatar = avatar_encoded_bytes

    def get_handle_msg(self, data):
        self.controller.send_to_server(data)


if __name__ == "__main__":
    app = QtClientView()
    app.run()
