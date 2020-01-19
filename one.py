# Sound made by Alexander, on http://www.orangefreesounds.com/
import socket
import tqdm
import os
import sys
from playsound import playsound as play
import hashlib
modes = ['transmit', 'download']
if sys.argv[1] not in modes:
  print("Invalid mode")
  exit()

if sys.argv[1] == 'transmit':
  if not len(sys.argv) == 4:
    print("Usage: (transmit/download) (ip-to-transmit-to) (file-to-transmit)")
    exit()

if sys.argv[1] == 'transmit':
  SEP = "<SEP>"
  BUFFER_SIZE = 4096
  port = 9001
  host = sys.argv[2]
  filename = sys.argv[3]
  filesize = os.path.getsize(filename)

  s = socket.socket()


  print(f"[*] Connecting to {host}:{port}...")
  s.connect((host, port))
  print(f"[*] Connected to {host}!")
  play('connect.wav')
  Hash = hashlib.md5(open(filename,'rb').read()).hexdigest()
  print(Hash)
  dat = f'{filename}{SEP}{filesize}{SEP}{Hash}'
  while len(dat.encode()) < 4096:
    dat = '0'+dat
  data = dat
  print(data)
  print(len(data.encode()))
  s.send(data.encode())
  

  progress = tqdm.tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)

  with open(filename, "rb") as f:
    for _ in progress:
      bytes_read = f.read(BUFFER_SIZE)
      if not bytes_read:
        break
      s.sendall(bytes_read)
      progress.update(len(bytes_read))
  s.close()
elif sys.argv[1] == 'download':

  SERVER_HOST = '0.0.0.0'
  SERVER_PORT = 9001
  BUFFER_SIZE = 4096
  SEP = "<SEP>"
  s = socket.socket()

  s.bind((SERVER_HOST, SERVER_PORT))
  s.listen(5)

  print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
  client_socket, address = s.accept()
  play('connect.wav')
  print(f"([*] Connection established!")


  received = client_socket.recv(BUFFER_SIZE).decode()
  print(f"Received {len(received.encode())} bytes")
  raw = received.split(SEP)
  print(raw)
  while '' in raw:
    raw.remove('')
  filename = raw[0]
  filesize = raw[1]
  filename = filename.replace('0','')

  filename = os.path.basename(filename)
  saveas = filename
  filesize = int(filesize)

  progress = tqdm.tqdm(range(filesize), f"Downloading file {filename}", unit="B", unit_scale=True, unit_divisor=1024)
  with open(saveas, "wb") as f:
    for _ in progress:
      bytes_read = client_socket.recv(BUFFER_SIZE)
      if not bytes_read:
        break
      print(bytes_read)
      f.write(bytes_read)
      progress.update(len(bytes_read))
  client_socket.close()
  s.close()
