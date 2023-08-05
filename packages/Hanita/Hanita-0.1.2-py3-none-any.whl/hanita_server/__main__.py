import argparse
import sys

from . import Base, ClientRequestHandler, Server


###############################################################################
# read_args
###############################################################################
def read_args():
    """ Читаем аргументы командной строки """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        dest="addr",
        default="127.0.0.1",
        help="IP-адрес для прослушивания"
    )
    parser.add_argument(
        "-p",
        dest="port",
        type=int,
        default=7777,
        help="TCP-порт (по умолчанию 7777)"
    )

    args = parser.parse_args()
    return args


###############################################################################
# main
###############################################################################
def main():
    """ mainloop """
    args = read_args()

    with Server((args.addr, args.port), ClientRequestHandler, Base) as server:
        server_addr = server.socket.getsockname()
        serve_message = "Serving on {host} port {port} ..."
        print(serve_message.format(host=server_addr[0], port=server_addr[1]))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

    print("\nKeyboard interrupt received, exiting.")
    sys.exit(0)


###############################################################################
#
###############################################################################
if __name__ == "__main__":
    main()
