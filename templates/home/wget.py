#!/usr/bin/env python3

import getopt
import ssl
import sys
import urllib.request
import ssl

USAGE = """
./wget2.py [options] URL

options:

    -c, --ca-file CA_FILE
        Load a set of CA certificates (bundled as one .pem)file.
        (default: /etc/ssl/certs/ca-certificates.crt)
    
    -h, --help
        Show this help message and exit

    -o, --out-file OUT_FILE
        Save download to OUT_FILE
        (default: print to stdout)
""".strip()

def usage(status):
    sys.stderr.write('%s\n' % USAGE)
    sys.exit(status)


def main(argv):
    shortopts = 'c:ho:'
    longopts = ['ca-file=', 'help', 'out-file=']
    ca_file = '/etc/ssl/certs/ca-certificates.crt'
    out_file = None

    try:
        opts, args = getopt.getopt(argv[1:], shortopts, longopts)
    except getopt.GetoptError as err:
        sys.stderr.write('%s\n' % str(err))
        usage(1)

    for o, a in opts:
        if o in ('-c', '--ca-file'):
            ca_file = a
        elif o in ('-h', '--help'):
            usage(0)
        elif o in ('-o', '--out-file'):
            out_file = a
        else:
            assert False, "unhandled option '%s'" % o

    if len(args) != 1:
        usage(1)

    url = args[0]
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(ca_file)

    if out_file:
        f = open(out_file, 'wb')
    else:
        f = sys.stdout

    resp = urllib.request.urlopen(url, timeout=10, context=ctx)
    data = resp.read(1024)
    while data:
        if out_file:
            f.write(data)
        else:
            f.write(data.decode())
        data = resp.read(1024)

    if out_file:
        f.close()

if __name__ == '__main__':
    main(sys.argv)
