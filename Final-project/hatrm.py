import tkinter
import sys
import threading
import socket
import os
from PIL import ImageTk,Image 

def recv_msg_hatrm(c, window):
    rowpos = 3 
    while True :
        msg = c.recv(32768).decode('utf-8')
        if not msg :
            sys.exit(0)
        if msg == "msg":
            msg=c.recv(32768).decode('utf')
            msglbl = tkinter.Label(window,text=msg)
            msglbl['font']=("Courier",10)
            msglbl['bg']='black'
            msglbl['fg']='#0aff43'
            msglbl['width']=50
            msglbl.grid(columnspan=2,column=0,row=rowpos,padx=5)
            rowpos += 1
        elif msg == "img":
            # msg=c.recv(32768).decode('utf')
            # msglbl = tkinter.Label(window,text=msg)
            # msglbl['font']=("Courier",10)
            # msglbl['bg']='black'
            # msglbl['fg']='#0aff43'
            # msglbl['width']=50
            # msglbl.grid(columnspan=2,column=0,row=rowpos,padx=5)
            # rowpos += 1
            msg=c.recv(32768).decode('utf')

            client_recieve_file(c, msg)

            # msg=c.recv(32768).decode('utf')

            img = ImageTk.PhotoImage(Image.open(msg)) 
            msglbl = tkinter.Label(window,image=img)
            msglbl.grid(columnspan=2,column=0,row=rowpos)
            rowpos += 1


def client_recieve_file(client_socket,filename):
    size = client_socket.recv(32768)
    size = size.decode('utf-8')
    size = int(float(size))
    size += 1
    file = open(filename, 'wb')
    while size> 0:
        data = client_socket.recv(32768)
        file.write(data)
        size -= 1
    file.close()

def client_send_file(client_socket,filename):
    file = open(filename)
    file.seek(0, os.SEEK_END)
    filesize =str(file.tell()/32768)
    client_socket.send(bytes(filesize, "utf-8"))
    file.close()

    file = open(filename,'rb')
    while True:
        data = file.read(32768)
        if not data:
            break
        client_socket.send(data)
    file.close()

def send_msg (sock_cli, txtchat, username):
    msg = "msg"
    sock_cli.send(bytes(msg, "utf-8"))
    msg = username +" : " + txtchat.get()
    sock_cli.send(bytes(msg, "utf-8"))
    # sock_cli.send(msg.encode('ascii'))
    
def send_img (sock_cli, txtchat, username):
    if(os.path.isfile(txtchat.get())):
        msg = "img"
        sock_cli.send(bytes(msg, "utf-8"))

        # msg = username +" : " + txtchat.get()
        # sock_cli.send(bytes(msg, "utf-8"))

        msg = txtchat.get()
        sock_cli.send(bytes(msg, "utf-8"))

        msg = txtchat.get()
        client_send_file(sock_cli,msg)

def windows_start(username):
    # buat object socket
    sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect ke server
    sock_cli.connect(("127.0.0.1", 6669))

    #Creating a window
    window = tkinter.Tk()
    window.title('Chatbox')
    window['bg']='#242424'
    window['padx']=10
    window['pady']=10
    #Adding Elements
    #Entry
    txtchat = tkinter.Entry(window)
    txtchat['width']=50
    txtchat['relief']=tkinter.GROOVE
    txtchat['bg']='#f5f6f7'
    txtchat['fg']='red'
    txtchat['font']=("Courier",12)
    txtchat.grid(column=0,row=1,padx=5,pady=15)

    #Button
    sendchat = tkinter.Button(window,text="send chat")
    sendchat['relief']=tkinter.GROOVE
    sendchat['bg']='red'
    sendchat['fg']='white'
    sendchat['activebackground']='#404040'
    sendchat['font']=("Courier",10)
    sendchat.grid(column=1,row=1,padx=5,pady=15)
    sendchat['command'] = lambda: send_msg(sock_cli, txtchat, username)

    sendimg = tkinter.Button(window,text="send img")
    sendimg['relief']=tkinter.GROOVE
    sendimg['bg']='red'
    sendimg['fg']='white'
    sendimg['activebackground']='#404040'
    sendimg['font']=("Courier",10)
    sendimg.grid(column=2,row=1,padx=5,pady=15)
    sendimg['command'] = lambda: send_img(sock_cli, txtchat, username)

    thread_hatrm = threading.Thread(target=recv_msg_hatrm, args=(sock_cli,window))
    thread_hatrm.start()

    window.mainloop()    