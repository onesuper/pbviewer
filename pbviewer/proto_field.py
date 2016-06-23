
from wire_format import *

class ProtoField(object):

    def __init__(self, field_num, wire_type, value, rawbytes):
        self._field_num = field_num
        self._wire_type = wire_type
        self._value = value
        self._rawbytes = rawbytes


    def __repr__(self):
        if self._wire_type == WIRETYPE_VARINT:
            return str(self._value)
        elif self._wire_type == WIRETYPE_FIXED64:
            return str(self._value)
        elif self._wire_type == WIRETYPE_LENGTH_DELIMITED:
            return '"'+ str(self._value) + '"'
        elif self._wire_type == WIRETYPE_START_GROUP:
            return str(self._value)
        elif self._wire_type == WIRETYPE_END_GROUP:
            return str(self._value)
        elif self._wire_type == WIRETYPE_FIXED32:
            return str(self._value)
        else:
            raise TypeError()

    @property
    def value(self):
        return self._value
    
    @property
    def signed_value(self):
        if self._wire_type == WIRETYPE_VARINT:
            return self._to_signed_int64(self._value)
        else:
            return self._value
    
    @property
    def zigzag_value(self):
        if self._wire_type == WIRETYPE_VARINT:
            return ZigZagDecode(self._value)
        else:
            return self._value    

    @property    
    def type(self):
        if self._wire_type == WIRETYPE_VARINT:
            return 'varint'
        elif self._wire_type == WIRETYPE_FIXED64:
            return 'fixed64'
        elif self._wire_type == WIRETYPE_LENGTH_DELIMITED:
            return 'string'
        elif self._wire_type == WIRETYPE_START_GROUP:
            return 's_group'
        elif self._wire_type == WIRETYPE_END_GROUP:
            return 'e_group'
        elif self._wire_type == WIRETYPE_FIXED32:
            return 'fixed32'
        else:
            raise TypeError()
    
    @property
    def hex(self):
        return self._hexify_rawbytes(self._rawbytes)
    
    @property
    def size(self):
        return len(self._rawbytes)
    

    def _hexify_rawbytes(self, array):
        return ''.join( [ "%02X " % x for x in array ] ).strip()

    def _to_signed_int64(self, i):
        """convert a unsigned, 64-bit integer to
        a signed, 64-bit integer
        """
        if i > INT64_MAX:
            i -= (1 << 64)
        return i
