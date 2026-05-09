# Nexus Security Layers

Status: CODE_NEEDS_TEST  
Routing: LOCAL_DRY_RUN_ONLY  
Deployment gate: CLOSED  

## Security Model

Prepare Security Model for local dry-run validation.

## WAL / Crypto Statement

Implement append-only WAL and cryptographic verification in local test mode only.

## Bridge Rule

Arweave bridge is treated as:

ED25519_ATTESTS_RSA_OWNER_ONLY

Rejected mappings:

- ED25519_SIG_TO_RSA_SIG
- RSA_SIG_TO_ED25519_R_S

## Blocks

- no private key output
- no seed phrase handling
- no Arweave upload
- no IPFS pin
- no autonomous execution
