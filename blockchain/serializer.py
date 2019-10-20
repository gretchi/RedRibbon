
import struct


def serialize_block_data(previous_hash, index, author, timestamp, public_key, metadata, data):
    """
    Arguments:
        typedef struct {
            char[32] previous_hash;
            unsigned int64 index;
            char[16] author;
            char[32] timestamp;
            char[450] public_key;
            unsigned int32 metadata_length;
            char[] metadata;
            unsigned int32 data_length;
            char[] data;
        } block_data_t;

    Returns:
        bytes -- Serialized data
        int -- Data length
    """

    packed_header = struct.pack(
        ">32sQ16s32s450s"
        , previous_hash
        , index
        , author
        , timestamp
        , public_key
    )


    metadata_length = len(metadata)
    packed_metadata = struct.pack(
        f">I{metadata_length}s"
        , metadata_length
        , metadata
        )

    data_length = len(data)
    packed_data = struct.pack(
        f">I{data_length}s"
        , data_length
        , data
        )

    data = packed_header + packed_metadata + packed_data

    return data, len(data)



def serialize_block_container(version, hash, signature, data):
    """
    Arguments:
        struct {
            unsigned int32 block_length;
            unsigned int16 container_version;
            char[32] hash;
            char[256] signature;
            block_data_t data;
        };
    """

    data_length = len(data)
    data = struct.pack(
        f">H32s256s{data_length}s"
        , version
        , hash
        , signature
        , data)

    data_length = len(data)
    packed_data = struct.pack(
        f">I{data_length}s"
        , data_length
        , data)

    return packed_data, len(packed_data)


def deserialize_blocks(data):
    header = struct.unpack(">IH32s256s32sQ16s32s450s", data[:832])
    metadata_length = struct.unpack(">I", data[833:833+4])
    metadata = struct.unpack(f">{metadata_length}s")
    data_length = struct.unpack(">I", data[833+metadata_length:833+metadata_length+4])
    data = struct.unpack(f">{data_length}s")

    pass
