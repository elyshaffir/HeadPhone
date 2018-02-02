import threading, socket

IP = '89.138.138.201'
PORT = 8081


class recve(threading.Thread):
    def run(self):
        recver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recver_socket.bind((IP, PORT))
        recver_socket.listen(1)
        r_socket, client_address = recver_socket.accept()
        while True:
            recvv = '-'
            while recvv != '':
                recvv += r_socket.recv(1)
            print recvv


class sender(threading.Thread):
    def run(self):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_socket.connect((IP, PORT))
        while True:
            sender_socket.send(raw_input())