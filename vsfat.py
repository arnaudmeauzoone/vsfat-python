import mmap

class DataRegion():
    def __init__(self, base, len, mem, file):
        self.base = base
        self.len = len
        self.mem = mem
        self.file = file

def build_mbr():
    print("building")

def read_data(offset, len):

    buf = bytearray()

    for dataRegion in dataRegions:
        if offset + len  < dataRegion.base || offset > dataRegion.base + dataRegion.len:
            return
        if dataRegion.mem:
            buf.extend(dataRegion.mem[offset:len])
        elif dataRegion.file:
            with open("hello.txt", "r+b") as f:
                mm = mmap.mmap(f.fileno(), 0)
                buf.extend(mm[offset:len])

    return buf
