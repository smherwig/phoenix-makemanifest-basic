
Note that you will have to change the paths in the manifest files and in the
command-lines below to match your environment.  The instructions are the same
for vanilla Graphene or for Phoenix.

Example usage:
```
# copy the enclave signing and token retrieval tools from the Graphene/Phoenix
# source 
./copy-signing-tools.sh ~/src/graphene

# Produce an enclave signature and launch token for an application
./make-manifest.sh ~/src/graphene templates/hello.manifest

# run the application in an enclave
cd templates
SGX=1 ~/src/graphene/Runtime/pal_loader hello.manifest.sgx
```

In addition, the scripts `helpers/ldd_rec.py` and
`helpers/find_python_files.py` are helpful for determining an application's
shared object dependencies, as well as Python's basic runtime dependencies,
respectively.  Both scripts accept a `--help` flag to display their usage
statement.


Lua 5.3 template
----------------
The Lua template (`templates/lua5.3.manifest) runs lua5.3.  Since Lua's builtin
libraries are minimal, I also added the popular thrid-party module `luaposix`
as trusted.

To install `luaposix`, enter

```
sudo apt-get install lua-posix-dev
```

There is a bug in the debian lua-posix debian package
(https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=891541); thus, after
installation, you also have to create a symlink:

```
sudo ln -s /usr/lib/x8664-linux-gnu/lub/5.3/posix_c.so
/usr/lib/x86_64-linux-gnu/lua/5.3/posix.so
```

I have a number of simplified-versions of coreutil programs written in Lua that
are available under Graphene's `/home` mount.  For instance, to cat a file:

```
SGX=1 ~/src/graphene/Runtime/pal_loader lua5.3.manifest.sgx /home/cat.lua /home/testfile
```

Using the fsserver
------------------

If the fsserver only hosts data (as opposed to code), then first run 

```
./helpers/cert2hex.sh root.crt
```

where `root.crt` is the "CA" certificate that signed the filserver's
certificate.  Then, add the following lines to the `manifest.conf`:

```
fs.mount.fsserver0.type = nextfs
fs.mount.fsserver0.path = /fsserver0
fs.mount.fsserver0.uri = tcp:127.0.0.1:9084
phoenix.ca_der= <the hexstring output of ./helpers/cert2hex.sh root.crt>
```

The `uri` should start with `tcp:`, and the IP address will likely be
`127.0.0.1`; enter the appropriate port number.


Using the timeserver
--------------------

To have Phoenix invoke the timeserver for time related system calls, you need to
specify in the manifest file the URL for the timeserver, the modulus and
exponent of the timeserver's public key, and the proportion (rate) of
time-related system calls that Phoenix sends to the timeserver (the remaining
proportion proxy to the untrusted host's kernel).

To dump the modulus and exponent for the timeserver's public key, enter:

```
cd helpers
./dump_pem_rsa_pubkey.py PATH_TO_TIMESERVER_PUBLIC_KEY_PEM
```

In the `manifest.conf` file, enter

```
timserver.url = udp:127.0.0.1:12345
timeserver.rsa_n = <pasted from dump_pem_rsa_pubkey.py's output>
timserver.rsa_e = <pasted from dump_pem_rsa_pubkey.py's output>
timeserver.rate = 10000
```

The `timeserver.url` must always start with `udp:`; you should specify the IP
address and port, as appropriate.

The `timeserver.rate` must be in the range `[0, 10000]`; `0` means to never use
the timeserver; `10000` means contact the timeserver for every call; `5000`
means use the timeserver for half the calls, etc.
