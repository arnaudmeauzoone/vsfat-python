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
        if offset >= dataRegion.base + dataRegion.len:
            continue
        if offset + len <= dataRegion.base:
            continue
        if (offset <= dataRegion.base && offset + len <= dataRegion.base + dataRegion.len):
            usepose = 0
            uselen = offset + len - dataRegion.base
        if (offset >= dataRegion.base && offset + len <= dataRegion.base + dataRegion.len):
            usepose = offset - dataRegion.base
            uselen = len
        if (offset >= dataRegion.base && offset + len >= dataRegion.base + dataRegion.len):
            usepose = offset - dataRegion.base
            uselen = dataRegion.base + dataRegion.len - offset
        if (offset <= dataRegion.base && offset + len >= dataRegion.base + dataRegion.len):
            usepose = 0
            uselen = dataRegion.base + dataRegion.len - offset

            if dataRegion.mem:
                buf.extend(dataRegion.mem[offset:len])
            elif dataRegion.file:
                with open(dataRegion.file, 'rb') as f:
                    mm = mmap.mmap(f.fileno(), 0)
                    buf.extend(mm[offset:len])

    return buf
