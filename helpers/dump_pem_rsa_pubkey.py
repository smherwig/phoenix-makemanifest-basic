#!/usr/bin/env python3

import re
import subprocess

def lstrip_00_bytes(a):
    h = a[0]
    while h == '00':
        a.pop(0)
        h = a[0]

def run_shell_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessErorr as e:
        die("cmd \"%s\" returned %d: %s", cmd, e.returncode, str(e))
    return output.decode()

def dump_pem_pubkey(pubfile):
    cmd = 'openssl rsa -inform PEM -pubin -in %s -text -noout' % pubfile
    output = run_shell_cmd(cmd)

    lines = output.splitlines()

    bits = 0 
    mod_hex = []
    exp_hex = []

    # XXX: really gross parsing of the openssl output
    for i, line in enumerate(lines):
        if re.match(r'\s+[\da-f]{2}:', line):
            line = line.strip().rstrip(':')
            mod_hex.extend(line.split(':'))
        else: 
            mobj = re.match(r'Exponent: \d+ \(0x([\da-f]+)\)', line)
            if mobj:
                hs = mobj.group(1)
                if len(hs) % 2:
                    hs = '0' + hs
                for i in range(0, len(hs), 2): 
                    exp_hex.append(hs[i:i+2])
                continue
            mobj = re.match(r'Public-Key: \((\d+) bit\)', line)
            if mobj:
                bits = int(mobj.group(1))

    lstrip_00_bytes(mod_hex)
    lstrip_00_bytes(exp_hex)

    return (''.join(mod_hex), ''.join(exp_hex))

USAGE = """
usage: dump_pem_rsa_pubkey.py PATH_TO_PUBLIC_KEY_PEM
""".strip()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write(USAGE + "\n")
        sys.exit(1)

    mod_hex, exp_hex = dump_pem_pubkey(sys.argv[1])
    print("RSA modulus (n)  = %s" % mod_hex)
    print("RSA exponent (e) = %s" % exp_hex)
