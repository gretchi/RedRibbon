
import os
import uuid
import json
import binascii

import digital_signature

USER_INFO_JSON_PATH = "./user.json"

class User(object):
    def __init__(self):
        self._user_info_json_path = os.path.abspath(USER_INFO_JSON_PATH)

        self._user_info = self._load()

        if self._user_info == None:
            self.generate_user()


    def _load(self):
        if os.path.exists(self._user_info_json_path) and os.path.getsize(self._user_info_json_path) > 0:
            with open(self._user_info_json_path, "r") as fh:
                return json.load(fh)

        return None


    def _save(self):
        with open(self._user_info_json_path, "w") as fh:
            json.dump(self._user_info, fh)


    def generate_user(self):
        identity = str(uuid.uuid4()).lower()
        secret_key_bytes, public_key_bytes = digital_signature.generate_key()

        secret_key = str(binascii.hexlify(secret_key_bytes), "ascii")
        public_key = str(binascii.hexlify(public_key_bytes), "ascii")

        self._user_info = {
            "identity": identity
            , "secret_key": secret_key
            , "public_key": public_key
        }

        self._save()


    @property
    def identity(self):
        return self._user_info["identity"]

    @property
    def secret_key(self):
        return binascii.unhexlify(self._user_info["secret_key"])

    @property
    def public_key(self):
        return binascii.unhexlify(self._user_info["public_key"])
