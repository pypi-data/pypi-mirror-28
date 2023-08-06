# the dovecot_cram_md5 module

This python module generate HMAC-MD5 contexts, which will be used by dovecot for the CRAM-MD5 authentication method.

## Theory

HMAC-MD5 is a challenge-response authentication protocol. In order to avoid the storage of clear password, dovecot allows to generate the "context" value. It is an intermediate hash generated from the password during the authentication.

References:

https://tools.ietf.org/html/draft-ietf-sasl-crammd5-10

https://tools.ietf.org/html/rfc2104

## Using the module

Once the package is installed, you can use the dovecotpw function:

```
#! /usr/bin/env python
import dovecot_cram_md5

print dovecot_cram_md5.dovecotpw("toto1234")
```
