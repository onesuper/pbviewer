# Pbviewer

## Motivation

PBViewer is for inspecting fields from [Protocol Buffers](https://developers.google.com/protocol-buffers/) with the absense of `.proto` file.

It saves time of codegen (for Message reader) which means you do not need to install **protoc** on your machine.

## Install

From the source code:

```basic
$ git clone <url> 
$ cd pbviewer
$ python setup.py install
```

## Dependencies

Nothing! **Pbviewer** do not depend on any library, even python protobuf.

But unitest does require Nose and protobuf.

## Example

```python
from pbviewer import ParseFields

# `ss` is the serialized data
fields = ParseFields(ss)

"""
====== Output =====
{1: 20150101, 2: 123, 4: "hello"}
"""
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

## How it works?

**Pbviewer** simply parses bytes by guessing what they mean. 

More specifically, **Pbviewer** parses the fields based on the encoding rule of Protocol Buffers (a.k.a. wired format. Please refer to: https://developers.google.com/protocol-buffers/docs/encoding)

As a result, it can not tell difference among `int64`, `uint64` and `sint64`. It only sees "variant-length" integers. And it references fields by tag numbers instead of their literal names.

## License

MIT