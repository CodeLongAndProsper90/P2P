import socket
import tqdm
import os
import sys
def ensure_args():
  if len(sys.argv) < 3:
    print("Usage: python3 client.py (ip_to_send_to) (file_to_send)")
ensure_args()

SEP = "<SEP>"
BUFFER_SIZE = 4096
port = 9001
host = sys.argv[1]
filename = sys.argv[2]
filesize = os.path.getsize(filename)

s = socket.socket()

s.listen(5)

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

