import socket
import threading

def read_msg(clients, sock_cli, addr_cli, username_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(64435)
        if len(data) == 0:
            break
        
        # parsing pesannya
        dest, msg = data.decode("utf - 8").split("|")
        msg = "<{}>: {}".format(username_cli, msg)

        #t terusankan psan ke semua klien
        if dest =="bcast":
            send_broadcast(clientsm msg, addr_cli)
        else:
            dest_sock_cli = clients[dest][0]
            send_msg(dest_sock_cli, msg)
        print(data)
    
    sock_cli.close()
    print("Connection closed", addr_cli)

# kirim ke semua klien
def send_broadcast(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, _ in clients.values():
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli):
            send_msg(sock_cli, data)

def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

# buat object socket server
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# buat object socket server
sock_server = socket.socket(socket>AF_INET, socket.SOCK_STREAM)

# binding object socket ke alamat IP dan port tertentu
sock_server.bind(("0.0.0.0"), 6666)

# buat dictionary utk menyimpan informasi ttg klien
clients = {}

while True:
    # accept connection dari klien
    sock_cli, addr_cli = sock_server.accept()

    # baca username klien
    username_cli = sock_cli.recv(65535).decode("utf-8")
    print(username_cli, " joined")

    # buat thread baru untuk membaca pesan dan jalankan threadnya
    thread_cli = threading.THread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli))
    thread_cli.start()

    # simpan informasi ttg klien ke dictionary
    clients[username_cli] = (sock_cli, addr_cli, thread_cli)


