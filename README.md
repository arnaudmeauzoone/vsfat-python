# BUSE-python - A block device in userspace (written in python)

BUSE (Block storage in USErspace) written in pyhton

This work is inspired from https://github.com/acozzette/BUSE

To use it clone this repo

```console
git clone https://github.com/arnaudmeauzoone/BUSE-python.git
cd BUSE-python
```
Import nbd module

```console
sudo modprobe nbd
```

Then lunch the server

```console
python3 server.py
```

Then, with the root user, start the client (can be lunched on other machine)

local nbd device, server IP, server port
```console
python3 client.py /dev/nbd0 127.0.0.1 15555 
```

You should have a fully working virtual disk all written in python !

```console
sudo mkfs.ext4 /dev/nbd0
sudo mount /dev/nbd0 /mnt
```
