""" Hanita client class and client mainloop """
import base64
import os
import sys
import time

from PyQt5.QtCore import QObject

from hanita_JIM import JIMClientMessage, JIMMessage

from .client_connection import ClientConnection, ClientConnectionError
from .client_db import ClientDB
from .client_qtview import QtClientView

WAITING_TIME = 1.0


###############################################################################
# class Client
###############################################################################
class Client:
    """ класс Client """

    def __init__(self, conn: ClientConnection, ViewClass: QtClientView):
        super().__init__()
        # self.user = ClientUser()
        self.self_id = None
        self.client_db = None
        self.connection = conn
        self._receiving = True
        self.view = ViewClass(self)
        self.msg_handlers = {
            JIMMessage.MSG: self.handle_msg,
            JIMMessage.CONTACT_LIST: self.handle_contact,
            JIMMessage.CHAT_INFO: self.handle_chat_info,
            JIMMessage.DEL_CONTACT: self.handle_del_contact,
            JIMMessage.LEAVE: self.handle_leave,
            JIMMessage.AUTHENTICATE: self.handle_authenticate,
            JIMMessage.AVATAR: self.handle_avatar,
            JIMMessage.AVATAR_CHANGED: self.handle_avatar_changed,
        }
        try:
            self.connection.connect()
        except ClientConnectionError:
            self.view.render_info("Не могу соединиться с сервером")
            self.connection = None
            self.close()

    def send_presence(self):
        """ Сообщаем серверу о присутствии """
        msg = JIMClientMessage.presence()
        self.send_to_server(msg)

    def handle_authenticate(self, msg):
        """ Обработка сообщения authenticate """
        if msg.response == 202 and msg.user:
            db_name = msg.user["user_name"] + ".db"
            full_db_name = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)), db_name)
            self.client_db = ClientDB(full_db_name)
            self.view.set_client_db(self.client_db)
            self.view.current_user = msg.user
            self.client_db.active_user = msg.user
            self.get_init_info()
            self.view.change_view.emit()

    def send_to_server(self, message):
        """
        Отправляем на сервер сообщение от пользователя.
        """
        self.connection.send(message)

    def send_and_get(self, message):
        """
        Отправляем на сервер и обрабатываем ответ от сервера.
        """
        self.connection.send(message)
        resp = None
        start = time.time()
        while resp is None:
            resp = self.connection.get()
            if time.time() - start > WAITING_TIME:
                self.view.render_info("Потеряна связь с сервером")
                break
        return resp

    def get_from(self):
        """ Получаем и обрабатываем сообщение, присланное от другого клиента """
        msgs = self.connection.get()
        for msg in msgs:
            if msg:
                self.handle(msg)

    def handle(self, msg):
        """ Обрабатываем полученные сообщения """
        if msg and msg.action and msg.action in self.msg_handlers:
            self.msg_handlers[msg.action](msg)

    def handle_avatar(self, msg):
        """ Обработка сообщения avatar. """
        # print(msg)
        image_str = msg["avatar"]
        # image = base64.b64decode(image_raw)
        self.client_db.update_user(msg["user_id"], avatar_bytes=image_str)

    def handle_avatar_changed(self, msg):
        """ Обработка сообщения об изменении аватарки пользователя. """
        self.send_to_server(JIMClientMessage.get_avatar(msg["user_id"]))

    def handle_msg(self, msg):
        """ Обработка сообщения msg """
        msg_id = msg["_id"]
        user = msg.user
        chat_id = msg.chat_id
        if not self.client_db.msg_exists(msg_id):
            self.client_db.add_msg(
                msg_id, user["user_id"], chat_id, msg.timestamp, msg.message)

    def handle_contact(self, msg):
        """ Обработка сообщения contact_list """
        contacts = msg["contacts"]
        for contact in contacts:
            user_id = contact["user_id"]
            user_name = contact["user_name"]
            self.client_db.update_user(user_id, user_name, True)

    def handle_del_contact(self, msg):
        """ Обработка сообщения del_contact. """
        contact_id = msg["user_id"]
        self.client_db.update_user(contact_id, contact=False)

    def handle_chat_info(self, msg):
        """ Обработка сообщения chat_list """
        # print("chat_info")
        chat_id = msg.chat["chat_id"]
        chat_name = msg.chat["chat_name"]
        chat_users = msg.chat_users
        if not chat_name:
            chat_name = self.create_chat_name(chat_users)
        if not self.client_db.chat_exists(chat_id):
            self.client_db.add_chat(chat_id, chat_name)

        if self.view.current_user["user_id"] == msg["from"]:
            self.view.current_chat = msg.chat

        for user in chat_users:
            self.client_db.update_user(user["user_id"], user["user_name"])
            self.send_to_server(JIMClientMessage.get_avatar(user["user_id"]))
        
        self.send_to_server(JIMClientMessage.get_msgs(chat_id))

    def handle_leave(self, msg):
        """ Обработка сообщения покинуть чат leave. """
        chat_id = msg["chat_id"]
        self.client_db.del_chat(chat_id)

    def create_chat_name(self, users):
        """ Создает имя чата на основе списка пользователей чата. """
        users_len = len(users)
        if not users_len:
            return
        elif users_len == 1:
            return users[0]["user_name"]
        user_names = [
            user["user_name"] for user in users
            if user["user_name"] != self.client_db.active_user["user_name"]
        ]
        chat_name = ", ".join(user_names)
        return chat_name

    def run(self):
        """ Главный цикл работы клиента """
        self.view.run()
        self.close()

    def get_init_info(self):
        get_messages = [
            JIMClientMessage.get_avatar(self.view.current_user["user_id"]),
            JIMClientMessage.get_contacts(),
            JIMClientMessage.get_chats(),
        ]
        for msg in get_messages:
            self.send_to_server(msg)

    def receive(self):
        """ Получаем сообщения от сервера """
        while self._receiving:
            self.get_from()

    def close(self, info=""):
        """ Закрываем клиент """
        msg = JIMClientMessage.quit()
        print("close client")
        self._receiving = False
        if self.connection:
            self.connection.send(msg)
            self.connection.close()
            self.connection = None
        if self.client_db:
            self.client_db.close()
            self.client_db = None
        if info:
            self.view.render_info(info)
        sys.exit()


class QtClient(Client, QObject):
    pass
