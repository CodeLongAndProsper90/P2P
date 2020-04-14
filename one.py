import argparse
import sys
parser = argparse.ArgumentParser(description='Send files without connecting to a server')
parser.add_argument('-t',  action='store_true')
parser.add_argument('-r', action='store_true')
parser.add_argument('--host', required='-t' in sys.argv, type=str)
parser.add_argument('-f', required='-t' in sys.argv, type=str)
args = parser.parse_args()
import socket
import tqdm
import os
import sys
import hashlib
from hurry.filesize import size
import pyfiglet
import base64

def warn_md5():
  print(f"Warning! MD5s do not match! {sent_hash}/{new_hash}")
  print("This means that either the transfer went wrong, or the file ")
  keep = input("Has been incerpeted by attackers, and is compromised. Keep file? (y/N)? ")
  if keep.lower() == 'n':
    os.remove(filename)

modes = ['transmit', 'receive','whomadethis?']
if args.t:
  SEP = "<SEP>"
  BUFFER_SIZE = 4096
  port = 9001
  host = args.host
  filename = args.f
  filesize = os.path.getsize(filename)
  s = socket.socket()


  print(f"[*] Connecting to {host}:{port}...")
  s.connect((host, port))
  print(f"[*] Connected to {host}!")
  Hash = hashlib.md5(open(filename,'rb').read()).hexdigest()
  dat = f'{filename}{SEP}{filesize}{SEP}{Hash}{SEP}'.encode()
  # while len(dat.encode()) < 4096:
    # dat = dat+'0'
  s.send(dat)
  

  progress = tqdm.tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)
  with open(filename, "rb") as fi:
    for _ in progress:
      bytes_read = fi.read(BUFFER_SIZE)
      byte_size = len(bytes_read)
      if not bytes_read:
        break
      s.sendall(bytes_read)
      progress.update(byte_size)
  s.close()



elif args.r:
  global sent_hash
  default_key = '5LabvIZ3MFAxk0IgJnTjwyHbWXVZdoPQcEzLeLL9IHE='.encode()
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


  received = client_socket.recv(BUFFER_SIZE).decode()
  print(f"Received {len(received)} bytes")
  raw = received.split(SEP)
  print(raw)
  while '' in raw:
    raw.remove('')
  print(raw)
  filename = raw[0]
  filesize = raw[1]
  sent_hash = raw[2]
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
      bytes_read =client_socket.recv(BUFFER_SIZE)
      if not bytes_read:
        break
      f.write(bytes_read)
      progress.update(len(bytes_read))
  client_socket.close()
  s.close()
  progress.close()
  new_hash = hashlib.md5(open(filename,'rb').read()).hexdigest()
  if not new_hash == sent_hash:
    warn_md5()

