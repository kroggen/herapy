# -*- coding: utf-8 -*-

import ecdsa
import enum

from ..utils.encoding import encode_address, decode_address
from ..utils.converter import convert_bytes_to_public_key, \
    convert_public_key_to_bytes


MAX_NAME_ADDRESS_LEN = 12


@enum.unique
class GovernanceTxAddress(enum.Enum):
    SYSTEM = "aergo.system"
    NAME = "aergo.name"
    ENTERPRISE = "aergo.enterprise"


def check_name_address(addr):
    if len(addr) <= MAX_NAME_ADDRESS_LEN:
        return True
    elif addr in set(e.value for e in GovernanceTxAddress):
        return True
    else:
        return False


class Address:
    def __init__(self, pubkey, empty=False, curve=ecdsa.SECP256k1):
        self.__address = None
        self.__curve = curve
        self.__empty = empty

        if empty:
            return

        if pubkey is None:
            assert 1 == 0

        if isinstance(pubkey, str):
            pubkey = decode_address(pubkey)
        elif isinstance(pubkey, bytes):
            pubkey = convert_bytes_to_public_key(pubkey, curve=curve)

        self.__address = convert_public_key_to_bytes(pubkey=pubkey,
                                                     curve=curve,
                                                     compressed=True)

    def __str__(self):
        return encode_address(self.__address)

    def __bytes__(self):
        return self.__address

    @property
    def value(self):
        return self.__address

    @value.setter
    def value(self, v):
        if self.__empty:
            if isinstance(v, str):
                self.__address = decode_address(v)
            elif isinstance(v, bytes):
                self.__address = v
        else:
            raise ValueError('Cannot set a value for the derived address')

    @property
    def curve(self):
        return self.__curve

    @property
    def public_key(self):
        return convert_bytes_to_public_key(self.__address, curve=self.__curve)
