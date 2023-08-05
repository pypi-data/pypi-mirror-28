"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
from ...utils import get_input_peer, get_input_channel, get_input_user, get_input_media, get_input_photo
import os
import struct


class DeletePhotosRequest(TLObject):
    CONSTRUCTOR_ID = 0x87cf7f2f
    SUBCLASS_OF_ID = 0x8918e168

    def __init__(self, id):
        """
        :param list[TLObject] id:

        :returns Vector<long>: This type has no constructors.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.id = [get_input_photo(_x) for _x in id]

    def to_dict(self, recursive=True):
        return {
            'id': ([] if self.id is None else [None if x is None else x.to_dict() for x in self.id]) if recursive else self.id,
        }

    def __bytes__(self):
        return b''.join((
            b'/\x7f\xcf\x87',
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.id)),b''.join(bytes(x) for x in self.id),
        ))

    @staticmethod
    def from_reader(reader):
        reader.read_int()
        _id = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _id.append(_x)

        return DeletePhotosRequest(id=_id)

    def on_response(self, reader):
        reader.read_int()  # Vector id
        count = reader.read_long()
        self.result = [reader.read_long() for _ in range(count)]

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)


class GetUserPhotosRequest(TLObject):
    CONSTRUCTOR_ID = 0x91cd32a8
    SUBCLASS_OF_ID = 0x27cfb967

    def __init__(self, user_id, offset, max_id, limit):
        """
        :param TLObject user_id:
        :param int offset:
        :param int max_id:
        :param int limit:

        :returns photos.Photos: Instance of either Photos, PhotosSlice.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.user_id = get_input_user(user_id)
        self.offset = offset
        self.max_id = max_id
        self.limit = limit

    def to_dict(self, recursive=True):
        return {
            'user_id': (None if self.user_id is None else self.user_id.to_dict()) if recursive else self.user_id,
            'offset': self.offset,
            'max_id': self.max_id,
            'limit': self.limit,
        }

    def __bytes__(self):
        return b''.join((
            b'\xa82\xcd\x91',
            bytes(self.user_id),
            struct.pack('<i', self.offset),
            struct.pack('<q', self.max_id),
            struct.pack('<i', self.limit),
        ))

    @staticmethod
    def from_reader(reader):
        _user_id = reader.tgread_object()
        _offset = reader.read_int()
        _max_id = reader.read_long()
        _limit = reader.read_int()
        return GetUserPhotosRequest(user_id=_user_id, offset=_offset, max_id=_max_id, limit=_limit)

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)


class UpdateProfilePhotoRequest(TLObject):
    CONSTRUCTOR_ID = 0xf0bb5152
    SUBCLASS_OF_ID = 0xc6338f7d

    def __init__(self, id):
        """
        :param TLObject id:

        :returns UserProfilePhoto: Instance of either UserProfilePhotoEmpty, UserProfilePhoto.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.id = get_input_photo(id)

    def to_dict(self, recursive=True):
        return {
            'id': (None if self.id is None else self.id.to_dict()) if recursive else self.id,
        }

    def __bytes__(self):
        return b''.join((
            b'RQ\xbb\xf0',
            bytes(self.id),
        ))

    @staticmethod
    def from_reader(reader):
        _id = reader.tgread_object()
        return UpdateProfilePhotoRequest(id=_id)

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)


class UploadProfilePhotoRequest(TLObject):
    CONSTRUCTOR_ID = 0x4f32c098
    SUBCLASS_OF_ID = 0xc292bd24

    def __init__(self, file):
        """
        :param TLObject file:

        :returns photos.Photo: Instance of Photo.
        """
        super().__init__()
        self.result = None
        self.content_related = True

        self.file = file

    def to_dict(self, recursive=True):
        return {
            'file': (None if self.file is None else self.file.to_dict()) if recursive else self.file,
        }

    def __bytes__(self):
        return b''.join((
            b'\x98\xc02O',
            bytes(self.file),
        ))

    @staticmethod
    def from_reader(reader):
        _file = reader.tgread_object()
        return UploadProfilePhotoRequest(file=_file)

    def on_response(self, reader):
        self.result = reader.tgread_object()

    def __str__(self):
        return TLObject.pretty_format(self)

    def stringify(self):
        return TLObject.pretty_format(self, indent=0)
