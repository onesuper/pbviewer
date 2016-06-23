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
import message
import wire_format
import output_stream


class Encoder(object):
    """Encodes logical protocol buffer fields to the wire format."""

    def __init__(self):
        self._stream = output_stream.OutputStream()

    def ToString(self):
        """Returns all values encoded in this object as a string."""
        return self._stream.ToString()

    def RawBuffer(self):
        return self._stream.RawBuffer()

    def __len__(self):
        return len(self._stream)

    def AppendTag(self, field_number, wire_type):
        """Appends a tag containing field number and wire type information."""
        self._stream.AppendVarUInt32(wire_format.PackTag(field_number, wire_type))

    def AppendInt32(self, value):
        """Appends a 32-bit integer to our buffer, varint-encoded."""
        self._stream.AppendVarint32(value)

    def AppendInt64(self, value):
        """Appends a 64-bit integer to our buffer, varint-encoded."""
        self._stream.AppendVarint64(value)

    def AppendUInt32(self, unsigned_value):
        """Appends an unsigned 32-bit integer to our buffer, varint-encoded."""
        self._stream.AppendVarUInt32(unsigned_value)

    def AppendUInt64(self, unsigned_value):
        """Appends an unsigned 64-bit integer to our buffer, varint-encoded."""
        self._stream.AppendVarUInt64(unsigned_value)

    def AppendSInt32(self, value):
        """Appends a 32-bit integer to our buffer, zigzag-encoded and then
        varint-encoded.
        """
        zigzag_value = wire_format.ZigZagEncode(value)
        self._stream.AppendVarUInt32(zigzag_value)

    def AppendSInt64(self, value):
        """Appends a 64-bit integer to our buffer, zigzag-encoded and then
        varint-encoded.
        """
        zigzag_value = wire_format.ZigZagEncode(value)
        self._stream.AppendVarUInt64(zigzag_value)

    def AppendFixed32(self, unsigned_value):
        """Appends an unsigned 32-bit integer to our buffer, in little-endian
        byte-order.
        """
        self._stream.AppendLittleEndian32(unsigned_value)

    def AppendFixed64(self, unsigned_value):
        """Appends an unsigned 64-bit integer to our buffer, in little-endian
        byte-order.
        """
        self._stream.AppendLittleEndian64(unsigned_value)

    def AppendSFixed32(self, value):
        """Appends a signed 32-bit integer to our buffer, in little-endian
        byte-order.
        """
        sign = (value & 0x80000000) and -1 or 0
        if value >> 32 != sign:
            raise message.EncodeError('SFixed32 out of range: %d' % value)
        self._stream.AppendLittleEndian32(value & 0xffffffff)

    def AppendSFixed64(self, value):
        """Appends a signed 64-bit integer to our buffer, in little-endian
        byte-order.
        """
        sign = (value & 0x8000000000000000) and -1 or 0
        if value >> 64 != sign:
            raise message.EncodeError('SFixed64 out of range: %d' % value)
        self._stream.AppendLittleEndian64(value & 0xffffffffffffffff)

    def AppendFloat(self, value):
        """Appends a floating-point number to our buffer."""
        self._stream.AppendRawBytes(struct.pack('f', value))

    def AppendDouble(self, value):
        """Appends a double-precision floating-point number to our buffer."""
        self._stream.AppendRawBytes(struct.pack('d', value))

    def AppendBool(self, value):
        """Appends a boolean to our buffer."""
        self.AppendInt32(value)

    def AppendEnum(self, value):
        """Appends an enum value to our buffer."""
        self.AppendInt32(value)

    def AppendString(self, value):
        """Appends a length-prefixed string to our buffer, with the
        length varint-encoded.
        """
        self._stream.AppendVarUInt32(len(value))
        self._stream.AppendRawBytes(value)

    def AppendBytes(self, value):
        """Appends a length-prefixed sequence of bytes to our buffer, with the
        length varint-encoded.
        """
        self.AppendString(value)
