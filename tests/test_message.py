
import unittest
from proto import test_message_pb2
from pbviewer.protobuf_parser import parse_from_input_stream



class Test(unittest.TestCase):

    def testMessage(self):
        pb = test_message_pb2.TestRef()
        pb.field1 = 20150101
        pb.field2 = 123
        pb.field4 = "hello"
        s = pb.SerializeToString()

        import io
        tube = io.BytesIO(s)
        fields = parse_from_input_stream(tube)

        self.assertEquals(20150101, fields[1].value)
        self.assertEquals(123, fields[2].value)
        self.assertFalse(fields.has_key(3))
        self.assertEquals("hello", fields[4].value)

if __name__ == '__main__':
    unittest.main()
