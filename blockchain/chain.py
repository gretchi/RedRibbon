
import os
import hashlib
import base64
import datetime
import json
import binascii
import struct

import digital_signature
from . import rrbc
from . import serializer

BLOCK_CHAIN_FILE_PATH = "./chain.json"
GENESIS_DATA = b"Genesis!"
VERSION = "1"


class Chain(object):
    def __init__(self, user_identity, secret_key, public_key):
        self._user_identity = user_identity.encode()
        self._secret_key = secret_key
        self._public_key = public_key
        self._block_chain_file_path = os.path.abspath(BLOCK_CHAIN_FILE_PATH)
        self._block_chain = self._load()
        self._genesis()


    def _genesis(self):
        if len(self._block_chain) == 0:
            self.push_block(GENESIS_DATA, is_genesis=True)


    def _load(self):
        if os.path.exists(self._block_chain_file_path) and os.path.getsize(self._block_chain_file_path) > 0:
            return rrbc.load(self._block_chain_file_path)

        return []

    def _if_necessary_save(self):
        if self._block_chain_file_path is not None:
            rrbc.save(self._block_chain_file_path)


    def sha256(self, data):
        return hashlib.sha256(data).digest()


    def encode(self, data):
        """Encode data to Base64

        Arguments:
            data {bytes} -- Target data

        Returns:
            str -- Base64 encoded data
        """
        encoded = base64.b64encode(data)
        return encoded


    def serialize(self, block_data):
        """Serialize a block data

        Arguments:
            block_data {dict} -- Block data

        Returns:
            str -- Serialized block data
        """
        print(len(block_data["public_key"]))
        print(type(self._public_key))


        serialized_block_data = struct.pack(
            ">IQ32s16s32s450s"
            , 0
            , 0
            , block_data["previous_hash"]
            , b"0000000000000000"
            , block_data["ts"].encode()
            , self._public_key
            )


        return serialized_block_data


    @property
    def _last_hash(self):
        chain_length = len(self._block_chain)

        if chain_length > 0:
            return self._block_chain[chain_length - 1]["hash"]

        return b"\x00" * 64


    def timestamp(self):
        """Generate a current timestamp

        Returns:
            bytes -- timestamp
        """

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        return now.isoformat(timespec="microseconds").encode()


    def push_block(self, data, **metadata):
        """Push block

        Arguments:
            data {bytes} -- Data
            mime_type {str} -- MIME Type
                Available types: https://www.iana.org/assignments/media-types/media-types.xhtml
            metadata {dict} -- Metadatas
        """
        # block_data = {
        #     "ts":
        #     , "v": VERSION
        #     , "author": self._user_identity
        #     , "previous_hash": self._last_hash
        #     , "data": encoded_data
        #     , "data_length": len(data)
        #     , "public_key": self._public_key
        #     , "metadata": json.dumps(metadata).encode()
        # }

        jsonfy_metadata = json.dumps(metadata).encode()
        encoded_data = self.encode(data)

        # Pack
        serialized_block_data, _ = serializer.serialize_block_data(
            self._last_hash
            , 0
            , self._user_identity
            , self.timestamp()
            , self._public_key
            , jsonfy_metadata
            , encoded_data)

        # print(serialized_block_data)


        # Hashing
        hash = self.sha256(serialized_block_data)

        # Signature
        signature = digital_signature.signature(self._secret_key, serialized_block_data)

        # Containerization
        serialized_block, _ = serializer.serialize_block_container(
            1
            , hash
            , signature
            , serialized_block_data
        )

        print(serialized_block)

        serializer.deserialize_blocks(serialized_block)

        # self._block_chain.append(block_data)
        # self._if_necessary_save(serialized_block)
