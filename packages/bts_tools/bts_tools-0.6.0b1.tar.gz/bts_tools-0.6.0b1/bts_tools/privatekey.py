# The MIT License (MIT)
#
# Copyright (c) 2015 Fabian Schuh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import ecdsa
import hashlib
from binascii import hexlify, unhexlify
import sys
import re
import os

from .base58 import ripemd160, Base58

""" This class and the methods require python3 """
assert sys.version_info[0] == 3, "graphenelib requires python3"


class Address(object):
    """ Address class
        This class serves as an address representation for Public Keys.
        :param str address: Base58 encoded address (defaults to ``None``)
        :param str pubkey: Base58 encoded pubkey (defaults to ``None``)
        :param str prefix: Network prefix (defaults to ``BTS``)
        Example::
           Address("BTSFN9r6VYzBK8EKtMewfNbfiGCr56pHDBFi")
    """
    def __init__(self, address=None, pubkey=None, prefix="BTS"):
        self.prefix = prefix
        if pubkey is not None :
            self._pubkey  = Base58(pubkey, prefix=prefix)
            self._address = None
        elif address is not None :
            self._pubkey  = None
            self._address = Base58(address, prefix=prefix)
        else :
            raise Exception("Address has to be initialized by either the " +
                            "pubkey or the address.")

    def derivesha256address(self):
        """ Derive address using ``RIPEMD160(SHA256(x))`` """
        pkbin         = unhexlify(repr(self._pubkey))
        addressbin    = ripemd160(hexlify(hashlib.sha256(pkbin).digest()))
        return Base58(hexlify(addressbin).decode('ascii'))

    def derivesha512address(self):
        """ Derive address using ``RIPEMD160(SHA512(x))`` """
        pkbin         = unhexlify(repr(self._pubkey))
        addressbin    = ripemd160(hexlify(hashlib.sha512(pkbin).digest()))
        return Base58(hexlify(addressbin).decode('ascii'))

    def __repr__(self) :
        """ Gives the hex representation of the ``GrapheneBase58CheckEncoded``
            Graphene address.
        """
        return repr(self.derivesha512address())

    def __str__(self) :
        """ Returns the readable Graphene address. This call is equivalent to
            ``format(Address, "BTS")``
        """
        return format(self, self.prefix)

    def __format__(self, _format) :
        """  May be issued to get valid "MUSE", "PLAY" or any other Graphene compatible
            address with corresponding prefix.
        """
        if self._address is None :
            if _format.lower() == "btc" :
                return format(self.derivesha256address(), _format)
            else :
                return format(self.derivesha512address(), _format)
        else :
            return format(self._address, _format)

    def __bytes__(self) :
        """ Returns the raw content of the ``Base58CheckEncoded`` address """
        if self._address is None :
            return bytes(self.derivesha512address())
        else :
            return bytes(self._address)


class PublicKey(Address):
    """ This class deals with Public Keys and inherits ``Address``.
        :param str pk: Base58 encoded public key
        Example:::
           PublicKey("BTS6UtYWWs3rkZGV8JA86qrgkG6tyFksgECefKE1MiH4HkLD8PFGL")
        .. note:: By default, graphene-based networks deal with **compressed**
                  public keys. If an **uncompressed** key is required, the
                  method ``unCompressed`` can be used::
                      PublicKey("xxxxx").unCompressed()
    """
    def __init__(self, pk, prefix=None):
        self.prefix  = prefix
        self._pk     = Base58(pk, prefix=prefix)
        self.address = Address(pubkey=pk, prefix=prefix)
        self.pubkey = self._pk

    def _derive_y_from_x(self, x, is_even):
        """ Derive y point from x point """
        curve = ecdsa.SECP256k1.curve
        # The curve equation over F_p is:
        #   y^2 = x^3 + ax + b
        a, b, p = curve.a(), curve.b(), curve.p()
        alpha = (pow(x, 3, p) + a * x + b) % p
        beta = ecdsa.numbertheory.square_root_mod_prime(alpha, p)
        if (beta % 2) != is_even :
            beta = p - beta
        return beta

    def unCompressed(self):
        """ Derive uncompressed key """
        public_key = repr(self._pk)
        prefix = public_key[0:2]
        if prefix == "04":
            return public_key
        assert prefix == "02" or prefix == "03"
        x = int(public_key[2:], 16)
        y = self._derive_y_from_x(x, (prefix == "02"))
        key = '04' + '%064x' % x + '%064x' % y
        return key

    def point(self) :
        """ Return the point for the public key """
        string = unhexlify(self.unCompressed())
        return ecdsa.VerifyingKey.from_string(string[1:], curve=ecdsa.SECP256k1).pubkey.point

    def __repr__(self) :
        """ Gives the hex representation of the Graphene public key. """
        return repr(self._pk)

    def __str__(self) :
        """ Returns the readable Graphene public key. This call is equivalent to
            ``format(PublicKey, "BTS")``
        """
        return format(self._pk, self.prefix)

    def __format__(self, _format) :
        """ Formats the instance of :doc:`Base58 <base58>` according to ``_format`` """
        return format(self._pk, _format)

    def __bytes__(self) :
        """ Returns the raw public key (has length 33)"""
        return bytes(self._pk)


class PrivateKey(PublicKey):
    """ Derives the compressed and uncompressed public keys and
        constructs two instances of ``PublicKey``:
        :param str wif: Base58check-encoded wif key
        Example:::
           PrivateKey("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd")
        Compressed vs. Uncompressed:
        * ``PrivateKey("w-i-f").pubkey``:
            Instance of ``PublicKey`` using compressed key.
        * ``PrivateKey("w-i-f").pubkey.address``:
            Instance of ``Address`` using compressed key.
        * ``PrivateKey("w-i-f").uncompressed``:
            Instance of ``PublicKey`` using uncompressed key.
        * ``PrivateKey("w-i-f").uncompressed.address``:
            Instance of ``Address`` using uncompressed key.
    """
    def __init__(self, wif=None):
        if wif is None :
            import os
            self._wif = Base58(hexlify(os.urandom(32)).decode('ascii'))
        elif isinstance(wif, Base58) :
            self._wif = wif
        else :
            self._wif = Base58(wif)
        # compress pubkeys only
        self._pubkeyhex, self._pubkeyuncompressedhex = self.compressedpubkey()
        self.pubkey               = PublicKey(self._pubkeyhex)
        self.uncompressed         = PublicKey(self._pubkeyuncompressedhex)
        self.uncompressed.address = Address(pubkey=self._pubkeyuncompressedhex)
        self.address              = Address(pubkey=self._pubkeyhex)

    def compressedpubkey(self):
        """ Derive uncompressed public key """
        secret = unhexlify(repr(self._wif))
        order  = ecdsa.SigningKey.from_string(secret, curve=ecdsa.SECP256k1).curve.generator.order()
        p      = ecdsa.SigningKey.from_string(secret, curve=ecdsa.SECP256k1).verifying_key.pubkey.point
        x_str  = ecdsa.util.number_to_string(p.x(), order)
        y_str  = ecdsa.util.number_to_string(p.y(), order)
        compressed   = hexlify(bytes(chr(2 + (p.y() & 1)), 'ascii') + x_str).decode('ascii')
        uncompressed = hexlify(bytes(chr(4), 'ascii') + x_str + y_str).decode('ascii')
        return([compressed, uncompressed])

    def __format__(self, _format) :
        """ Formats the instance of :doc:`Base58 <base58>` according to
            ``_format``
        """
        return format(self._wif, _format)

    def __repr__(self) :
        """ Gives the hex representation of the Graphene private key."""
        return repr(self._wif)

    def __str__(self) :
        """ Returns the readable (uncompressed wif format) Graphene private key. This
            call is equivalent to ``format(PrivateKey, "WIF")``
        """
        return format(self._wif, "WIF")

    def __bytes__(self) :
        """ Returns the raw private key """
        return bytes(self._wif)
