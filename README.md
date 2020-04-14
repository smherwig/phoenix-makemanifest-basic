Example usage:

Note that you will have to change the paths in the manifest files and in the
command-lines below to match your environment.  The instructions are the same
for vanilla Graphene or for Phoenix.

```
# copy the enclave signing and token retrieval tools from the Graphene/Phoenix
# source 
./copy-signing-tools.sh ~/src/graphene

# Produce a enclave signature and launch token for an application
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
