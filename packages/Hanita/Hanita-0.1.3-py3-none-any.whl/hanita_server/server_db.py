from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from .models import Chat, ChatMsg, ChatUser, Contact, User
from pymongo import MongoClient


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


###############################################################################
# ### ServerDBError
###############################################################################
class ServerDBError(Exception):
    """ Класс-исключение для ServerDB """
    pass


###############################################################################
# ### class ServerDB
###############################################################################
class ServerDB:
    """ Класс для управления БД сервера

    """

    def __init__(self, base, dbname=""):
        if not dbname:
            dbname = "sqlite:///:memory:"
        self.engine = create_engine(
            dbname, echo=False, connect_args={
                "check_same_thread": False
            })
        self.base = base
        self.session = None
        self.mng_client = MongoClient()
        self.mng_db = self.mng_client.main_db
        try:
            self.setup()
        except Exception as err:
            print(str(err))
            self.close()

    def add_obj(self, obj, error_msg="add_obj error"):
        """ Добавить в базу """
        try:
            self.session.add(obj)
            self.session.commit()
        except:
            self.session.rollback()
            raise ServerDBError(error_msg)

    def get_obj(self, cls, obj_id):
        """ Получить объект класса cls из базы.
        Если объекта с obj_id в базе не существует, возвращается None.
        """
        obj = self.session.query(cls).filter(cls.id == obj_id).first()
        return obj

    def del_obj(self, cls, obj_id, error_msg="del_obj error"):
        """ Удалить из базы.
        Ничего из базы не удаляется. Меняется только статус с active на deleted
        """
        obj = self.session.query(cls) \
            .filter(cls.id == obj_id) \
            .first()
        if cls == Chat and self.get_users_for(obj.id):
            raise ServerDBError(
                "Попытка удалить чат с активными пользователями")
        try:
            obj.status = "deleted"
            self.session.commit()
        except:
            self.session.rollback()
            raise ServerDBError(error_msg)

    def obj_exists(self, cls, obj_id):
        """ Проверить наличие в базе """
        q = self.session.query(cls).filter(cls.id == obj_id)
        return self.session.query(q.exists()).scalar()

    def add_new_user(self, login):
        """ Добавить нового пользователя """
        if self.get_user_id(login):
            raise ServerDBError("login уже занят")
        user = User(login)
        self.add_obj(user)
        return user

    def add_contact(self, user_id, contact_id):
        """ Добавить контакт. """
        contact = Contact(user_id, contact_id)
        self.add_obj(contact)

    def set_user_status(self, user_id, status):
        """ Установить статус для пользователя """
        user = self.session.query(User) \
            .filter(User.id == user_id).first()
        user.status = status
        self.session.commit()

    def set_user_online(self, user_id, online, fileno=None):
        """ Установить статус для пользователя """
        user = self.session.query(User) \
            .filter(User.id == user_id).first()
        user.online = online
        user.fileno = fileno
        self.session.commit()

    def get_user_id(self, user_login):
        """ Получить  user_id по логину. Если логина нет в базе,
        возвращается None.
        """
        user = self.session.query(User) \
            .filter(User.login == user_login) \
            .first()
        return user.id if user else None

    def get_users_for(self, chat_id, status=None):
        """
        Получить список всех активных пользователей чата.
        Возвращает список объектов класса User. Если chat_id не существует,
        возвращается пустой список.
         """
        status = status or "active"
        user_list = self.session.query(User) \
            .join(ChatUser) \
            .filter(ChatUser.chat_id == chat_id) \
            .filter(ChatUser.status == "active") \
            .filter(User.status == status).all()
        return user_list

    def get_online_users(self, chat_id):
        """
        Получить список пользователей чата, находящихся онлайн.
        Возвращает список объектов класса User. Если chat_id не существует,
        возвращается пустой список.
        """
        user_list = self.session.query(User) \
            .join(ChatUser) \
            .filter(ChatUser.chat_id == chat_id) \
            .filter(ChatUser.status == "active") \
            .filter(User.status == "active") \
            .filter(User.online == 1).all()
        return user_list

    def add_new_chat(self, chat_name):
        """ Добавить новый чат. """
        chat = Chat(chat_name)
        self.add_obj(chat)
        return chat

    def get_chat(self, chat_id):
        """ Возвращает объект Chat по данномы chat_id """
        return self.get_obj(Chat, chat_id)

    def get_chats_for(self, user_id):
        """
        Получить список всех активных чатов для данного пользователя.
        Возвращает список объектов класса Chat. Если user_id не существует,
        возвращается пустой список.
        """
        chat_list = self.session.query(Chat) \
            .join(ChatUser) \
            .filter(ChatUser.user_id == user_id) \
            .filter(ChatUser.status == "active").all()
        return chat_list

    def add_user_to_chat(self, chat_id, user_id):
        """ Добавить пользователя в чат """
        chatuser = ChatUser(chat_id, user_id)
        self.add_obj(chatuser)

    def del_user_from_chat(self, chat_id, user_id):
        """ Удалить пользователя из чата """
        chatuser = self.session.query(ChatUser) \
            .filter(ChatUser.chat_id == chat_id) \
            .filter(ChatUser.user_id == user_id) \
            .first()
        if chatuser:
            self.del_obj(ChatUser, chatuser.id)

    def find_users(self, substr):
        """
        Найти всех пользователей по строке поиска.
        Возвращает список объектов класса User.
        """
        users = self.session.query(User) \
            .filter(User.name.like('%{}%'.format(substr))) \
            .all()
        return users

    def get_contacts_for(self, user_id):
        """
        Получить список контактов пользователя
        Возвращает список объектов класса User. Если user_id не существует,
        или имеет статус 'deleted', генерируется исключение ServerDBError
        """
        user = self.get_obj(User, user_id)
        if user is None:
            raise ServerDBError(
                "попытка получить контакты для несуществующего пользователя")
        if user.status == "deleted":
            raise ServerDBError(
                "нельзя получить контакты для удаленного пользователя")

        contacts = self.session.query(User) \
            .join(Contact, User.id == Contact.contact_id) \
            .filter(Contact.user_id == user_id) \
            .filter(Contact.status == "active") \
            .all()
        return contacts

    def del_contact(self, user_id, contact_id):
        """
        Удалить пользователя с contact_id из списка контактов для user_id.
        """
        contact = self.session.query(Contact) \
            .filter(Contact.user_id == user_id) \
            .filter(Contact.contact_id == contact_id) \
            .first()
        self.del_obj(Contact, contact.id)

    def add_chat_msg(self, msg):
        """ Сохранить сообщение в БД """
        self.mng_db.messages.insert_one(msg)

    def get_chat_msgs(self, chat_id):
        """
        Получить сообщения для чата.
        Возвращает список объектов типа JIMClientMessage, где action = 'msg'.
        Если чата с chat_id не существует или он имеет статус 'deleted',
        генерируется исключение ServerDBError.
        """
        chat = self.get_obj(Chat, chat_id)
        if chat is None or chat.status == "deleted":
            raise ServerDBError(
                "Нельзя получить сообщения для несуществующего/удаленного чата"
            )
        msgs = self.mng_db.messages.find({"chat_id": chat_id})
        return list(msgs)

    def setup(self):
        """ Загрузка БД """
        self.base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.commit()

    def close(self):
        """ Закрытие БД """
        print("DB close")
        if self.session:
            self.session.close()
            self.session = None
