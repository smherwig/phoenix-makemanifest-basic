#!/bin/bash

set -e

#
# Signs a Graphene manifest and retrieves launch token
#
# Assumes: 
#   1. signings key is at:
#       $GRAPHENE/Pal/src/host/Linux-SGX/signer/enclave-key.pem
#
#   2. manifest name is EXECNAME.manifest, where execname is the
#     basename of the executable (e.g., python3.6).
#
# Example: 
#   $ ./make-manifest ~/src/graphene python3.6.manifest
#
# This produces:
#
#   python3.6.manifest.sgx - a copy of python3.6, ammended with file hashes
#   python3.6.sig          - enclave signature
#   python3.6.token        - enclave launch token

if [ $# -ne 2 ]; then
    printf "usage: $0 GRAPHENE_ROOTDIR MANIFEST\n" >&2
    exit 1
fi

GRAPHENE=$1
MANIFEST=$2
EXEC=${MANIFEST::-9}    # chomp '.manifest"

# ${var:offset:length}
# note that a negative offset needs a space
if [ ${GRAPHENE: -1} = "/" ]; then
    GRAPHENE=${GRAPHENE::-1}    # chomp trailing '/'
fi

LIBPAL=$GRAPHENE/Runtime/libpal-Linux-SGX.so
ENCLAVE_KEY=$GRAPHENE/Pal/src/host/Linux-SGX/signer/enclave-key.pem

./pal-sgx-sign \
    -key      $ENCLAVE_KEY \
    -libpal   $LIBPAL \
    -manifest $MANIFEST \
    -output   $MANIFEST.sgx

./pal-sgx-get-token \
    -sig    $EXEC.sig \
    -output $EXEC.token
