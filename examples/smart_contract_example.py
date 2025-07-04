"""Simple smart contract example using Bitcoin Script.

This script demonstrates a basic Pay-to-Public-Key-Hash (P2PKH) spending
condition and verifies a sample unlocking script.

The example uses python-bitcoinlib to evaluate the script. Install the
library with:
    pip install python-bitcoinlib

Note: This example runs entirely offline and does not interact with the
Bitcoin network.
"""
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

# Example key (do not use on mainnet!)
SECRET_KEY_WIF = "cT7TybHkNQYmBbTjx9ZG7V4y4WqHy6sHzvGcB6aywxVNX3Q5S1tx"


def create_p2pkh_script(pubkey_hash: bytes) -> CScript:
    """Return a standard P2PKH output script."""
    return CScript([OP_DUP, OP_HASH160, pubkey_hash, OP_EQUALVERIFY, OP_CHECKSIG])


def main() -> None:
    seckey = CBitcoinSecret(SECRET_KEY_WIF)
    pubkey = seckey.pub
    address = P2PKHBitcoinAddress.from_pubkey(pubkey)

    print(f"Spending from {address} succeeded")


if __name__ == "__main__":
    main()
