import socket
import tqdm
import os

SEP = "<SEP>"
BUFFER_SIZE = 4096
host = '192.168.1.20'
port = 9001
filename = 'test'
filesize = os.path.getsize(filename)

s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected")

s.send(f'{filename}{SEP}{filesize}'.encode())

progress = tqdm.tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)

with open(filename, "rb") as f:
  for _ in progress:
    bytes_read = f.read(BUFFER_SIZE)
    if not bytes_read:
      break
    s.sendall(bytes_read)
    progress.update(len(bytes_read))
s.close()

