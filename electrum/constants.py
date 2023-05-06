# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
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

import os
import json

from .util import inv_dict
from . import bitcoin


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except:
        r = default
    return r


GIT_REPO_URL = "https://github.com/runebase/runebase-electrum/"
GIT_REPO_ISSUES_URL = "https://github.com/runebase/runebase-electrum/issues"
BIP39_WALLET_FORMATS = read_json('bip39_wallet_formats.json', [])


class AbstractNet:

    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 0
    CHECKPOINTS = {}
    GENESIS = ""
    REDUCE_BLOCK_TIME_HEIGHT = 0

    @classmethod
    def max_checkpoint(cls) -> int:
        checkpoints = [int(k) for k, v in cls.CHECKPOINTS.items() if v != 0] or [0, ]
        return max(0, max(checkpoints))

    @classmethod
    def rev_genesis_bytes(cls) -> bytes:
        return bytes.fromhex(bitcoin.rev_hex(cls.GENESIS))

    @classmethod
    def coinbase_maturity(cls, height: int):
        return 500 if height < cls.REDUCE_BLOCK_TIME_HEIGHT else 2000


class RunebaseMainnet(AbstractNet):

    TESTNET = False
    WIF_PREFIX = 0xd8
    BITCOIN_ADDRTYPE_P2PKH = 0
    BITCOIN_ADDRTYPE_P2SH = 5
    ADDRTYPE_P2PKH = 0x3d
    ADDRTYPE_P2SH = 0x7b
    SEGWIT_HRP = "rc"
    GENESIS = "0000208ee7a300f2baaf39f8524bf1bd6ed90db885d97b26e1a229f44ff73b9a"
    GENESIS_BITS = 0x1f00ffff
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json('checkpoints.json', {})
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 0
    HEADERS_URL = 'https://downloads.runebase.io/electrum_headers'

    POS_NO_RETARGET = False

    POW_LIMIT = 0x0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    POS_LIMIT = 0x00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    QIP9_POS_LIMIT = 0x0000000000001fffffffffffffffffffffffffffffffffffffffffffffffffff
    RBT_POS_LIMIT = 0x0000000000003fffffffffffffffffffffffffffffffffffffffffffffffffff

    QIP5_FORK_HEIGHT = 0
    QIP9_FORK_HEIGHT = 0
    OFFLINE_STAKE_HEIGHT = 900000 #upcoming fork
    REDUCE_BLOCK_TIME_HEIGHT = 999999999 # upcoming fork

    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = []

    # for the 88 and 2301 coin type issue, see https://github.com/satoshilabs/slips/pull/196
    # Runebase official uses 88 as coin type
    BIP44_COIN_TYPE = 88
    SLIP_COIN_TYPE = 2301

    XPRV_HEADERS = {
        'standard': 0x0586dcf1,
        'p2wpkh-p2sh': 0x049d7878,
        'p2wsh-p2sh': 0x295b005,
        'p2wpkh': 0x4b2430c,
        'p2wsh': 0x2aa7a99
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)

    XPUB_HEADERS = {
        'standard': 0x0586c22e,
        'p2wpkh-p2sh': 0x049d7cb2,
        'p2wsh-p2sh': 0x295b43f,
        'p2wpkh': 0x4b24746,
        'p2wsh': 0x2aa7ed3
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)


class RunebaseTestnet(AbstractNet):

    TESTNET = True
    WIF_PREFIX = 0xca
    BITCOIN_ADDRTYPE_P2PKH = 111
    BITCOIN_ADDRTYPE_P2SH = 196
    ADDRTYPE_P2PKH = 106
    ADDRTYPE_P2SH = 229
    SEGWIT_HRP = "rcrt"
    GENESIS = "0000019d9d91d1c7fd440938747eed3ca13a2d2c0533054115f147ab0da69d46"
    GENESIS_BITS = 0x1f00ffff
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = read_json('checkpoints_testnet.json', {})
    BIP44_COIN_TYPE = 1
    SLIP_COIN_TYPE = 1
    HEADERS_URL = 'https://downloads.runebase.io/electrum_testnet_headers'

    POS_NO_RETARGET = False

    POW_LIMIT = 0x0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    POS_LIMIT = 0x0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    QIP9_POS_LIMIT = 0x0000000000001fffffffffffffffffffffffffffffffffffffffffffffffffff
    RBT_POS_LIMIT = 0x0000000000003fffffffffffffffffffffffffffffffffffffffffffffffffff

    QIP5_FORK_HEIGHT = 0
    QIP9_FORK_HEIGHT = 0
    OFFLINE_STAKE_HEIGHT = 10000 # upcoming fork
    REDUCE_BLOCK_TIME_HEIGHT = 999999999999999 # upcoming fork

    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = []

    XPRV_HEADERS = {
        'standard': 0x053784a4,
        'p2wpkh-p2sh': 0x044a4e28,
        'p2wsh-p2sh': 0x024285b5,
        'p2wpkh': 0x045f18bc,
        'p2wsh': 0x02575048
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)

    XPUB_HEADERS = {
        'standard': 0x053782bf,
        'p2wpkh-p2sh': 0x044a5262,
        'p2wsh-p2sh': 0x024289ef,
        'p2wpkh': 0x045f1cf6,
        'p2wsh': 0x02575483
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)


class RunebaseRegtest(RunebaseTestnet):

    SEGWIT_HRP = "rcrt"
    GENESIS = "7bf779b04828d0fd6de63c64c1de4980eb16afe40aa0dd7e0f865edf92438e69"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = {}
    HEADERS_URL = None

    POS_NO_RETARGET = True

    POW_LIMIT = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    POS_LIMIT = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    QIP9_POS_LIMIT = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    QIP5_FORK_HEIGHT = 0
    QIP9_FORK_HEIGHT = 0
    OFFLINE_STAKE_HEIGHT = 1
    REDUCE_BLOCK_TIME_HEIGHT = 0


# don't import net directly, import the module instead (so that net is singleton)
net = RunebaseMainnet


def set_mainnet():
    global net
    net = RunebaseMainnet


def set_testnet():
    global net
    net = RunebaseTestnet


def set_regtest():
    global net
    net = RunebaseRegtest
