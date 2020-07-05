#!/usr/bin/env python3

import os
import binascii
import struct
import sys

USAGE = """
usage: dump_sigfile.py SIGFILE

Prints a .sig file (a SIGSTRUCT).

See: 
    sdm-vol-3d: '37.14 ENCLAVE SIGNATURE STRUCTURE (SIGSTRUCT)' 
    of the Intel Software Developer Manuals.
""".strip()

SIGSTRUCT_SIZE = 1808
HEADER = binascii.unhexlify("06000000e10000000000010000000000")
VENDOR_INTEL = binascii.unhexlify("00008086")
VENDOR_NON_INTEL = binascii.unhexlify("00000000")
HEADER2 = binascii.unhexlify("01010000600000006000000001000000")
EXPONENT = binascii.unhexlify("03000000")

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
        print("%-19s [%3dB]: %s" % \
                (name, len(value), binascii.hexlify(value).decode()))
    else:
        print("%-19s [%3dB]: %s (%s)" % \
                (name, len(value), binascii.hexlify(value).decode(),
                    extra))

def print_vendor(value):
    vendor = "Unknown Vendor"
    if value == VENDOR_INTEL:
        vendor = "Intel"
    elif value == VENDOR_NON_INTEL:
        vendor = "Non-Intel"
    print_field("VENDOR", value, vendor)

def print_date(value):
    yyyy, mm, dd = struct.unpack("HBB", value)
    date_stamp = "%4d-%02d-%02d" % (yyyy, mm, dd)
    print_field("DATE", value, date_stamp)

def main(argv):
    if len(argv) != 2:
        usage(1)

    sig_file = argv[1]
    size = os.path.getsize(sig_file)
    if size != SIGSTRUCT_SIZE:
        die('file "%s" is %d bytes; expected %d bytes\n' % \
                (sig_file, size, SIGSTRUCT_SIZE))

    with open(sig_file, 'rb') as f:
        ss = f.read(SIGSTRUCT_SIZE)
        assert len(ss) == SIGSTRUCT_SIZE

    header          = take(ss,   0,  16)
    vendor          = take(ss,  16,   4)
    date            = take(ss,  20,   4)
    header2         = take(ss,  24,  16)
    swdefined       = take(ss,  40,   4)
    reserved0       = take(ss,  44,  84)
    modulus         = take(ss, 128, 384)
    exponent        = take(ss, 512,   4)
    signature       = take(ss, 516, 384)
    miscselect      = take(ss, 900,   4)
    miscmask        = take(ss, 904,   4)
    cet_attributes  = take(ss, 908,   1)
    cet_attributes_mask  = take(ss, 909,   1)
    reserved1       = take(ss, 910,   2)
    isvfamilyid     = take(ss, 912,  16)
    attributes      = take(ss, 928,  16)
    attributemask   = take(ss, 944,  16)
    enclavehash     = take(ss, 960,  32)
    reserved2       = take(ss, 992,  16)
    isvextprodid    = take(ss,1008,  16)
    isvprodid       = take(ss,1024,   2)
    isvsvn          = take(ss,1026,   2)
    reserved3       = take(ss,1028,  12)
    q1              = take(ss,1024, 384)
    q2              = take(ss,1424, 384)

    if header != HEADER:
        warn('HEADER does not match required value: %s' % \
                binascii.hexlify(HEADER).decode())

    if vendor != VENDOR_INTEL and vendor != VENDOR_NON_INTEL:
        warn('VENDOR unknown')

    if header2 != HEADER2:
        warn('HEADER2 does not match required value: %s' % \
                binascii.hexlify(HEADER2).decode())

    if reserved0 != b'\x00' * 84:
        warn('first RESERVED not zero')

    if exponent != EXPONENT:
        warn('EXPONENT not 3')

    if reserved1 != b'\x00\x00':
        warn('second RESERVED not zero')

    if reserved2 != b'\x00' * 16:
        warn('third RESERVED not zero')

    print_field("HEADER", header)
    print_vendor(vendor)
    print_date(date)
    print_field("HEADER2", header2)
    print_field("SWDEFINED", swdefined)
    print_field("RESERVED", reserved0)
    print_field("MODULUS", modulus)
    print_field("EXPONENT", exponent)
    print_field("SIGNATURE", signature)
    print_field("MISCSELECT", miscselect)
    print_field("MISCMASK", miscmask)
    print_field("CET_ATTRIBUTES", cet_attributes)
    print_field("CET_ATTRIBUTES_MASK", cet_attributes_mask)
    print_field("RESERVED", reserved1)
    print_field("ISVFAMILYID", isvfamilyid)
    print_field("ATTRIBUTES", attributes)
    print_field("ATTRIBUTEMASK", attributemask)
    print_field("ENCLAVEHASH", enclavehash, "MRENCLAVE")
    print_field("RESERVED", reserved2)
    print_field("ISVEXTPRODID", isvextprodid)
    print_field("ISVPRODID", isvprodid)
    print_field("ISVSVN", isvsvn)
    print_field("RESERVED", reserved3)
    print_field("Q1", q1)
    print_field("Q2", q2)

if __name__ == '__main__':
    main(sys.argv)

