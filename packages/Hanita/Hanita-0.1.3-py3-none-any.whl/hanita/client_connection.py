"""
Здесь собранны инструменты, отвечающие за связь клиента с сервером
"""
import json
import socket

from hanita_JIM import JIMMessage

BUFFERSIZE = 1024


###############################################################################
# ### ClientConnectionError
###############################################################################
class ClientConnectionError(Exception):
    """ Базовое исключение для ClientConnection """
    pass


###############################################################################
# ### ClientConnection
###############################################################################
class ClientConnection:
    """
    Класс устанавливает соединение с сервером, передает данные на сервер,
    получает ответ от сервера.
    """

    def __init__(self, host=None, port=7777, timeout=0.1):
        if host is None:
            host = "127.0.0.1"
        self.host = host
        self.port = port
        self.connection = None
        self.timeout = timeout

    def connect(self):
        """ Устанавливаем соединение с сервером """
        if self.connection:
            raise ClientConnectionError("Соединение уже установлено")
        try:
            self.connection = socket.create_connection((self.host, self.port),
                                                       timeout=self.timeout)
        except socket.error as err:
            raise ClientConnectionError(err)

    def send(self, message):
        """ Отправляет сообщение на сервер """
        if not isinstance(message, dict):
            raise ClientConnectionError("Неверный формат сообщения")

        json_msg = json.dumps(message)
        byte_msg = json_msg.encode()
        if self.connection:
            self.connection.sendall(byte_msg)

    def get(self):
        """ Получает сообщение от сервера.
        Возвращает массив сообщений или пустой массив.
        """
        if self.connection:
            byte_msg = b""
            out_msgs = []
            _get_data = True
            while _get_data:
                try:
                    data = self.connection.recv(BUFFERSIZE)
                except socket.timeout:
                    _get_data = False
                except OSError:
                    print("потеряна связь с сервером")
                    _get_data = False
                else:
                    # if not data or data.endswith(b"}"):
                    #     _get_data = False
                    byte_msg += data
            if byte_msg:
                msgs = byte_msg.decode().replace(
                    "}{", "}<split>{").split("<split>")
                for msg in msgs:
                    try:
                        json_msg = json.loads(msg)
                    except ValueError:
                        print("!!! отброшено !!!\n client get:", msg)
                    else:
                        jim = JIMMessage(json_msg)
                        out_msgs.append(jim)
            return out_msgs

    def close(self):
        """ Закрывает соединение с сервером """
        if self.connection:
            # self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            self.connection = None
