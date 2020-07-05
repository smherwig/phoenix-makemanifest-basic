#!/usr/bin/env python3

import os
import binascii
import sys

USAGE = """
usage: dump_target_info.py TARGET_INFO_FILE

Prints a TARGETINFO file (a TARGETINFO).

See: 
    sdm-vol-3d: '37.17 REPORT TARGET INFO (TARGETINFO)'
    of the Intel Software Developer Manuals.

    The my_target_info.lua script reads /dev/attestation/my_target_info
    and writes the data to a file.  This script can then be used to
    display that file.
""".strip()

TARGETINFO_SIZE = 512

def usage(status):
    sys.stderr.write("%s\n" % USAGE)
    sys.exit(status)

def die(msg):
    sys.stderr.write("[Error] %s" % msg)
    sys.exit(1)

def warn(msg):
    sys.stderr.write("[Warn] %s" % msg)

def take(data, offset, size):
    return data[offset:offset+size]

def print_field(name, value, extra=""):
    if not extra:
        print("%-14s [%3dB]: %s" % \
                (name, len(value), binascii.hexlify(value).decode()))
    else:
        print("%-14s [%3dB]: %s (%s)" % \
                (name, len(value), binascii.hexlify(value).decode(),
                    extra))

def main(argv):
    if len(argv) != 2:
        usage(1)

    target_info_file = argv[1]
    size = os.path.getsize(target_info_file)
    if size != TARGETINFO_SIZE:
        die('file "%s" is %d bytes; expected %d bytes\n' % \
                (target_info_file, size, TARGETINFO_SIZE))

    with open(target_info_file, 'rb') as f:
        ti = f.read(TARGETINFO_SIZE)
        assert len(ti) == TARGETINFO_SIZE

    measurement    = take(ti,   0,  32)
    attributes     = take(ti,  32,  16)
    cet_attributes = take(ti,  48,  16)
    reserved0      = take(ti,  49,   1)
    configsvn      = take(ti,  50,   2)
    miscselect     = take(ti,  52,   4)
    reserved1      = take(ti,  56,   8)
    configid       = take(ti,  64,  64)
    reserved2      = take(ti, 128, 384)

    if reserved0 != b'\x00':
        warn('first RESERVED not zero')

    if reserved1 != b'\x00' * 8:
        warn('second RESERVED not zero')

    if reserved2 != b'\x00' * 384:
        warn('third RESERVED not zero')

    print_field("MEASUREMENT", measurement, "MRENCLAVE")
    print_field("ATTRIBUTES", attributes)
    print_field("CET_ATTRIBUTES", cet_attributes)
    print_field("RESERVED", reserved0)
    print_field("CONFIGSVN", configsvn)
    print_field("MISCSELECT", miscselect)
    print_field("RESERVED", reserved1)
    print_field("CONFIGID", configid)
    print_field("RESERVED", reserved2)

if __name__ == '__main__':
    main(sys.argv)

