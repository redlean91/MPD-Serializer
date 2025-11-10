# https://github.com/redlean91/MPD-Serializer
# MPD Serializer for Just Dance
# Serializer for Media Presentation Description files to Just Dance-like format

# Removed a few classes so i could make this public.

import struct

class UnsupportedType(Exception):
    def __init__(self, _type):
        self.type = _type
        super().__init__(f"Wrong/Unsupported type for operand: {_type}")

class CSerializerObject:
    @staticmethod
    def int8(_value=None):
        return struct.pack(">b", _value)

    @staticmethod
    def uint8(_value=None):
        return struct.pack(">B", _value)
    
    @staticmethod
    def int16(_value=None):
        return struct.pack(">h", _value)
    
    @staticmethod
    def uint16(_value=None):
        return struct.pack(">H", _value)
    
    @staticmethod
    def int32(_value=None):
        return struct.pack(">i", _value)

    @staticmethod
    def uint32(_value=None):
        return struct.pack(">I", _value)
    
    @staticmethod
    def float32(_value=None):
        return struct.pack(">f", _value)

    @staticmethod
    def String8(_value: str="",):
        if isinstance(_value, str):
            return CSerializerObject.uint32(len(_value)) + _value.encode(encoding="utf-8")
        else:
            raise UnsupportedType(_type="String8")

    @staticmethod
    def NULL(_value=None):
        return b''
