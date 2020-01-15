# server2.py
import socket
from threading import Thread
from socketserver import ThreadingMixIn
import os

TCP_IP = '192.168.1.85'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print(" New thread started for "+ip+":"+str(port))

    def size(self, path):
      return os.path.getsize(path)
    def run(self):
        filename=self.sock.recv(1024)
        filename = filename.decode("utf-8") 
        
        if filename.startswith("FILE:"):
          filename = filename.replace("FILE:",'',1)
        if not os.path.exists(filename):
          conn.send('STATUS:NFile'.encode('utf-8')) # Send the file status
          conn.close()
          return
        else:
          conn.send("STATUS:File".encode('utf-8'))
        print(f"Size of {filename} is {self.size(filename)}") 
        filesize = self.size(filename)
        conn.send(str(filesize).encode('utf-8')) # Send filesize
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                # l = f.read(BUFFER_SIZE)
            # if not l:
                # f.close()
                # self.sock.close()
                # break

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
