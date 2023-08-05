import argparse

from .client import QtClient
from .client_connection import ClientConnection
from .client_qtview import QtClientView


###############################################################################
# read_args
###############################################################################
def read_args():
    """
    Получаем аргументы командной строки.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "addr",
        default="127.0.0.1",
        nargs="?",
        help="IP сервера (по умолчанию 127.0.0.1)")
    parser.add_argument(
        "port",
        type=int,
        default=7777,
        nargs="?",
        help="TCP-порт сервера (по умолчанию 7777)")

    args = parser.parse_args()

    return args


###############################################################################
# main
###############################################################################
def main():
    """ Точка входа """
    args = read_args()

    connection = ClientConnection(args.addr, args.port)

    client = QtClient(connection, QtClientView)
    client.run()

    client.close("Good Bye!")


###############################################################################
if __name__ == "__main__":
    main()
