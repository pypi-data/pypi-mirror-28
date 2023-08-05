"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
import os
import struct


class PhoneCall(TLObject):
    CONSTRUCTOR_ID = 0xec82e140
    SUBCLASS_OF_ID = 0xd48afe4f

    def __init__(self, phone_call, users):
        """
        :param TLObject phone_call:
        :param list[TLObject] users:

        Constructor for phone.PhoneCall: Instance of PhoneCall.
        """
        super().__init__()

        self.phone_call = phone_call
        self.users = users

    def to_dict(self, recursive=True):
        return {
            'phone_call': (None if self.phone_call is None else self.phone_call.to_dict()) if recursive else self.phone_call,
            'users': ([] if self.users is None else [None if x is None else x.to_dict() for x in self.users]) if recursive else self.users,
        }

    def __bytes__(self):
        return b''.join((
            b'@\xe1\x82\xec',
            bytes(self.phone_call),
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.users)),b''.join(bytes(x) for x in self.users),
        ))

    @staticmethod
    def from_reader(reader):
        _phone_call = reader.tgread_object()
        reader.read_int()
        _users = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _users.append(_x)

        return PhoneCall(phone_call=_phone_call, users=_users)

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)
