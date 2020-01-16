# client2.py
#!/usr/bin/env python

import socket
import sys
import time
import threading
from hurry.filesize import size as Size
import os
import ast
TCP_IP = '192.168.1.20'
TCP_PORT = 9001
BUFFER_SIZE = 1024
data = 0
if len(sys.argv) < 2:
  print("Missing operand")
  exit()
filename = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("Connected!")
s.send(f"FILE:{filename}".encode('utf-8'))
print("Reqesting file...")

if len(sys.argv) < 3:
  saveas = sys.argv[1]
else:
  saveas = sys.argv[2]
exists = s.recv(BUFFER_SIZE).decode('utf-8')
if exists.startswith("STATUS:"):
    exists = exists.replace("STATUS:","",1)
    print(exists)
    if exists.startswith('NFile'):
      print(f'{sys.argv[1]}: No such file or directory')
      exit(1)
    else:
      print(f"File {filename} exists...")
size = s.recv(BUFFER_SIZE).decode('utf-8')
print(size.split('#0'))
if size.startswith("SIZE:"):
    size = size.replace("SIZE:","",1)
    size = size.split('#0')
    data = size
    size = size[0]
print(f"Size of file is {Size(int(size))}")
byte = 0
print("Processing data...")
for item in data:
    print("Item is :" + item)
    if item.startswith("DATA:"):
        write = item.replace('DATA:','',1)
        print("New version: " + write)
#        write = write.decode('utf-8')
        print(write)
        write = ast.literal_eval(write)
        break
try:
  with open(saveas, 'wb') as f:
      while True:
          if type(write) is not bytes:
            write = s.recv(BUFFER_SIZE)
            print(write)
          if not write:
              f.close()
              break
          # write data to a file
          f.write(write)
          byte+=BUFFER_SIZE
          if byte < int(size):
              f.close()
              break
          
          input()
          print(f"Downloaded {Size(byte)} of {Size(int(size))}",end='\r')
          write = None 
except KeyboardInterrupt or EOFError:
#  os.remove(filename)
    print()
print('Successfully got the file')
s.close()
print('connection closed')
with open(saveas, 'r') as f:
    print(f.read())
