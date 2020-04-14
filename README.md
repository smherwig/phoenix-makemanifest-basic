```
./copy-signing-tools.sh ~/src/graphene
./make-manifest.sh ~/src/graphene templates/hello.manifest
cd templates
SGX=1 ~/src/graphene/Runtime/pal_loader hello.manifest.sgx
```
