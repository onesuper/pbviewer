# Protocol Buffers - Google's data interchange format
# Copyright 2008 Google Inc.
# http://code.google.com/p/protobuf/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This implementation is modified from google's original Protobuf implementation.
The original author is: robinson@google.com (Will Robinson).
Modified by onesuperclark@gmail.com(onesuper).
"""

import struct
import input_stream
import wire_format


class Decoder(object):
    """Decodes logical protocol buffer fields from the wire."""

    def __init__(self, input):
        """Initializes the decoder to read from input stream.
        """
        self._stream = input_stream.InputStream(input)

    def Position(self):
        """Returns the 0-indexed position in |s|."""
        return self._stream.Position()

    def ReadFieldNumberAndWireType(self):
        """Reads a tag from the wire. Returns a (field_number, wire_type) pair."""
        tag_and_type = self.ReadUInt32()
        return wire_format.UnpackTag(tag_and_type)

    def ReadInt32(self):
        """Reads and returns a signed, varint-encoded, 32-bit integer."""
        return self._stream.ReadVarint32()

    def ReadInt64(self):
        """Reads and returns a signed, varint-encoded, 64-bit integer."""
        return self._stream.ReadVarint64()

    def ReadUInt32(self):
        """Reads and returns an signed, varint-encoded, 32-bit integer."""
        return self._stream.ReadVarUInt32()

    def ReadUInt64(self):
        """Reads and returns an signed, varint-encoded,64-bit integer."""
        return self._stream.ReadVarUInt64()

    def ReadSInt32(self):
        """Reads and returns a signed, zigzag-encoded, varint-encoded,
        32-bit integer."""
        return wire_format.ZigZagDecode(self._stream.ReadVarUInt32())

    def ReadSInt64(self):
        """Reads and returns a signed, zigzag-encoded, varint-encoded,
        64-bit integer."""
        return wire_format.ZigZagDecode(self._stream.ReadVarUInt64())

    def ReadFixed32(self):
        """Reads and returns an unsigned, fixed-width, 32-bit integer."""
        return self._stream.ReadLittleEndian32()

    def ReadFixed64(self):
        """Reads and returns an unsigned, fixed-width, 64-bit integer."""
        return self._stream.ReadLittleEndian64()

    def ReadSFixed32(self):
        """Reads and returns a signed, fixed-width, 32-bit integer."""
        value = self._stream.ReadLittleEndian32()
        if value >= (1 << 31):
            value -= (1 << 32)
        return value

    def ReadSFixed64(self):
        """Reads and returns a signed, fixed-width, 64-bit integer."""
        value = self._stream.ReadLittleEndian64()
        if value >= (1 << 63):
            value -= (1 << 64)
        return value

    def ReadFloat(self):
        """Reads and returns a 4-byte floating-point number."""
        serialized = self._stream.ReadString(4)
        return struct.unpack('f', serialized)[0]

    def ReadDouble(self):
        """Reads and returns an 8-byte floating-point number."""
        serialized = self._stream.ReadString(8)
        return struct.unpack('d', serialized)[0]

    def ReadBool(self):
        """Reads and returns a bool."""
        i = self._stream.ReadVarUInt32()
        return bool(i)

    def ReadEnum(self):
        """Reads and returns an enum value."""
        return self._stream.ReadVarUInt32()

    def ReadString(self):
        """Reads and returns a length-delimited string."""
        length = self._stream.ReadVarUInt32()
        return self._stream.ReadString(length)

    def ReadBytes(self):
        """Reads and returns a length-delimited byte sequence."""
        return self.ReadString()

    def ReadVarint(self):
        return self._stream._ReadVarintHelper()
