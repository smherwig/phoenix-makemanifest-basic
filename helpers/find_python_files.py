#!/usr/bin/env python3

import getopt
import re
import os
import subprocess
import sys

USAGE = """
./find_python_files [options] VERSION  [DIR1 ...]

Finds the .py and .so files, as well as the .so dependencies, for a given
python version.  VERSION should be 2.7, 3.5, 3.6, etc.  The script does
not include any .pyc files.  The script searchs:

    - /usr/lib/python{VERSION}
    - /usr/local/lib/python{VERSION}/dist-packages
    - /usr/lib/python{MAJOR_VERSION}/dist-packages

as well as the .so dependencies for /usr/bin/python{VERSION}, 
where MAJOR_VERSION is 2 for 2.7, and 3 for 3.5 and 3.6, etc.

Additional search directories may be given after the VERSION argument.

options:
  -h, --help
    Show this help message and exit

  -p, --prefix PREFIX
    Instead of just printing a list of the files
    print the files in a format suitable for a Graphene
    manifest file, e.g.:

        sgx.trusted_files.<PREFIX><COUNTER> = file:/<FILE-PATH>

    PREFIX should not include the '.' symbol. 

  -v, --verbose
    Show debug messages

example:
  ./find_python_files --prefix py 3.6
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


def dirwalk(root, valid_exts):
    debug("searching %s for file extensions: %s" % (root, valid_exts))
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fname in filenames:
            ext = os.path.splitext(fname)[1]
            if ext in valid_exts:
                fullpath = os.path.join(dirpath, fname)
                results.append(fullpath)
    return results

def main(argv):
    global verbose
    short_opts = 'hp:v'
    long_opts = ['help', 'prefix=', 'verbose']
    prefix = None
    py_version = None
    py_major_version = None
    valid_exts = ('.py', '.so')

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
    
    if not len(args):
        usage(1)

    py_version = args[0] 
    py_major_version = py_version.split('.')[0]
    if py_major_version == py_version:
        sys.stderr.write('%s is not a valid python version' % py_version)
        sys.exit(1)

    # get the .py and .so files under these directories
    fileset = set()
    fileset.update(dirwalk('/usr/lib/python%s' % py_version, valid_exts))
    fileset.update(dirwalk('/usr/local/lib/python%s/dist-packages'% py_version, valid_exts))
    fileset.update(dirwalk('/usr/lib/python%s/dist-packages' % py_major_version, valid_exts))

    for path in args[1:]:
        fileset.update(dirwalk(path, valid_exts))
    
    # add the .so dependencies
    for path in list(fileset):
        if path.endswith('.so'):
            fileset.update(ldd_rec(path))
    fileset.update(ldd_rec('/usr/bin/python%s' % py_version))
    
    # sort the files alphabetically
    outfiles = list(fileset)
    outfiles.sort()

    # output the results
    for i, path in enumerate(outfiles):
        if prefix is not None:
            print('sgx.trusted_files.%s%d = file:%s' % (prefix, i, path))
        else:
            print('%s' % (path,))

if __name__ == '__main__':
    main(sys.argv)
