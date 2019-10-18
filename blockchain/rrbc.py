
import struct

HEADER_SIGNATURE = b"\x52\x52\x42\x43"
CONTAINER_VERSION = 1

CONTAINER_HEADER_SEQ = 0
CONTAINER_HEADER_LENGTH = 24
CONTAINER_HEADER_FORMAT = ">4sB3xQQ"


def _unpack(fh):
    sequance = HEADER_SIGNATURE

    base_pointer = 0x00
    pointer = 0x00

    read_data = fh.read(CONTAINER_HEADER_LENGTH)
    print(len(read_data), read_data)

    data = struct.unpack(CONTAINER_HEADER_FORMAT, read_data)

    print(data)
    pointer += CONTAINER_HEADER_LENGTH


def _pack(fh):
    data = struct.pack(
        CONTAINER_HEADER_FORMAT
        , HEADER_SIGNATURE
        , CONTAINER_VERSION
        , 0
        , 0)

    fh.write(data)


def load(path):
    with open(path, "rb") as fh:
        _unpack(fh)



def save(path):
    with open(path, "wb") as fh:
        _pack(fh)
