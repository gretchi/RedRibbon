
import os
import hashlib
import base64
import datetime
import json

BLOCK_CHAIN_FILE_PATH = "./chain.json"
GENESIS_DATA = b"Genesis!"

class Chain(object):
    def __init__(self, user_identity):
        self._user_identity = user_identity
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


    def push_block(self, data):
        """Push block

        Arguments:
            data {bytes} -- Data
        """
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        ts = now.isoformat(timespec="microseconds")

        block_data = {
            "ts": ts,
            "author": self._user_identity,
            "previous_hash": self._last_hash,
            "data": self.encode(data)
        }


        serialized_block_data = self.serialize(block_data)

        hash = self.sha256(serialized_block_data.encode())
        block_data["hash"] = hash

        self._block_chain.append(block_data)
        self._save()
