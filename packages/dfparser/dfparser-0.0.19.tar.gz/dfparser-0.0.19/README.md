# python-df-parser

Python parser for [dataforge envelope](http://npm.mipt.ru/dataforge/) format.
Envelope format designed to transport and store tuples with binary data and
metadata in a single packet [more info](http://npm.mipt.ru/dataforge/docs.html#envelope_format).

Implementation currently supports:
  - Parse and serialize metadata in JSON format.
  - Handle 0x14000 and DF02 protocol versions.
  - Transparent binary data compression (only zlib supported)

## Installation
Latest version on PyPi can be installed by command `pip3 install dfparser`

## Usage
#### Create simple message
  - 0x14000 protocol version
        >>> import dfparser
        >>> dfparser.create_message({"param": "abc"}, data=b'bnary')
        b'#!\x00\x01@\x00pY_2\x00\x01\x00\x00\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x05!#\r\n{\n    "param": "abc"\n}\r\n\r\nbnary'
  - DF02 version
        >>> import dfparser
        >>> dfparser.create_message({"param": "abc"}, b'binary', version=b'DF02')
        b'#~DF02JS\x00\x00\x00\x1a\x00\x00\x00\x06~#\r\n{\n    "param": "abc"\n}\r\n\r\nbinary'

#### Parse message
  - From file
        >>> import dfparser
        >>> header, meta, data = envelope_parser.parse_from_file("df02.df")
        >>> # Or read only metadata
        >>> header, meta, _ = envelope_parser.parse_from_file("df02.df", nodata=True)
  - From bytes
        >>> import dfparser
        >>> data = b'#~DF02JS\x00\x00\x00\x1a\x00\x00\x00\x06~#\r\n{\n    "param": "abc"\n}\r\n\r\nbinary'
        >>> envelope_parser.parse_message(data)
        ({'data_len': 6, 'meta_len': 26, 'meta_type': b'JS', 'type': b'DF02'},
         {'param': 'abc'},
         b'binary')

  - From stream
        >>> import dfparser
        >>> # stream.df contains multiple messages sequentaly written
        >>> data = open("/home/chernov/stream.df", 'rb').read()
        >>> dfparser.get_messages_from_stream(data)
        ([{'data': b'bnary',
           'header': {'data_len': 5,
            'data_type': 0,
            'meta_len': 26,
            'meta_type': 65536,
            'time': 1885524830,
            'type': b'\x00\x01@\x00'},
           'meta': {'param': 'abc'}},
          {'data': b'binary',
           'header': {'data_len': 6,
            'meta_len': 26,
            'meta_type': b'JS',
            'type': b'DF02'},
           'meta': {'param': 'abc'}}],
         b'')

### Transparent compression
  To apply transparent compression to message meta should contains field `"compression": "zlib"`
    >>> import dfparser
    >>> data = b''.join(b'0' for _ in range(100))
    >>> compr = dfparser.create_message({"compression": "zlib"}, data)
    >>> compr
    b'#!\x00\x01@\x00pt\xf7\xa7\x00\x01\x00\x00\x00\x00\x00!\x00\x00\x00\x00\x00\x00\x00\x0c!#\r\n{\n    "compression": "zlib"\n}\r\n\r\nx\x9c30\xa0=\x00\x00\xb3q\x12\xc1'
    >>> _, _, decompr = envelope_parser.parse_message(compr)
    >>> data == decompr
    True

## Build
        # Update protobuf formats use:
        #(Protobuf 3.2.0+)[https://github.com/google/protobuf/releases] should
        # be installed and be in $PATH
        cd configs && protoc rsb_event.proto  --python_out ../ && cd ..
        python3 setup.py build
