# client2.py
#!/usr/bin/env python

import socket
import sys
import time
import threading
from hurry.filesize import size as Size
import os
TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
if len(sys.argv) < 2:
  print("Missing operand")
  exit()
filename = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(filename.encode('utf-8'))
if len(sys.argv) < 3:
  saveas = sys.argv[1]
else:
  saveas = sys.argv[2]
exists = s.recv(BUFFER_SIZE).decode('utf-8')
if exists == 'NFile':
  print(f'{sys.argv[1]}: No such file or directory')
  exit(1)
else:
  print(f"File {filename} exists...")
size = int(s.recv(BUFFER_SIZE).decode('utf-8'))
print(f"Size of file is {Size(size)}")
byte = 0
try:
  with open(saveas, 'wb') as f:
      while True:
          data = s.recv(BUFFER_SIZE)
          if not data:
              f.close()
              break
          # write data to a file
          f.write(data)
          byte+=BUFFER_SIZE
          print(f"Downloaded {Size(byte)} of {Size(size)}",end='\r')
except KeyboardInterrupt or EOFError:
  os.remove(filename)
print()
print('Successfully got the file')
s.close()
print('connection closed')
