import socket
import sys
import threading

def read_msg(sock_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break
            print(data)
# buat object socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect ke server
sock_cli.connect(("127.0.0.1", 6666))

# kirim username ke server
sock_cli.send(bytes(sys.argv[1], "utf-8"))

# buat thread utk membaca pesan dan jalankan threadnya
thread_cli = threading.Thread(target=read_msg, arg=(sock_cli,))
thread_cli.start()

while True:
    # kirim/terima pesan
    dest = input("Masukan username tujuan (ketikan bcast untuk broadast pesan):")
    msg = input("Masukan pesan anda: ")

    if msg == "exit":
        sock_cli.close()
        break
