#!/usr/bin/python

import socket, fcntl, os, sys, termios

hote = sys.argv[2]
port = int(sys.argv[3])

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print("Connection on {}".format(hote))

f = open(sys.argv[1], "w+")

#define NBD_SET_SIZE             _IO( 0xab, 2 )
NBD_SET_SIZE = 171 << (4*2) | 2

#define BD_CLEAR_SOCK             _IO( 0xab, 4 )
NBD_CLEAR_SOCK = 171 << (4*2) | 4

#define NBD_SET_SOCK            _IO( 0xab, 0 )
NBD_SET_SOCK = 171 << (4*2) | 0

#define USBDEVFS_RESET             _IO( 0xab, 3 )
NBD_DO_IT = 171 << (4*2) | 3

## TODO add the good ioctl
fcntl.ioctl(f, NBD_SET_SIZE, 134217728)
fcntl.ioctl(f, NBD_CLEAR_SOCK)
fcntl.ioctl(f, NBD_SET_SOCK, socket.fileno())
fcntl.ioctl(f, NBD_DO_IT)
