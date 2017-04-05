import socket
import select

def broadcast_data(message):
    #On envoye un message vers toutes les connexions
    for sock in liste_connexion:
        if sock != server_socket:
            try:
                sock.sendall(message) # envoye le message a tout le monde
            except Exception as msg: # cas d'erreur
                print(type(msg).__name__)
                sock.close()
                try:
                    liste_connexion.remove(sock)
                except ValueError as msg:
                    print('Erreur')

liste_connexion = []
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
PORT = 1337

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
print("En attendant")
server_socket.listen(10) # 10 connexions possibles

liste_connexion.append(server_socket)
print("Le serveur est demare ")

while True:
    # Get the list sockets which are ready to be read through select
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(liste_connexion, [], [])
    for SOCK in READ_SOCKETS: # New connection
        # Handle the case in which there is a new connection recieved through server_socket
        if SOCK == server_socket:
            SOCKFD, addr = server_socket.accept()
            liste_connexion.append(SOCKFD) # on ajoute la connexion dans la liste
            print("\rClient ({0}, {1}) connecte".format(addr[0], addr[1]))
            broadcast_data("Client ({0}:{1}) est actif\n"
                           .format(addr[0], addr[1]).encode())
        else: # le message de l utilisateur 
            try: # le message est recu et il est traite
                data = SOCK.recv(RECV_BUFFER)
                if data:
                    addr = SOCK.getpeername() # on prend l address du socket
                    
                    print(message)
                    print(end)
                    print(' ')
                    broadcast_data(message.encode())
            except Exception as msg: # client deconnecte
                print(type(msg).__name__, msg)
                print("\rClient ({0}, {1}) deconnecte.".format(addr[0], addr[1]))
                broadcast_data("\rClient ({0}, {1}) inactif\n"
                               .format(addr[0], addr[1]).encode())
                SOCK.close()
                try:
                    liste_connexion.remove(SOCK)
                except ValueError as msg:
                    print("{}:{}.".format(type(msg).__name__, msg))
                continue

server_socket.close()