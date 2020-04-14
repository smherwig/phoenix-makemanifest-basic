#!/usr/bin/env python3

import getopt
import re
import os
import subprocess
import sys

USAGE = """
./ldd_rec [options] SHARED_OBJECT

Recursively run `ldd' over a shared object (a .so or executable),
and print out all non-glibc dependencies (Graphene provides
it's own patched glibc objects).  This is useful for knowing what
to specify for the fs.mount and sgx.trusted_files directives in a
Graphene manifest file.

options:
  -h, --help
    Show this help message and exit

  -p, --prefix PREFIX
    Instead of just printing a list of the dependencies,
    print the dependencies in a format suitable for a Graphene
    manifest file, e.g.:

        sgx.trusted_files.<PREFIX><COUNTER> = file:/<PATH-TO-DEPENDENCY>

    PREFIX should not include the '.' symbol. 

  -v, --verbose
    Show debug messages

bugs:
    Recursion could be more efficient by memoizing previous results
    (and thus not running ldd over shared objects we had previously
     run ldd over).

example:
    ./ldd_rec.py --prefix '' /bin/ls
""".strip()

verbose = False

# Graphene-provided libc files
glibc_libs = (
    # part of graphene Runtime
    'ld-linux-x86-64.so.2',
    'libc.so.6',
    'libdl.so.2',
    'libm.so.6',
    'libnss_dns.so.2',
    'libpthread.so.0',
    'libresolv.so.2',
    'librt.so.1',
    'libutil.so.1',
    # not explicitly in Graphene Runtime (but still omit)
    'linux-vdso.so.1'
)

def usage(status):
    sys.stderr.write('%s\n' % USAGE)
    sys.exit(status)

## str -> void
def debug(msg):
    msg = msg.rstrip()
    if verbose:
        sys.stderr.write('%s\n' % msg)

## int, str -> noreturn
def die(status, msg):
    msg = msg.rstrip()
    sys.stderr.write('%s\n' % msg)
    sys.exit(status)

## str -> bytes
def run_cmd(cmd):
    debug('running cmd: %s' % cmd)
    try:
        output = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
       die(1, "cmd '%s' returned %d: %s" % (cmd, e.returncode, str(e)))
    else:
        return output

## str -> set of str
def ldd_rec(path):
    deps = set()
    output = run_cmd('ldd %s' % path).decode('utf-8')
    for mobj in re.finditer(r'^\s*.+ => (.+) \(0x[a-f0-9]+\)\s*$', output, re.MULTILINE):
        so_path = mobj.group(1)
        so_name = os.path.basename(so_path)
        if so_name not in glibc_libs:
            deps.add(so_path)
            deps.update(ldd_rec(so_path))
        else:
            debug("skipping %s's dependency on glibc file %s" % (path, so_name))
    return deps

def main(argv):
    global verbose
    short_opts = 'hp:v'
    long_opts = ['help', 'prefix=', 'verbose']
    prefix = None

    try:
        opts, args = getopt.getopt(argv[1:], short_opts, long_opts)
    except getopt.GetoptError as e:
        sys.stderr.write('%s\n' % str(e))
        usage(1)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage(0)
        elif o in ('-p', '--prefix'):
            prefix = a
        elif o in ('-v', '--verbose'):
            verbose = True
        else:
            assert False, "unhandled option '%s'" % o
    
    if len(args) != 1:
        usage(1)

    shared_object_path = args[0]
    deps = ldd_rec(shared_object_path)
    for i, dep in enumerate(deps):
        if prefix is not None:
            print('sgx.trusted_files.%s%d = file:%s' % (prefix, i, dep))
        else:
            print('%s' % (dep,))

if __name__ == '__main__':
    main(sys.argv)
