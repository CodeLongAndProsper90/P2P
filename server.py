import socket
import tqdm 
import os

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9001
BUFFER_SIZE = 4096
SEP = "<SEP>"
s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
client_socket, address = s.accept()


received = client_socket.recv(BUFFER_SIZE).decode()
print(received)
filename, filesize = received.split(SEP)
filename = os.path.basename(filename)
saveas = filename
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
