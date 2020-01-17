import socket
import tqdm
import os
import sys
def ensure_args():
  if len(sys.argv) < 3:
    print("Usage: python3 client.py (ip_to_send_to) (file_to_send)")
ensure_args()

<<<<<<< HEAD
SEP = "<SEP>"
BUFFER_SIZE = 4096
host = '192.168.1.20'
port = 9001
filename = 'test'
filesize = os.path.getsize(filename)
=======
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9001
BUFFER_SIZE = 4096
<<<<<<< HEAD
host = sys.argv[1]
port = 9001
filename = sys.argv[2]
filesize = os.path.getsize(filename)

=======
SEP = "<SEP>"
saveas = 'test.img.trans'
>>>>>>> 642e413a62f170930a0620193a825e8544dc2735
s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
>>>>>>> d335da56a43165ed560da016454308e41a69423c

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

