# Pbviewer

## Motivation

**Pbviewer** (or **pbviewer**) is for inspecting fields from [Protocol Buffers](https://developers.google.com/protocol-buffers/) with the absense of `.proto` file.

It saves time of codegen (for Message reader) and installation of **protoc** on your machine.

## Installation

From the source code:

```basic
$ git clone <url> 
$ cd pbviewer
$ python setup.py install
```

## Example

```python
from pbviewer import ParseFields

# `ss` is the serialized data (file-like object)
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

## Dependencies

Nothing! **Pbviewer** do not depend on any library, even python protobuf.

But the unittest requires Nose and protobuf.

## How it works?

**Pbviewer** simply parses byte buffer by guessing what the bytes mean. 

More specifically, **pbviewer** parses the fields based on the encoding rule of Protocol Buffers (a.k.a. wired format. Please refer to: https://developers.google.com/protocol-buffers/docs/encoding). All code here is in pure python.

As a result, it can not tell difference among `int64`, `uint64` and `sint64`. It only sees "variant-length" integers. And it references all the fields by tag numbers instead of their literal names (appear in `.proto` file).

## License

MIT