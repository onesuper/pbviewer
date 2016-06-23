#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import unittest

from pbviewer.encoder import Encoder
from pbviewer.decoder import Decoder
from pbviewer.wire_format import *

import io

class Test(unittest.TestCase):

    def testEncodeAndDecode(self):
        encoder = Encoder()
        encoder.AppendTag(0, WIRETYPE_VARINT)
        encoder.AppendInt32(2**20)
        encoder.AppendTag(1, WIRETYPE_VARINT)
        encoder.AppendSInt64(-2**40)
        encoder.AppendTag(2, WIRETYPE_LENGTH_DELIMITED)
        encoder.AppendString("hello")
        encoder.AppendTag(3, WIRETYPE_VARINT)
        encoder.AppendBool(True)
        encoder.AppendTag(4, WIRETYPE_FIXED64)
        encoder.AppendDouble(0.31415926)
        encoder.AppendTag(5, WIRETYPE_VARINT)
        encoder.AppendUInt32(2**30)
        encoder.AppendTag(6, WIRETYPE_VARINT)
        encoder.AppendUInt64(2**40)
        buffer_size = len(encoder)

        tube = io.BytesIO(encoder.ToString())
        decoder = Decoder(tube)
        self.assertEquals((0, WIRETYPE_VARINT), decoder.ReadFieldNumberAndWireType())
        self.assertEquals(2**20, decoder.ReadInt32())
        self.assertEquals((1, WIRETYPE_VARINT), decoder.ReadFieldNumberAndWireType())
        self.assertEquals(-2**40, decoder.ReadSInt64())
        self.assertEquals((2, WIRETYPE_LENGTH_DELIMITED), decoder.ReadFieldNumberAndWireType())
        self.assertEquals("hello", decoder.ReadString())
        self.assertEquals((3, WIRETYPE_VARINT), decoder.ReadFieldNumberAndWireType())
        self.assertEquals(True, decoder.ReadBool())
        self.assertEquals((4, WIRETYPE_FIXED64), decoder.ReadFieldNumberAndWireType())
        self.assertEquals(0.31415926, decoder.ReadDouble())
        self.assertEquals((5, WIRETYPE_VARINT), decoder.ReadFieldNumberAndWireType())
        self.assertEquals(2**30, decoder.ReadUInt32())
        self.assertEquals((6, WIRETYPE_VARINT), decoder.ReadFieldNumberAndWireType())
        self.assertEquals(2**40, decoder.ReadUInt64())
        self.assertEquals(buffer_size, decoder.Position())

if __name__ == '__main__':
    unittest.main()
