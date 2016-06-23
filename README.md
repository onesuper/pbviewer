# PBViewer

PBViewer is for inspecting fields from [Protocol Buffers](https://developers.google.com/protocol-buffers/) with the absense of `.proto` file.

It saves time of code-generating the message reader and does **NOT** depend on `protoc`.

## Example

```python
from pbviewer.protobuf_parser import parse_from_input_stream

# ss is the serialized data
fields = parse_from_input_stream(ss)

"""
====== Output =====
{1: 20150101, 2: 123, 4: "hello"}
""""
print fields

"""
====== Output =====
1	varint 	            20150101	4	D5 EE CD 09
2	varint 	                 123	1	7B
4	string 	hello               	6	05 68 65 6C 6C 6F
"""
for k,v in fields.items():
    print '{}\t{:7}\t{:20}\t{}\t{}'.format(k, v.type, v.value, v.size, v.hex)
```

## License

MIT