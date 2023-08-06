import base64
import json
import os
import socket
import socketserver
import threading
import time
from pprint import pprint

from hanita_JIM import JIMMessage, JIMResponse

from .models import *
from .server_db import ServerDB

RECV_BUFFER = 1024


def history_it(user_id, action):
    """ Функция пробует связаться с микросервисом ms_hanita_hist и,
    в случае успеха, передает туда сообщения о входе/выходе пользователей.
    Выполнение сервиса не является обязательным, поэтому ошибки игнорируются.
    """
    try:
        with socket.create_connection(("127.0.0.1", 5555)) as conn:
            data = {
                "user_id": user_id,
                "action": action,
                "timestamp": time.time()
            }
            json_data = json.dumps(data)
            conn.send(json_data.encode())
    except:
        pass


###############################################################################
# ### ClientRequestHandler
###############################################################################
class ClientRequestHandler(socketserver.BaseRequestHandler):
    """ Класс-обработчик запросов клиента """

    def setup(self):
        # yapf: disable
        self.action_handlers = {
            JIMMessage.MSG: self.handler_msg,
            JIMMessage.QUIT: self.handler_quit,
            JIMMessage.AUTHENTICATE: self.handler_authenticate,
            JIMMessage.PRESENCE: self.handler_presence,
            # JIMMessage.WHO_ONLINE: self.handler_who_online,
            JIMMessage.GET_CONTACTS: self.handler_get_contacts,
            JIMMessage.ADD_CONTACT: self.handler_add_contact,
            JIMMessage.DEL_CONTACT: self.handler_del_contact,
            JIMMessage.NEW_CHAT: self.handler_new_chat,
            JIMMessage.GET_CHATS: self.handler_get_chats,
            JIMMessage.LEAVE: self.handler_leave,
            JIMMessage.NEW_AVATAR: self.handler_new_avatar,
            JIMMessage.GET_AVATAR: self.handler_get_avatar,
            JIMMessage.GET_MSGS: self.handler_get_msgs,
        }
        # yapf: enable
        self.__quit = False
        self.msg = None
        self.user = None
        self._authenticate = False
        db_name = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)), 'server.db')
        self.db = ServerDB(self.server.base, "sqlite:///" + db_name)
        self.lock = threading.Lock()

    def _login_required(func):
        def inner(self, *args, **kwargs):
            if self._authenticate:
                return func(self, *args, **kwargs)
            else:
                self.send(JIMResponse(401))

        return inner

    def handle(self):
        """ Основной обработчик """
        while not self.__quit:
            msgs = self.get()
            if msgs:
                for msg in msgs:
                    if self.__quit:
                        break
                    if msg.action and msg.action in self.action_handlers:
                        self.msg = msg
                        action_handler = self.action_handlers[msg.action]
                        action_handler()
                        self.msg = None
                    else:
                        self.send(JIMResponse(400))

    def finish(self):
        if self.user:
            self.db.set_user_online(self.user.id, False)
            self.user = None
        self.db.close()

    def response(self, resp_code=None):
        """ Ответить на сообщение """
        if resp_code:
            self.send(JIMResponse(resp_code))

    def send_to_chat(self, chat_id, message):
        """ Отправить сообщение всем авторизованным пользователям чата. """
        if "_id" in message:
            message["_id"] = str(message["_id"])
        online_users = self.db.get_online_users(chat_id)
        print("\nsend_to_chat online_users:")
        pprint(online_users)
        for user in online_users:
            self.send_to(user, message)

    def send_to_all(self, message):
        """ Отправить сообщение всем авторизованным пользователям. """
        chats = self.db.get_chats_for(self.user.id)
        for chat in chats:
            self.send_to_chat(chat.id, message)

    def get(self):
        """ Получить сообщение от ... """
        _get_data = True
        bmsg = b""
        while _get_data:
            try:
                data = self.request.recv(RECV_BUFFER)
            except ConnectionError:
                self.__quit = True
                break
            if data == b"" or data.decode().endswith("}"):
                _get_data = False
            bmsg += data
        if bmsg:
            messages_str = bmsg.decode().replace("}{", "}<split>{")
            arr_msgstr = messages_str.split("<split>")
            msgs = [JIMMessage(json.loads(msg)) for msg in arr_msgstr]

            return msgs

    def send_to(self, user, message):
        """ Отправить сообщение другому клиенту """
        json_msg = json.dumps(message)
        bmsg = json_msg.encode("utf_8")
        with socket.fromfd(user.fileno, socket.AF_INET,
                           socket.SOCK_STREAM) as s:
            try:
                # print("send_to:", user.name, bmsg)
                s.sendall(bmsg)
            except socket.error:
                self.db.set_user_online(user.id, False)
                self.__quit = True

    def send(self, message):
        """ Ответить отправителю """
        msg = json.dumps(message).encode()
        try:
            self.request.sendall(msg)
        except ConnectionError:
            self.db.set_user_online(self.user.id, False)
            self.__quit = True

    # handlers ################################################################

    def handler_authenticate(self):
        """
        Аутентификация пользователя.
        Возвращает код ответа.
        """
        if self.msg.action != JIMMessage.AUTHENTICATE:
            raise
        if self.msg.user and set(self.msg.user) == {"login", "password"}:
            login = self.msg.user["login"]
            password = self.msg.user["password"]
            user = User(login)
            # Если пользователя нет в базе
            user_id = self.db.get_user_id(login)
            if user_id is None:
                self.db.add_obj(user)
                print("user.id:", user.id)
            else:
                user = self.db.get_obj(User, user_id)
            print(user_id)
            print(user)
            self.user = user
            self.db.set_user_online(user.id, True, self.request.fileno())
            self._authenticate = True
            self.server.clients[self.request] = user.id
            user_info = {"user_id": user.id, "user_name": user.name}
            response = JIMResponse(202, user=user_info)
            response["action"] = "authenticate"
            print("\nauthentication response:")
            pprint(response)
            self.send(response)

            # внести вход в историю, если запущен ms_hanita_hist
            history_it(self.user.id, "enter")
        else:
            self.send(JIMResponse(400))

    @_login_required
    def handler_get_chats(self):
        user_chats = self.db.get_chats_for(self.user.id)
        for chat in user_chats:
            chat_info = self.get_chat_info(chat.id)
            self.send(chat_info)

    @_login_required
    def handler_quit(self):
        """ Обработчик события Quit """
        if self.msg.action != JIMMessage.QUIT:
            raise

        self.__quit = True
        self.send(JIMResponse(200))

        # внести выход в историю, если запущен ms_hanita_hist
        history_it(self.user.id, "quit")

    @_login_required
    def handler_msg(self):
        """ Обработчик события MSG.
        Принимает сообщение вида:
            {
                "action": "msg",
                "chat_id": ...,
                "timestamp": ...,
                "message": ...,
            }

        Сохраняет в базе.
        Если есть пользователи онлайн, то пересылает им это сообщение,
        предварительно добавив поле user, определяющее автора сообшение.
        Т.е. отсылает следующую структуру:
            {
                "action": "msg",
                "chat_id": ...,
                "timestamp": ...,
                "user": {
                    "user_id": self.user.id,
                    "user_name": self.user.name,
                }
                "message": ...,
            }

        """
        if self.msg.action != JIMMessage.MSG:
            raise
        print("handler_msg self.msg:", self.msg)
        self.send(JIMResponse(200))
        out_msg = self.msg
        out_msg.user = {"user_id": self.user.id, "user_name": self.user.name}
        self.db.add_chat_msg(out_msg)
        print("handler_msg out_msg:", out_msg)
        self.send_to_chat(self.msg.chat_id, out_msg)

    @_login_required
    def handler_presence(self):
        """ Обработчик события Presence """
        if self.msg.action != JIMMessage.PRESENCE:
            raise
        self.send(JIMResponse(200))

    @_login_required
    def handler_get_contacts(self):
        """ Обработчик события get_contacts.
        Отправляет пользователю следующую структуру:
        {
            "action": "contact_list",
            "contacts": [
                {
                    "user_id": int,
                    "user_name": str,
                },
                ...
            ]
        }
          """
        contact_list = self.db.get_contacts_for(self.user.id)
        users = []
        for contact in contact_list:
            user = {
                "user_id": contact.id,
                "user_name": contact.name
            }
            users.append(user)
        msg = {
            "action": "contact_list",
            "contacts": users
        }
        # print("_get_contacts out_msg:", msg)
        self.send(msg)

    @_login_required
    def handler_add_contact(self):
        """ Обработчик события ADD_CONTACT """
        # print("handler_add_contact msg:", self.msg)
        contact_name = self.msg["user_name"]
        contact_id = self.db.get_user_id(contact_name)
        if not contact_id:
            # упрощение, просто добавит нового пользователя
            user = self.db.add_new_user(contact_name)
            contact_id = user.id
        self.db.add_contact(self.user.id, contact_id)
        contact = {
            "user_id": contact_id,
            "user_name": contact_name
        }
        msg = {
            "action": "contact_list",
            "contacts": [contact]
        }
        self.send(msg)

    @_login_required
    def handler_del_contact(self):
        """ Обработчик события del_contact. """
        # print("handler_del_contact msg:", self.msg)
        self.db.del_contact(self.user.id, self.msg.user_id)
        self.send(self.msg)

    @_login_required
    def handler_new_chat(self):
        """ Обработчик события new_chat """
        chat_name = self.msg["chat_name"]
        chat_user_ids = self.msg["chat_user_ids"]
        chat = self.db.add_new_chat(chat_name)
        print("self.user.id:", self.user.id)
        self.db.add_user_to_chat(chat.id, self.user.id)
        for user_id in chat_user_ids:
            self.db.add_user_to_chat(chat.id, user_id)
        msg = self.get_chat_info(chat.id)
        self.send_to_chat(chat.id, msg)

    @_login_required
    def get_chat_info(self, chat_id):
        """ Получить информацию о чате.
        Возвращает структуру:
        {
            "action": "chat_info",
            "chat": {
                "chat_id": int,
                "chat_name": str
            },
            "chat_users": [
                {
                    "user_id": int,
                    "user_name": str
                },
                ...
            ]
        }
        """
        chat = self.db.get_chat(chat_id)
        users = self.db.get_users_for(chat.id)
        chat_users = []
        for user in users:
            chat_user = {"user_id": user.id, "user_name": user.name}
            chat_users.append(chat_user)
        print(chat_users)
        msg = {
            "action": JIMMessage.CHAT_INFO,
            "chat": {
                "chat_id": chat.id,
                "chat_name": chat.name
            },
            "chat_users": chat_users
        }
        msg["from"] = self.user.id

        return msg

    @_login_required
    def handler_leave(self):
        """ Покинуть чат. Обработчик события leave. """
        chat_id = self.msg["chat_id"]
        user_id = self.user.id
        self.db.del_user_from_chat(chat_id, user_id)
        self.send(self.msg)

    def send_avatar(self, user_id):
        """ Отправить аватарку пользователю. """
        # avatar_str = ""
        path_to_avatar = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "avatars", str(user_id))
        if os.path.isfile(path_to_avatar):
            with open(path_to_avatar, "r") as avatar:
                msg = {
                    "action": "avatar",
                    "user_id": user_id,
                    "avatar": avatar.read()
                }
                self.send(msg)

    @_login_required
    def handler_new_avatar(self):
        """ Получить и сохранить аватарку от пользователя. """
        print("*** message new_avatar ***")
        path_to_avatar = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "avatars", str(self.user.id)
        )
        with open(path_to_avatar, "w") as avatar_file:
            # image = base64.b64decode(self.msg["avatar"])
            avatar_file.write(self.msg["avatar"])
        info_msg = {
            "action": JIMMessage.AVATAR_CHANGED,
            "user_id": self.user.id
        }
        self.send_to_all(info_msg)

    @_login_required
    def handler_get_avatar(self):
        """ Обработчик сообщения get_avatar. """
        print("get_avatar")
        print(self.msg)
        self.send_avatar(self.msg["user_id"])

    @_login_required
    def handler_get_msgs(self):
        """ Обработчик сообщения get_msgs """
        msgs = self.db.get_chat_msgs(self.msg["chat_id"])
        for msg in msgs:
            msg["_id"] = str(msg["_id"])
            self.send(msg)
