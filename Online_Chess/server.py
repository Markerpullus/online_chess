import socket, select
from imports.ip import server_ip, server_port

IP = server_ip
PORT = server_port
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
print('Listening for connections on {}: {}'.format(IP, PORT))
server_socket.listen()

sockets_list = []
clients = {}

def receive_message(client_socket):
    try:
        msg = client_socket.recv(32)
        if not len(msg):
            return False
        return msg.decode()

    except:
        return False

def start():
    print('Both players connected, starting game now')
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            message = receive_message(notified_socket)
            user = clients[notified_socket]
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            type = message.split('|')[0]
            fromx, fromy = message.split('|')[1:3]
            tox, toy = message.split('|')[3:]
            print(f'{user} moved {type} from ({fromx}, {fromy}) to ({tox}, {toy})')
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(message.encode())
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

while True:
    client_socket, client_address = server_socket.accept()
    user = receive_message(client_socket)

    sockets_list.append(client_socket)
    clients[client_socket] = user

    print('{} connected from {}:{}'.format(user, *client_address))

    if len(clients) == 2:
        for socket in sockets_list:
            socket.send('!'.encode())
        start()
        break
