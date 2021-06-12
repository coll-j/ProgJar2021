import socket
import sys
import threading
import pickle

def read_msg(sock_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        sys.stdout.write("\033[F") #back to previous line 
        sys.stdout.write("\033[K") #clear line 
        print(data.decode('utf-8'))
        print("Masukkan username tujuan (ketikan bcast untuk broadcast pesan):")
# buat object socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect ke server
sock_cli.connect(("127.0.0.1", 6666))

# kirim username ke server
username = sys.argv[1]
sock_cli.send(bytes(username, "utf-8"))

# buat thread utk membaca pesan dan jalankan threadnya
thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

while True:
    # kirim/terima pesan
    dest = input("Masukkan username tujuan (ketikan bcast untuk broadcast pesan):\n")
    sys.stdout.write("\033[F") #back to previous line 
    sys.stdout.write("\033[K") #clear line
    sys.stdout.write("\033[F") #back to previous line 
    sys.stdout.write("\033[K") #clear line 
    msg = input("Masukkan pesan untuk {}:\n".format(dest))
    sys.stdout.write("\033[F") #back to previous line 
    sys.stdout.write("\033[K") #clear line
    sys.stdout.write("\033[F") #back to previous line 
    sys.stdout.write("\033[K") #clear line
    data = [dest, msg]

    if msg == "exit":
        sock_cli.close()
        break

    print("<{}>: {}".format(username, msg))
    sock_cli.send(bytes('|'.join(data), 'utf-8'))
