import mmap

dataRegions = []
v_mem = bytearray(b'\x00'*134217728)

class DataRegion():
    def __init__(self, base, len, mem, file):
        self.base = base
        self.len = len
        self.mem = mem
        self.file = file

def build_mbr():
    bootcode = bytes([0xFA, 0xB8, 0x00, 0x10, 0x8E, 0xD0, 0xBC, 0x00, 0xB0, 0xB8, 0x00, 0x00,
       0x8E, 0xD8, 0x8E, 0xC0, 0xFB, 0xBE, 0x00, 0x7C, 0xBF, 0x00, 0x06, 0xB9, 0x00, 0x02, 0xF3, 0xA4,
       0xEA, 0x21, 0x06, 0x00, 0x00, 0xBE, 0xBE, 0x07, 0x38, 0x04, 0x75, 0x0B, 0x83, 0xC6, 0x10, 0x81,
       0xFE, 0xFE, 0x07, 0x75, 0xF3, 0xEB, 0x16, 0xB4, 0x02, 0xB0, 0x01, 0xBB, 0x00, 0x7C, 0xB2, 0x80,
       0x8A, 0x74, 0x01, 0x8B, 0x4C, 0x02, 0xCD, 0x13, 0xEA, 0x00, 0x7C, 0x00, 0x00, 0xEB, 0xFE, 0x00])
    serial = bytes([0xDE, 0xAB, 0xBE, 0xEF])
    part1 = bytes([0x00, 0x20, 0x21, 0x00, 0x0c, 0xcd, 0xfb, 0xd2, 0x00, 0x08, 0x00, 0x00,0x00, 0xf8, 0xdf, 0xff])
    part2 = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00])
    part3 = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00])
    part4 = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00, 0x00, 0x00, 0x00])
    footer = bytes([0x55, 0xAA])

    mbr = bytearray(b'\x00'*512)
    mbr[0:len(bootcode)] = bootcode
    mbr[440: 440 + len(serial)] = serial
    mbr[446: 446 + len(part1)] = part1
    mbr[462: 462 + len(part2)] = part2
    mbr[478: 478 + len(part3)] = part3
    mbr[494: 494 + len(part4)] = part4
    mbr[510: 510 + len(footer)] = footer

    dataRegions.append(DataRegion(0, 512, mbr, 0))
    v_mem[0:512] = mbr
    print("mbr done")

def build_boot_sector():
    BPB_BytsPerSec = 512
    BkBootSec = 6
    part1_base = 1048576

    bootentry = bytearray()
    bootentry.extend(b'\xeb') ## BS_jmpBoot[0]
    bootentry.extend(b'\x58') ## BS_jmpBoot[1]
    bootentry.extend(b'\x90') ## BS_jmpBoot[1]
    bootentry.extend("VSFAT1.0".encode('utf-8')) ## BS_OEMName
    bootentry.extend(bytes(BPB_BytsPerSec)) ## BPB_BytsPerSec
    bootentry.extend(bytes(32)) ## SecPerClus
    bootentry.extend(bytes(32)) ## RsvdSecCnt
    bootentry.extend(bytes(2)) ## NumFATs
    bootentry.extend(bytes(0)) ## RootEntCnt
    bootentry.extend(bytes(0)) ## TotSec16
    bootentry.extend(bytes(248)) ## Media
    bootentry.extend(bytes(0)) ## FATSz16
    bootentry.extend(bytes(32)) ## SecPerTrk
    bootentry.extend(bytes(64)) ## NumHeads
    bootentry.extend(bytes(0)) ## HiddSec
    bootentry.extend(bytes(102400)) ## TotSec32
    bootentry.extend(bytes(8189)) ## FATSz32
    bootentry.extend(bytes(0)) ## ExtFlags
    bootentry.extend(bytes(0)) ## FSVer
    bootentry.extend(bytes(2)) ## RootClus
    bootentry.extend(bytes(1)) ## FSInfo
    bootentry.extend(bytes(BkBootSec)) ## BkBootSec
    bootentry.extend(bytes(128)) ## DrvNum
    bootentry.extend(bytes(0)) ## Reserved1
    bootentry.extend(bytes(29)) ## BootSig
    bootentry.extend(b'\x84\x56\xf2\x37') ## VolID
    bootentry.extend(b'\xAA\x55') ## BootSign
    bootentry.extend(bytes([0x56, 0x53, 0x46, 0x41, 0x54, 0x46, 0x53, 0x20, 0x20, 0x20, 0x20])) ## VolLab
    bootentry.extend(bytes([0x46, 0x41, 0x54, 0x33, 0x32, 0x20, 0x20, 0x20])) ## FilSysType

    dataRegions.append(DataRegion(part1_base, 512, bootentry, 0))
    dataRegions.append(DataRegion(part1_base + BkBootSec*BPB_BytsPerSec, 512, bootentry, 0))

    v_mem[part1_base: part1_base + 512] = bootentry
    v_mem[part1_base + BkBootSec*BPB_BytsPerSec: part1_base + BkBootSec*BPB_BytsPerSec + 512] = bootentry

def build_fats():
    BPB_FATSz32 = 8189
    BPB_BytsPerSec = 512
    BPB_RsvdSecCnt = 32
    part1_base = 1048576

    fatspecial = bytes([0x00, 0x20, 0x21, 0x00, 0x0c, 0xcd, 0xfb, 0xd2, 0x00, 0x08, 0x00, 0x00,0x00, 0xf8, 0xdf, 0xff])

    fat = bytearray(b'\x00'*BPB_FATSz32*BPB_BytsPerSec)
    fat[0:len(fatspecial)] = fatspecial

    dataRegions.append(DataRegion(part1_base + BPB_BytsPerSec * (BPB_RsvdSecCnt + BPB_FATSz32 * 0), BPB_FATSz32 * BPB_BytsPerSec, fat, 0))
    dataRegions.append(DataRegion(part1_base + BPB_BytsPerSec * (BPB_RsvdSecCnt + BPB_FATSz32 * 1), BPB_FATSz32 * BPB_BytsPerSec, fat, 0))

def build_root_dir():
    pass

def scan_folders():
    pass

def read_data(offset, lenth):

    buf = bytearray()

    for dataRegion in dataRegions:
        if offset >= dataRegion.base + dataRegion.len:
            continue
        if offset + lenth <= dataRegion.base:
            continue
        if (offset <= dataRegion.base and offset + lenth <= dataRegion.base + dataRegion.len):
            usepose = 0
            uselen = offset + lenth - dataRegion.base
        if (offset >= dataRegion.base and offset + lenth <= dataRegion.base + dataRegion.len):
            usepose = offset - dataRegion.base
            uselen = lenth
        if (offset >= dataRegion.base and offset + lenth >= dataRegion.base + dataRegion.len):
            usepose = offset - dataRegion.base
            uselen = dataRegion.base + dataRegion.len - offset
        if (offset <= dataRegion.base and offset + lenth >= dataRegion.base + dataRegion.len):
            usepose = 0
            uselen = dataRegion.len

            if dataRegion.mem:
                buf.extend(dataRegion.mem[usepose:uselen])
            elif dataRegion.file:
                with open(dataRegion.file, 'rb') as f:
                    mm = mmap.mmap(f.fileno(), 0)
                    buf.extend(mm[usepose:uselen])

    pad = (lenth - len(buf))
    buf.extend(b'\x00'*pad)
    return buf
