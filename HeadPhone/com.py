import threading, socket

OTHER_IP = '127.0.0.1'
OTHER_PORT_RECV = 8080  # When testing with 2 machines, the other machine should flip the ports when using.
OTHER_PORT_SEND = 8081


class Recv(threading.Thread):
    def run(self):
        recver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recver_socket.bind(('', OTHER_PORT_RECV))
        recver_socket.listen(1)
        r_socket, client_address = recver_socket.accept()
        print threading.current_thread().getName()
        print r_socket.recv(1)


class Sender(threading.Thread):
    def run(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.connect((OTHER_IP, OTHER_PORT_SEND))
        sender_socket.send(raw_input())
        print threading.current_thread().getName()