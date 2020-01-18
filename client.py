import socket
import tqdm 
import os
import sys
def ensure_args():
  if len(sys.argv) < 3:
    print("Usage: python3 client.py (ip_to_send_to) (file_to_send)")
ensure_args()

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9001
BUFFER_SIZE = 4096
host = sys.argv[1]
port = 9001
filename = sys.argv[2]
filesize = os.path.getsize(filename)

SEP = "<SEP>"
saveas = 'test.img.trans'
s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()


received = client_socket.recv(BUFFER_SIZE).decode()
print(received)
filename, filesize = received.split(SEP)
filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Reciving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(saveas, "wb") as f:
  for _ in progress:
    bytes_read = client_socket.recv(BUFFER_SIZE)
    if not bytes_read:
      break
  f.write(bytes_read)
  progress.update(len(bytes_read))
client_socket.close()
s.close()
