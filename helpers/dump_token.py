#!/usr/bin/env python3

import os
import binascii
import struct
import sys

USAGE = """
usage: dump_token.py TOKEN_FILE

Prints a .token file (an EINITTOKEN).

See: 
    sdm-vol-3d: '37.15 EINIT TOKEN STRUCTURE (EINITTOKEN)
    of the Intel Software Developer Manuals.
""".strip()

TOKEN_SIZE = 304

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
        print("%-24s [%3dB]: %s" % \
                (name, len(value), binascii.hexlify(value).decode()))
    else:
        print("%-24s [%3dB]: %s (%s)" % \
                (name, len(value), binascii.hexlify(value).decode(),
                    extra))

def print_valid(value):
    v = struct.unpack("B", value[0:1])[0]
    extra = "invalid"
    if v & 0x01:
        extra = "valid"
    print_field("VALID", value, extra)

def main(argv):
    if len(argv) != 2:
        usage(1)

    token_file = argv[1]
    size = os.path.getsize(token_file)
    if size != TOKEN_SIZE:
        die('file "%s" is %d bytes; expected %d bytes\n' % \
                (token_file, size, TOKEN_SIZE))

    with open(token_file, 'rb') as f:
        t = f.read(TOKEN_SIZE)
        assert len(t) == TOKEN_SIZE

    valid       = take(t,   0,  4)
    reserved0   = take(t,   4, 44)
    attributes  = take(t,  48, 16)
    mrenclave   = take(t,  64, 32)
    reserved1   = take(t,  96, 32)
    mrsigner    = take(t, 128, 32)
    reserved2   = take(t, 160, 32)
    cpusvnle    = take(t, 192, 16)
    isvprodidle = take(t, 208,  2)
    isvsvnle    = take(t, 210,  2)
    cet_masked_attributes_le = take(t, 212, 1)
    reserved3   = take(t, 213, 23)
    maskedmiscselectle  = take(t, 236,  4)
    maskedattributesle  = take(t, 240, 16)
    keyid       = take(t, 256, 32)
    mac         = take(t, 288, 16)

    if reserved0 != b'\x00' * 44:
        warn("first RESERVED not zero")

    print_valid(valid)
    print_field("RESERVED", reserved0)
    print_field("ATTRIBUTES", attributes)
    print_field("MRENCLAVE", mrenclave)
    print_field("RESERVED", reserved1)
    print_field("MRSIGNER", mrsigner)
    print_field("RESERVED", reserved2)
    print_field("CPUSVNLE", cpusvnle)
    print_field("ISVPRODIDLE", isvprodidle)
    print_field("ISVSNVLE", isvsvnle)
    print_field("CET_MASKED_ATTRIBUTES_LE", cet_masked_attributes_le)
    print_field("RESERVED", reserved3)
    print_field("MASKEDMISCSELECTLE", maskedmiscselectle)
    print_field("MASKEDATTRIBUTESLE", maskedattributesle)
    print_field("KEYID", keyid)
    print_field("MAC", mac)

if __name__ == '__main__':
    main(sys.argv)

