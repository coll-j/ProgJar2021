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

        msg = data.decode('utf-8')
        if '<' in msg:
            clear_line()
            print(msg)
            print("Pilih aksi [1: kirim pesan, 2: lihat daftar pengguna, 3: tambah teman, 4: exit]:")
        else:
            clear_line()
            print(msg)
def clear_line():
    sys.stdout.write("\033[F") #back to previous line 
    sys.stdout.write("\033[K") #clear line
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
    act = int(input("Pilih aksi [1: kirim pesan, 2: lihat daftar pengguna, 3: tambah teman, 4: exit]:\n"))
    clear_line()
    if act == 1:
        clear_line()
        # kirim/terima pesan
        dest = input("Masukkan username tujuan (ketikan bcast untuk broadcast pesan):")
        clear_line()
        msg = input("Masukkan pesan untuk {}:".format(dest))
        clear_line()
        data = [username, dest, msg]

        print("<{}>: {}".format(username, msg))
        sock_cli.send(bytes('|'.join(data), 'utf-8'))
    if act == 2:
        # lihat daftar pengguna
        # clear_line()
        sock_cli.send(bytes('get_user', 'utf-8'))
    if act == 3:
        # tambah teman
        clear_line()
        dest = input("Masukkan username yang ingin ditambahkan:")
        # clear_line()
        
        data = "add|{}|{}".format(username, dest)
        sock_cli.send(bytes(data, 'utf-8'))
    if act == 4:
        sock_cli.close()
        break
