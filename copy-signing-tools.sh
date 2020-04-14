#!/bin/bash

set -e

#
# Copies enclave signing and launch token scripts from Graphene
#

if [ $# -ne 1 ]; then
    printf "usage: $0 GRAPHENE_ROOTDIR\n" >&2
    exit 1
fi

GRAPHENE=$1

# ${var:offset:length}
# note that a negative offset needs a space
if [ ${GRAPHENE: -1} = "/" ]; then
    GRAPHENE=${GRAPHENE::-1}
fi

cp $GRAPHENE/Pal/src/host/Linux-SGX/generated_offsets.py .
cp $GRAPHENE/Pal/src/host/Linux-SGX/signer/aesm_pb2.py .
cp $GRAPHENE/Pal/src/host/Linux-SGX/signer/aesm.proto .
cp $GRAPHENE/Pal/src/host/Linux-SGX/signer/pal-sgx-get-token .
cp $GRAPHENE/Pal/src/host/Linux-SGX/signer/pal-sgx-sign .

# Only newer versions of Graphene have pal_sgx_sign.py
if [ -f $GRAPHENE/Pal/src/host/Linux-SGX/signer/pal_sgx_sign.py ]; then
    cp $GRAPHENE/Pal/src/host/Linux-SGX/signer/pal_sgx_sign.py .
fi
