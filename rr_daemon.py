#!/usr/bin/env python3

import uuid

from api import ApiService
from blockchain import Chain



def main():
    user_identity = str(uuid.uuid4()).lower()
    chain = Chain(user_identity)
    chain.push_block("うんち".encode())

    api_service = ApiService()
    api_service.run()


if __name__ == "__main__":
    main()
