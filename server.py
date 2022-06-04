#!/usr/bin/python

import socket
from vsfat import *

class Request:
    def __init__(self, r_magic, r_type, r_handle, r_from, r_len):
        self.r_magic = r_magic
        self.r_type = r_type
        self.r_handle = r_handle
        self.r_from = r_from
        self.r_len = r_len

class Reply:
    def __init__(self, r_magic, r_error, r_handle):
        self.r_magic = r_magic
        self.r_error = r_error
        self.r_handle = r_handle

def readAll(conn, n):
    buf = bytearray()
    while len(buf) < n:
        packet = conn.recv(n - len(buf))
        if not packet:
            return None
        buf.extend(packet)
    return buf

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 15555))

build_mbr()
build_boot_sector()
# build_fats()
# build_root_dir()
# scan_folder()


while True:
  server.listen(1)
  conn, addr = server.accept()
  print("received conn from {0}".format(addr))
  while True:
    data = conn.recv(28)
    if data:
      request = Request(data[0:4],data[4:8],data[8:16],data[16:24],data[24:28])
      # print("received request: magic = {0}".format(request.r_magic.hex()))
      # print("received request: type = {0}".format(request.r_type.hex()))
      # print("received request: handle = {0}".format(request.r_handle.hex()))
      # print("received request: from = {0}".format(request.r_from.hex()))
      # print("received request: len = {0}".format(request.r_len.hex()))
      reply = Reply(b'\x67\x44\x66\x98',b'\x00\x00\x00\x00',request.r_handle)
      reply_data = bytearray()
      reply_data.extend(reply.r_magic)
      reply_data.extend(reply.r_error)
      reply_data.extend(reply.r_handle)
      if(int.from_bytes(request.r_type, "big") == 0): ## read request
          print("received read request of lenth {0} from {1}".format(request.r_len.hex(), request.r_from.hex()))
          conn.sendall(reply_data)
          #buf = read_data(int.from_bytes(request.r_from, "big"), int.from_bytes(request.r_len, "big"))
          buf = bytearray()
          buf.extend(v_mem[int.from_bytes(request.r_from, "big"):int.from_bytes(request.r_from, "big")+int.from_bytes(request.r_len, "big")])
          conn.sendall(buf)
      if(int.from_bytes(request.r_type, "big") == 1): ## write request
          print("received write request of lenth {0} from {1}".format(request.r_len.hex(), request.r_from.hex()))
          data = readAll(conn, int.from_bytes(request.r_len, "big"))
          v_mem[int.from_bytes(request.r_from, "big"):int.from_bytes(request.r_from, "big")+int.from_bytes(request.r_len, "big")] = data
          conn.sendall(reply_data)
      if(int.from_bytes(request.r_type, "big") == 2): ## close request
          print("received close request")
          conn.close()
      if(int.from_bytes(request.r_type, "big") == 3):
          print("received flush request")
          conn.sendall(reply_data)
      if(int.from_bytes(request.r_type, "big") == 4):
          print("received trim request")
          conn.sendall(reply_data)
