import socket
import select
import sys

#appeler le program avec des arguments le nom du host = localhost et le port
if len(sys.argv) < 3:
    print("Usage : python {0} hostname port".format(sys.argv[0]))
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

master_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
master_sock.settimeout(200) 

# connexion
try:
    master_sock.connect((host, port))
except Exception as msg:
    print(type(msg).__name__)
    print("Connexion impossible")
    sys.exit()

print("Connexion reussie! Vous pouvez chattez!")

while True:
    SOCKET_LIST = [sys.stdin, master_sock]
    # choisir les sockets disponibles
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(SOCKET_LIST, [], [])

    for sock in READ_SOCKETS: #
        if sock == master_sock:
            data = sock.recv(4096)
            if not data:
                print('\nDeconnecte du server ')
                sys.exit()
            else: #afficher le message
                print(data.decode())
                print(end)
                print('')
        else: 
            msg = sys.stdin.readline()
            master_sock.sendall(msg.encode()) #encoder le message python v3