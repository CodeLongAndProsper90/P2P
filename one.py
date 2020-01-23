import socket
import tqdm
import os
import sys
import hashlib
from hurry.filesize import size
import pyfiglet
from cryptography.fernet import Fernet
def warn_md5():
  print(f"Warning! MD5s do not match! {sent_hash}/{new_hash}")
  print("This means that either the transfer went wrong, or the file ")
  keep = input("Has been incerpeted by attackers, and is compromised. Keep file? (y/N)? ")
  if keep.lower() == 'n':
    os.remove(filename)

modes = ['transmit', 'receive','whomadethis?']
if len(sys.argv) == 1:
  print("Usage: transmit (ip-to-transmit-to) (file-to-transmit)")
  sys.exit()
if sys.argv[1] not in modes:
  print(f"Invalid mode {sys.argv[1]} (Transmit/Receive)")
  sys.exit()

if sys.argv[1] == 'transmit':
  if not len(sys.argv) == 4:
    print("Usage: transmit (ip-to-transmit-to) (file-to-transmit)")
    sys.exit()
if sys.argv[1] == 'download':
  if not len(sys.argv) == 2:
    print('Usage: download')
if sys.argv[1] == 'whomadethis?':
   print(pyfiglet.figlet_format("A Programmer"))
   sys.exit()
if sys.argv[1] == 'transmit':
  default_key = '5LabvIZ3MFAxk0IgJnTjwyHbWXVZdoPQcEzLeLL9IHE='.encode()
  f = Fernet(default_key)
  
  SEP = "<SEP>"
  BUFFER_SIZE = 4096
  port = 9001
  host = sys.argv[2]
  filename = sys.argv[3]
  if host == 'magic@narnia' and filename == 'unicorns':
    print("ERROR: Cannot transfer unicorns: missing dependency: Magic")
    sys.exit()
  filesize = os.path.getsize(filename)
  s = socket.socket()


  print(f"[*] Connecting to {host}:{port}...")
  s.connect((host, port))
  print(f"[*] Connected to {host}!")
  Hash = hashlib.md5(open(filename,'rb').read()).hexdigest()
  print(Hash)
  dat = f'{filename}{SEP}{filesize}{SEP}{Hash}'
  # while len(dat.encode()) < 4096:
    # dat = dat+'0'
  data = f.encrypt(dat.encode())
  s.send(data.encode())
  

  progress = tqdm.tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)
  with open(filename, "rb") as fi:
    for _ in progress:
      bytes_read = fi.read(BUFFER_SIZE)
      byte_size = len(bytes_read)
      bytes_read = f.encrypt(bytes_read)
      if not bytes_read:
        break
      s.sendall(bytes_read)
      progress.update(byte_size)
  s.close()



elif sys.argv[1] == 'receive':
  global sent_hash
  default_key = '5LabvIZ3MFAxk0IgJnTjwyHbWXVZdoPQcEzLeLL9IHE='.encode()
  f = Fernet(default_key)
  print(f.encrypt("hello WORLD".encode()))
  SERVER_HOST = '0.0.0.0'
  SERVER_PORT = 9001
  BUFFER_SIZE = 4096
  SEP = "<SEP>"
  s = socket.socket()

  s.bind((SERVER_HOST, SERVER_PORT))
  s.listen(5)

  print(f"[+] Listening as {SERVER_HOST}:{SERVER_PORT}")
  client_socket, address = s.accept()
  print(f"([*] Connection established!")


  received = f.decrypt(client_socket.recv(BUFFER_SIZE)).decode()
  print(f"Received {len(received.encode())} bytes")
  raw = received.split(SEP)
  print(raw)
  while '' in raw:
    raw.remove('')
  print(len(raw))
  filename = [0]
  filesize = raw[1]
  sent_hash = raw[2]
  f = Fernet(raw[3])
  filename = filename.replace('0','')

  filename = os.path.basename(filename)
  saveas = filename
  filesize = int(filesize)
  if filesize >= 524288000:
    v = input(f'{filename} seems to be a large file. ({size(filesize)}) Download? [Y/n]')
    if v.lower() == 'n':
      print("User abort!")
      sys.exit()


  progress = tqdm.tqdm(range(filesize), f"Downloading file {filename}", unit="B", unit_scale=True, unit_divisor=1024)
  saveas =os.path.abspath(os.getcwd() +'/' +  saveas)
  print(saveas)
  with open(saveas, "wb") as f:
    for _ in progress:
      bytes_read = f.decrypt(client_socket.recv(BUFFER_SIZE))
      if not bytes_read:
        break
      f.write(bytes_read)
      progress.update(len(bytes_read))
  client_socket.close()
  s.close()
  progress.close()
  del f
new_hash = hashlib.md5(open(filename,'rb').read()).hexdigest()
if not new_hash == sent_hash:
  warn_md5()

