""" Модель данных для клиента """
import sqlite3
import threading
import time


class ClientDBError(Exception):
    pass


###############################################################################
# ### ClientDB
###############################################################################
class ClientDB:
    def __init__(self, path_to_db=None):
        self._observers = []
        self._active_chat = None
        self._active_user = None
        self.lock = threading.Lock()
        if not path_to_db:
            path_to_db = ":memory:"
        self.conn = sqlite3.connect(path_to_db, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.setup()

    @property
    def active_user(self):
        return self.get_user(self._active_user)

    @active_user.setter
    def active_user(self, user):
        self._active_user = user["user_id"]
        self.update_user(user["user_id"], user["user_name"])

    @property
    def active_chat(self):
        return self._active_chat

    @active_chat.setter
    def active_chat(self, chat_name):
        self._active_chat = chat_name
        # self.add_chat(chat_name)

    def setup(self):
        """ Создаем таблицы """
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                user_name TEXT,
                avatar BLOB,
                contact INTEGER CHECK(contact IN (0, 1)) DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS chats(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE,
                chat_name TEXT,
                read_time REAL 
            );

            CREATE TABLE IF NOT EXISTS chat_users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (chat_id) REFERENCES chats(id),
                CONSTRAINT  unique_user_for_chat UNIQUE (user_id, chat_id)
            );

            CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                msg_id INTEGER UNIQUE NOT NULL,
                user_id INTEGER,
                chat_id INTEGER,
                time REAL,
                message TEXT,
                readed INTEGER CHECK(readed IN (0, 1)) DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
            );
            """)
        self.conn.commit()

    ############################################################################
    def user_exists(self, user_id):
        """ Проверить наличие пользователя """
        cmd = "SELECT 1 FROM users WHERE user_id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (user_id, ))
        result = self.cursor.fetchone()
        self.lock.release()
        return bool(result)

    def add_user(self, user_id, user_name, contact=False):
        """ Добавить пользователя в БД.
        Если пользователь с user_id уже имеется в базе,
        генерируется исключение ClientDBError
        """
        if self.user_exists(user_id):
            raise ClientDBError("user_id уже имеется в базе")
        cmd = "INSERT INTO users(user_id, user_name, contact) VALUES (?, ?, ?)"
        self.lock.acquire()
        self.cursor.execute(cmd, (user_id, user_name, int(contact)))
        self.conn.commit()
        self.lock.release()
        self._notify()

    def get_user(self, user_id):
        """
        Получить данные о пользователе из БД.
        Возвращает словарь
        {
            'user_id': ...,
            'user_name': ...
        }
        Если пользователя с user_id в БД не существует, возвращается {}
        """
        user = {}
        user_keys = ("user_id", "user_name")
        if self.user_exists(user_id):
            cmd = "SELECT * FROM users WHERE users.user_id = ?"
            self.lock.acquire()
            self.cursor.execute(cmd, (user_id, ))
            user_val = self.cursor.fetchone()[1:]
            self.lock.release()
            user = dict(zip(user_keys, user_val))

        return user

    def get_user_avatar(self, user_id):
        """ Получить аватарку пользователя. """
        if self.user_exists(user_id):
            cmd = "SELECT avatar FROM users WHERE user_id = ?"
            self.lock.acquire()
            self.cursor.execute(cmd, (user_id,))
            user_avatar = self.cursor.fetchone()[0]
            # print("user_avatar", user_avatar)
            self.lock.release()
            return user_avatar

    def update_user(self, user_id, user_name=None, contact=None, avatar_bytes=None):
        """
        Обновить данные о пользователе.
        Если пользователя нет в базе, то он будет добавлен.
        """
        if self.user_exists(user_id):
            self.lock.acquire()
            if user_name:
                cmd = "UPDATE users SET user_name = ? WHERE user_id = ?"
                self.cursor.execute(cmd, (user_name, user_id))
            if contact is not None:
                cmd = "UPDATE users SET contact = ? WHERE user_id = ?"
                self.cursor.execute(cmd, (int(contact), user_id))
            if avatar_bytes:
                cmd = "UPDATE users SET avatar = ? WHERE user_id = ?"
                self.cursor.execute(cmd, (avatar_bytes, user_id))
            self.conn.commit()
            self.lock.release()
            self._notify()
        else:
            contact = contact or False
            self.add_user(user_id, user_name, contact)

    def get_contacts(self, user_id, filter_str=""):
        """ Получить список контактов. """
        filter_str = "%"+filter_str+"%"
        # print(filter_str)
        cmd = "SELECT user_id, user_name FROM users WHERE contact = 1 AND user_name LIKE ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (filter_str,))
        users_data = self.cursor.fetchall()
        self.lock.release()
        user_keys = "user_id", "user_name"
        contacts = []
        for data in users_data:
            contact = dict(zip(user_keys, data))
            contacts.append(contact)
        # print("db.get_contacts:", contacts)
        return contacts

    ############################################################################
    def chat_exists(self, chat_id):
        """
        Проверить наличие чата с chat_id в БД
        """
        cmd = "SELECT 1 FROM chats WHERE chats.chat_id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_id, ))
        result = self.cursor.fetchone()
        self.lock.release()
        return bool(result)

    def add_chat(self, chat_id, chat_name):
        """ Добавить чат в БД. Если chat_id уже есть в базе,
        генерируется исключение ClientDBError.
        """
        if self.chat_exists(chat_id):
            raise ClientDBError("chat_id уже имеется в базе")
        cmd = "INSERT INTO chats(chat_id, chat_name) VALUES (?, ?)"
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_id, chat_name))
        self.conn.commit()
        self.lock.release()
        self._notify()

    def get_chat(self, chat_id):
        """
        Получить данные о чате с chat_id.
        Возвращает словарь с свойствами чата.
        Если чата с chat_id в базе нет, то возвращается пустой словарь {}
        """
        chat = {}
        chat_keys = ("chat_id", "chat_name", "read_time")
        if self.chat_exists(chat_id):
            cmd = "SELECT * FROM chats WHERE chat_id = ?"
            self.lock.acquire()
            self.cursor.execute(cmd, (chat_id,))
            chat_data = self.cursor.fetchone()[1:]
            self.lock.release()
            chat = dict(zip(chat_keys, chat_data))
        return chat

    def set_chat_readed(self, chat_id):
        """
        Обновляет время прочтения чата.
        Если чата с chat_id нет в БД, генерируется исключение ClientDBError
        """
        if not self.chat_exists(chat_id):
            raise ClientDBError("нельзя обновить время для неизвестного чата")
        cmd = "UPDATE chats SET read_time = ? WHERE chat_id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (time.time(), chat_id))
        self.conn.commit()
        self.lock.release()
        self._notify()

    def del_chat(self, chat_id):
        """
        Удаляет чат с chat_id из БД.
        """
        cmd = "DELETE FROM chats WHERE chat_id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_id,))
        self.conn.commit()
        self.lock.release()
        self._notify()

    def get_chats(self):
        """
        Возвращает список chat_id чатов.
        """
        cmd = "SELECT chat_id FROM chats"
        self.lock.acquire()
        self.cursor.execute(cmd)
        chats = [i[0] for i in self.cursor.fetchall()]
        self.lock.release()
        return chats

    ############################################################################
    def msg_exists(self, msg_id):
        """
        Проверяет наличие сообщения в БД.
        """
        cmd = "SELECT 1 FROM messages WHERE msg_id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (msg_id,))
        result = self.cursor.fetchone()
        self.lock.release()
        return bool(result)

    def add_msg(self, msg_id, user_id, chat_id, timestamp, message, action=None):
        """
        Добавить сообщение в БД.
        """
        if action and action != "msg":
            raise ClientDBError
        if self.msg_exists(msg_id):
            return
        cmd = "INSERT INTO messages(msg_id, user_id, chat_id, time, message)" \
            "VALUES (?, ?, ?, ?, ?)"
        self.lock.acquire()
        self.cursor.execute(
            cmd, (msg_id, user_id, chat_id, timestamp, message))
        self.conn.commit()
        self.lock.release()
        self._notify()

    def get_msg(self, msg_id):
        """
        Получить сообщение из БД.
        """
        msg = {}
        msg_keys = ("msg_id", "user_id", "chat_id",
                    "timestamp", "message", "readed")
        if self.msg_exists(msg_id):
            cmd = "SELECT * FROM messages WHERE msg_id = ?"
            self.lock.acquire()
            self.cursor.execute(cmd, (msg_id,))
            msg_data = self.cursor.fetchone()[1:]
            self.lock.release()
            msg = dict(zip(msg_keys, msg_data))
        return msg

    def set_msg_readed(self, msg_id):
        """
        Пометить сообщение как прочтенное.
        """
        if self.msg_exists(msg_id):
            cmd = "UPDATE messages SET readed = ?"
            self.lock.acquire()
            self.cursor.execute(cmd, (1,))
            self.conn.commit()
            self.lock.release()
            self._notify()

    def get_msgs(self, chat_id):
        """
        Получить список id сообщений для чата.
        """
        cmd = "SELECT msg_id FROM messages WHERE chat_id = ?"
        self.lock.acquire()
        self.cursor.execute(cmd, (chat_id,))
        msgs = [i[0] for i in self.cursor.fetchall()]
        self.lock.release()
        return msgs

    ############################################################################

    def add_observer(self, observer):
        self._observers.append(observer)

    def del_observer(self, observer):
        self._observers.remove(observer)

    def _notify(self):
        # print("notified")
        for observer in self._observers:
            observer.model_is_changed()

    def close(self):
        """ Закрываем соединение с БД """
        if self.conn:
            self.conn.close()
            self.conn = None
