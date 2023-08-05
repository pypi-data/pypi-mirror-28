""" server.py """
import socketserver


###############################################################################
# Server
###############################################################################
class Server(socketserver.ThreadingTCPServer):
    """ class Server """
    clients = {}
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass,
                 base, bind_and_activate=True):
        socketserver.ThreadingTCPServer.__init__(
            self, server_address, RequestHandlerClass, bind_and_activate)
        self.base = base

    def get_request(self):
        """ Получаем запрос """
        request, client_address = self.socket.accept()
        self.clients[request] = None
        print("get_request")
        return request, client_address

    def verify_request(self, request, client_address):
        """
        Проверяем запрос
        Return True if we should proceed with this request
        """
        print("verify_request", request, client_address)
        return True

    def close_request(self, request):
        print("close_request")
        self.clients.pop(request, None)
        request.close()
