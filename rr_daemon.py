#!/usr/bin/env python3

from api import ApiService
from blockchain import Chain
from user import User


def main():
    user = User()
    chain = Chain(user.identity, user.secret_key, user.public_key)
    chain.push_block("".encode())

    # api_service = ApiService()
    # api_service.run()


if __name__ == "__main__":
    main()
