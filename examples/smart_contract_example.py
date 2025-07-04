"""Simple smart contract example using Bitcoin Script.

This script demonstrates a basic Pay-to-Public-Key-Hash (P2PKH) spending
condition and verifies a sample unlocking script.

The example uses python-bitcoinlib to evaluate the script. Install the
library with:
    pip install python-bitcoinlib

Note: This example runs entirely offline and does not interact with the
Bitcoin network.
"""

from bitcoin.core import (
    COutPoint,
    CScript,
    CTxIn,
    CTxOut,
    CTransaction,
    Hash160,
)
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.core.script import (
    OP_CHECKSIG,
    OP_DUP,
    OP_EQUALVERIFY,
    OP_HASH160,
    SignatureHash,
    SIGHASH_ALL,
)
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

    # Create the locking (output) script
    script_pub_key = create_p2pkh_script(Hash160(pubkey))

    # Build a dummy transaction
    tx = CTransaction([CTxIn(COutPoint(0, 0))], [CTxOut(0, script_pub_key)])

    # Create the unlocking (input) script by signing the transaction
    sighash = SignatureHash(script_pub_key, tx, 0, SIGHASH_ALL)
    signature = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    script_sig = CScript([signature, pubkey])
    tx.vin[0].scriptSig = script_sig

    # Verify the script
    VerifyScript(script_sig, script_pub_key, tx, 0, (SCRIPT_VERIFY_P2SH,))

    print(f"Spending from {address} succeeded")


if __name__ == "__main__":
    main()
