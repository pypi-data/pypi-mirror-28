# -*- python-mode -*-
# -*- coding: UTF-8 -*-

# key_derivation
# Copyright (C) 2017 Francisco Reverbel
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import struct
import hashlib
import hmac


# path format for Stellar key pair derivation, as specified in
# https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0005.md
ACCOUNT_PATH_FORMAT = "m/44'/148'/%d'"


# the index of the first hardened key, per BIP-0032 and SLIP-0010
HARDENED = 0x80000000

# As in https://github.com/satoshilabs/slips/blob/master/slip-0010.md
CURVE = b'ed25519 seed'


hmac_sha_512 = lambda key, data: hmac.new(key, data, hashlib.sha512).digest()


def key(v):
    return v[:32]


def chain_code(v):
    return v[32:]


def ser32(i):
    return struct.pack('>L', i)
    

def new_master_key(seed):
    h = hmac_sha_512(CURVE, seed);
    return (key(h), chain_code(h))


def derive(parent_key, parent_chain_code, i):
    assert len(parent_key) == 32
    assert len(parent_chain_code) == 32    
    assert i >= HARDENED, 'no public derivation for ed25519'
    data = b'\x00' + parent_key + ser32(i)
    h = hmac_sha_512(parent_chain_code, data)
    return (key(h), chain_code(h))


def derive_along_path(path, seed):
    elements = list(element.rstrip("'") for element in path.split('/'))[1:]
    (key, chain_code) = new_master_key(seed)
    for e in elements:
        (key, chain_code) = derive(key, chain_code, int(e) | HARDENED)
    return key


def account_keypair(seed, account_number):
    from stellar_base.keypair import Keypair
    acc_seed = derive_along_path(ACCOUNT_PATH_FORMAT % account_number, seed);
    return Keypair.from_raw_seed(acc_seed)

def selftest():
    from binascii import unhexlify
    
    seed = unhexlify(
        'e4a5a632e70943ae7f07659df1332160937fad82587216a4c64315a0fb39497ee4a01f76ddab4cba68147977f3a147b6ad584c41808e8238a07f6cc4b582f186'
    )
    k = unhexlify(
        'e0eec84fe165cd427cb7bc9b6cfdef0555aa1cb6f9043ff1fe986c3c8ddd22e3'
    )
    key = derive_along_path("m/44'/148'", seed)
    assert key == k

    kp = account_keypair(seed, 0)
    assert kp.address().decode() == 'GDRXE2BQUC3AZNPVFSCEZ76NJ3WWL25FYFK6RGZGIEKWE4SOOHSUJUJ6'
    assert kp.seed().decode() == 'SBGWSG6BTNCKCOB3DIFBGCVMUPQFYPA2G4O34RMTB343OYPXU5DJDVMN'

    kp = account_keypair(seed, 9)
    assert kp.address().decode() == 'GBTVYYDIYWGUQUTKX6ZMLGSZGMTESJYJKJWAATGZGITA25ZB6T5REF44'
    assert kp.seed().decode() == 'SCJGVMJ66WAUHQHNLMWDFGY2E72QKSI3XGSBYV6BANDFUFE7VY4XNXXR'
