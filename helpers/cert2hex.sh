#!/bin/bash

set -e

#
# Converts a PEM certificate to a hexstring of its corresponding 
# DER-encoding.
#

# Example: 
#   $ ./cert2hex.sh cert.pem
#

if [ $# -ne 1 ]; then
    printf "usage: $0 CERT\n" >&2
    exit 1
fi

CERT="$1"

# xxd  defaults to only printing 60 hexdigits per line.
# This limit can be toggled with -c, but only up to 256.
# Thus, I use tr to "join" xxd's output lines.
openssl x509 -inform PEM -outform DER -in $CERT | xxd -p | tr -d \\n
