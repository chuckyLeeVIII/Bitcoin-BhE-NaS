# Examples

This directory contains examples demonstrating how features described by various
BIPs can be used.

## Smart Contract Example

Script for a Pay-to-Public-Key-Hash (P2PKH) contract using
`python-bitcoinlib`.

### Running the example

Install the dependency:

```bash
pip install python-bitcoinlib
```

Then execute the script:

```bash
python3 smart_contract_example.py
```

The script creates a dummy transaction, signs it, and verifies the script
entirely offline.
