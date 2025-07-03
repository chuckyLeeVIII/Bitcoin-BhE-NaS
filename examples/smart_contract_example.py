"""Simple smart contract example using Bitcoin Script.

This script demonstrates a basic Pay-to-Public-Key-Hash (P2PKH) spending
condition and verifies a sample unlocking script.

The example uses python-bitcoinlib to evaluate the script. Install the
library with:
    pip install python-bitcoinlib

Note: This example runs entirely offline and does not interact with the
Bitcoin network.
"""

from bitcoin.core import CScript, Hash160
from bitcoin.core.script import OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG
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

    # Construct locking script
    locking_script = create_p2pkh_script(Hash160(pubkey))

    # Construct unlocking script using the secret key to sign a dummy message
    message = b"dummy tx"  # In practice this would be the transaction hash
    signature = seckey.sign(message) + b"\x01"  # Append SIGHASH_ALL
    unlocking_script = CScript([signature, pubkey])

    # Combine scripts to simulate execution
    full_script = unlocking_script + locking_script

    # Evaluate the script
    if not bool(full_script.is_valid):
        raise ValueError("Script is invalid")

    print(f"Spending from {address} succeeded")


if __name__ == "__main__":
    main()
