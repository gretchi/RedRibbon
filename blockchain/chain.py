
import os
import hashlib
import base64
import datetime
import json
import binascii

import digital_signature

BLOCK_CHAIN_FILE_PATH = "./chain.json"
GENESIS_DATA = b"Genesis!"
VERSION = "1"


class Chain(object):
    def __init__(self, user_identity, secret_key, public_key):
        self._user_identity = user_identity
        self._secret_key = secret_key
        self._public_key = public_key
        self._block_chain_file_path = os.path.abspath(BLOCK_CHAIN_FILE_PATH)
        self._block_chain = self._load()
        self._genesis()


    def _genesis(self):
        if len(self._block_chain) == 0:
            self.push_block(GENESIS_DATA)


    def _load(self):
        if os.path.exists(self._block_chain_file_path) and os.path.getsize(self._block_chain_file_path) > 0:

            with open(self._block_chain_file_path, "r") as fh:
                return json.load(fh)

        return []

    def _if_necessary_save(self):
        if self._block_chain_file_path is not None:
            self._save()


    def _save(self):
        with open(self._block_chain_file_path, "w") as fh:
            json.dump(self._block_chain, fh)


    def sha256(self, data):
        return hashlib.sha256(data).hexdigest()


    def encode(self, data):
        """Encode data to Base64

        Arguments:
            data {bytes} -- Target data

        Returns:
            str -- Base64 encoded data
        """
        encoded = base64.b64encode(data).decode()
        return encoded


    def serialize(self, block_data):
        """Serialize a block data

        Arguments:
            block_data {dict} -- Block data

        Returns:
            str -- Serialized block data
        """
        serialized_block_data = json.dumps(block_data)
        return serialized_block_data


    @property
    def _last_hash(self):
        chain_length = len(self._block_chain)

        if chain_length > 0:
            return self._block_chain[chain_length - 1]["hash"]

        return "0" * 64


    def push_block(self, data, **metadata):
        """Push block

        Arguments:
            data {bytes} -- Data
            mime_type {str} -- MIME Type
                Available types: https://www.iana.org/assignments/media-types/media-types.xhtml
            metadata {dict} -- Metadatas
        """
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        ts = now.isoformat(timespec="microseconds")
        encoded_data = self.encode(data)

        block_data = {
            "ts": ts
            , "v": VERSION
            , "author": self._user_identity
            , "previous_hash": self._last_hash
            , "data": encoded_data
            , "data_length": len(data)
            , "public_key": str(binascii.hexlify(self._public_key), "ascii")
            , "metadata": metadata
        }


        # Hashing
        serialized_block_data = self.serialize(block_data)
        hash = self.sha256(serialized_block_data.encode())
        block_data["hash"] = hash

        # Signature
        serialized_block_data = self.serialize(block_data).encode()
        signature = digital_signature.signature(self._secret_key, serialized_block_data)
        block_data["signature"] = str(binascii.hexlify(signature), "ascii")

        print(len(signature))

        self._block_chain.append(block_data)
        self._if_necessary_save()
