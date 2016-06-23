
from encoder import Encoder
from decoder import Decoder
from message import DecodeError
from wire_format import *
from proto_field import ProtoField

def parse_from_input_stream(input_stream):
    delta_bytes = 0 
    total_bytes = 0
    total_raw_bytes = 0
    
    d = Decoder(input_stream)

    fields = {}

    while True:
        try:
            (field_num, wire_type) = d.ReadFieldNumberAndWireType() 
        except EOFError:
            break

        filed_encoder = Encoder()  # encode the bytes back
        tag_bytes = d.Position() - total_bytes

        if wire_type == WIRETYPE_VARINT:
            uint64_value = d.ReadUInt64()
            filed_encoder.AppendUInt64(uint64_value)
            value = uint64_value
        elif wire_type == WIRETYPE_FIXED64:
            value = d.ReadDouble()
            filed_encoder.AppendDouble(value)
        elif wire_type == WIRETYPE_FIXED32:
            value = d.ReadFloat()
            filed_encoder.AppendFloat(value)
        elif wire_type == WIRETYPE_LENGTH_DELIMITED:
            value = d.ReadString()
            filed_encoder.AppendString(value)
        else:
            raise IOError()

        delta_bytes = d.Position() - total_bytes
        total_bytes = d.Position()
        raw_bytes = delta_bytes - tag_bytes
        total_raw_bytes += raw_bytes
        fields[field_num] = ProtoField(field_num, wire_type, value, filed_encoder.RawBuffer())
    return fields






