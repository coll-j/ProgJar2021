import socket
import re

def getResponseLine(response):
    try:
        # line = response[0]
        res = re.findall(r'([A-Z]+/[0-9\.]+) ([0-9]+) ([A-Za-z ]*)', response)
        return res[0]
    except:
        return None

def getWebServer(response):
    try:
        res = re.findall(r'Server: (.*)\n', response)
        return res[0]
    except:
        return None

def getHTTPVersion(response):
    try:
        res = getResponseLine(response)
        return res[0]
    except:
        return None

def getContentType(response):
    try:
        res = re.findall(r'Content-Type: (.*);', response)
        return res[0]
    except:
        return None

def getPageTitle(response):
    try:
        res = re.findall(r'<title>(.*)</title>', response)
        return res[0]
    except:
        return None


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
page_url = 'classroom.its.ac.id'
server_address = (page_url, 80)
client_socket.connect(server_address)

request_header = 'GET / HTTP/1.0\r\nHost: {}\r\n\r\n'.format(page_url)
request_header = bytes(request_header, encoding='utf-8')
# print(request_header)
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8') + '\n'

print(response)
print(getResponseLine(response))
print(getWebServer(response))
print(getHTTPVersion(response))
print(getContentType(response))
print(getPageTitle(response))

client_socket.close()
