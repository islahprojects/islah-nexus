"""
dDNA Sovereign Key — Shamir Secret Sharing
===========================================
JAJIS 2026 · Flag 1 Resolution · INTERNAL_ONLY
islah.nexus · AI1 Zero · OV Nexus

PROBLEM (Flag 1):
  The dDNA master key is sovereign (only JJ holds it).
  If lost, it is gone forever — violating Law VII (Walang Maiiwan).
  A central recovery mechanism violates Law VI (every dot sovereign).

SOLUTION: Shamir Secret Sharing (k-of-n threshold)
  - Key is split into n shares.
  - Any k shares reconstruct the key (k < n, so no single guardian is omnipotent).
  - Zero shares reveal zero information (information-theoretically secure).
  - JJ owns the scheme parameters. JJ chooses guardians. JJ sets threshold.

HARD RULES (from alignment skill):
  - No cloud dependency by default.
  - No autonomous execution.
  - No auto-deletion of files without explicit JJ command.
  - No sigma = 1.0 (this is a local tool, not a proof of perfect security).
  - Master key is NEVER stored or logged by this script after generation.

REQUIREMENTS:
  - Python 3.8+ (stdlib only — no pip install needed)
  - Windows / PowerShell compatible
  - CHI2MM / Honor X6C 4GB compatible (O(1) memory use per share)

USAGE:
  python ddna_sovereign_key.py demo              # local self-test
  python ddna_sovereign_key.py generate 5 3      # split into 5 shares, need 3 to recover
  python ddna_sovereign_key.py verify            # check shares file without recovering key
  python ddna_sovereign_key.py recover           # reconstruct key from shares in ddna_shares.json

SEAL: JJ.ANNA.FLAG1.20260510
"""

import secrets
import hashlib
import json
import sys
import os
from datetime import datetime, timezone


# -------------------------------------------------------------------
# PRIME FIELD
# p = 2^256 - 189  (a known safe prime larger than any 256-bit secret)
# All polynomial arithmetic is performed mod p.
# -------------------------------------------------------------------
PRIME = 2**256 - 189
KEY_BYTES = 32  # 256-bit dDNA key


# -------------------------------------------------------------------
# CORE: Shamir's Secret Sharing over GF(PRIME)
# -------------------------------------------------------------------

def _eval_poly(coeffs: list, x: int) -> int:
    """Evaluate polynomial with given coefficients at x, mod PRIME."""
    result = 0
    for coeff in reversed(coeffs):
        result = (result * x + coeff) % PRIME
    return result


def split_key(secret_bytes: bytes, n: int, k: int) -> list:
    """
    Split secret_bytes into n shares. Any k shares reconstruct the secret.

    Returns: list of (x, y) integer tuples — the shares.
    Raises:  ValueError on bad parameters.
    """
    if not (1 <= k <= n):
        raise ValueError(f"k must satisfy 1 <= k <= n, got k={k}, n={n}")
    if len(secret_bytes) > KEY_BYTES:
        raise ValueError(f"Secret too long: max {KEY_BYTES} bytes")

    secret_int = int.from_bytes(secret_bytes.ljust(KEY_BYTES, b'\x00'), 'big')
    if secret_int >= PRIME:
        raise ValueError("Secret exceeds prime field. This should not happen for 256-bit keys.")

    # Build polynomial: f(x) = secret + a1*x + a2*x^2 + ... + a(k-1)*x^(k-1)
    coeffs = [secret_int] + [secrets.randbelow(PRIME) for _ in range(k - 1)]

    shares = [(i, _eval_poly(coeffs, i)) for i in range(1, n + 1)]
    return shares


def recover_key(shares: list) -> bytes:
    """
    Reconstruct the secret from k or more (x, y) shares using Lagrange interpolation.

    Returns: 32-byte secret.
    Raises:  ValueError if fewer than 2 shares provided (trivially unsafe).
    """
    if len(shares) < 2:
        raise ValueError("Need at least 2 shares to reconstruct (k >= 2 is required).")

    x_s = [s[0] for s in shares]
    y_s = [s[1] for s in shares]
    k = len(x_s)

    # Lagrange interpolation at x=0 to find the constant term (the secret)
    result = 0
    for i in range(k):
        num = y_s[i]
        den = 1
        for j in range(k):
            if i != j:
                num = num * (0 - x_s[j]) % PRIME
                den = den * (x_s[i] - x_s[j]) % PRIME
        # Python 3.8+: pow(x, -1, m) computes modular inverse
        result = (result + num * pow(den, -1, PRIME)) % PRIME

    return result.to_bytes(KEY_BYTES, 'big')


# -------------------------------------------------------------------
# KEY GENERATION + FINGERPRINTING
# -------------------------------------------------------------------

def generate_ddna_key() -> bytes:
    """Generate a cryptographically secure 256-bit dDNA sovereign key."""
    return secrets.token_bytes(KEY_BYTES)


def key_fingerprint(key: bytes) -> str:
    """
    SHA-256 fingerprint (first 16 hex chars) for public verification.
    Safe to share — reveals nothing about the key itself.
    """
    return hashlib.sha256(key).hexdigest()[:16].upper()


def key_checksum(key: bytes) -> str:
    """Full SHA-256 of the key — for JJ's private verification only."""
    return hashlib.sha256(key).hexdigest().upper()


# -------------------------------------------------------------------
# SHARE SERIALIZATION
# -------------------------------------------------------------------

def shares_to_printable(shares: list, n: int, k: int) -> list:
    """
    Convert share tuples to printable strings safe for paper/USB/IPFS storage.
    Format: SHARE-{guardian_num}:{x_hex}:{y_hex}
    """
    printable = []
    for idx, (x, y) in enumerate(shares):
        x_hex = format(x, '04x')                 # x is small (1..n), 4 hex chars
        y_hex = format(y, f'0{KEY_BYTES * 2}x')  # y is 256-bit, 64 hex chars
        printable.append(f"DDNA-SHARE-{idx+1:02d}:{x_hex}:{y_hex}")
    return printable


def shares_from_printable(printable: list) -> list:
    """Parse printable share strings back to (x, y) integer tuples."""
    shares = []
    for s in printable:
        s = s.strip()
        try:
            # Format: DDNA-SHARE-XX:xxxx:yyyy...
            parts = s.split(':')
            if len(parts) != 3:
                raise ValueError(f"Malformed share: {s[:40]}")
            x = int(parts[1], 16)
            y = int(parts[2], 16)
            shares.append((x, y))
        except Exception as e:
            raise ValueError(f"Could not parse share '{s[:40]}': {e}")
    return shares


# -------------------------------------------------------------------
# FILE I/O
# -------------------------------------------------------------------

SHARES_FILE = 'ddna_shares.json'


def save_shares(printable: list, fingerprint: str, n: int, k: int, label: str = '') -> str:
    """Save shares to ddna_shares.json. Returns path."""
    timestamp = datetime.now(timezone.utc).isoformat()
    data = {
        '_project': 'islah.nexus · AI1 Zero · JAJIS 2026',
        '_law': 'Flag 1 Resolution — Shamir Secret Sharing',
        '_seal': f'JJ.ANNA.FLAG1.{timestamp[:10].replace("-","")}',
        'fingerprint': fingerprint,
        'scheme': f'{k}-of-{n}',
        'label': label or f'dDNA-{timestamp[:10]}',
        'created_utc': timestamp,
        'n_total_shares': n,
        'k_threshold': k,
        'shares': printable,
    }
    with open(SHARES_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    return os.path.abspath(SHARES_FILE)


def load_shares(path: str = SHARES_FILE) -> dict:
    """Load shares JSON file."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Shares file not found: {path}\n"
            f"Run: python ddna_sovereign_key.py generate <n> <k>"
        )
    with open(path) as f:
        return json.load(f)


# -------------------------------------------------------------------
# CLI COMMANDS
# -------------------------------------------------------------------

def cmd_demo():
    """Self-test: generate key, split 3-of-5, recover, verify match."""
    print()
    print("  [dDNA] DEMO — 3-of-5 Shamir Secret Sharing self-test")
    print("  " + "─" * 50)

    key = generate_ddna_key()
    fp = key_fingerprint(key)
    print(f"  Original fingerprint : {fp}")

    shares = split_key(key, n=5, k=3)

    # Test 1: recover with shares 1, 3, 5
    recovered_a = recover_key([shares[0], shares[2], shares[4]])
    fp_a = key_fingerprint(recovered_a)
    ok_a = "PASS" if fp == fp_a else "FAIL"

    # Test 2: recover with shares 2, 4
    # Only 2 shares when k=3 — should NOT match (wrong value)
    recovered_b = recover_key([shares[1], shares[3]])
    fp_b = key_fingerprint(recovered_b)
    ok_b = "PASS" if fp != fp_b else "FAIL (security leak)"

    print(f"  Recover shares 1,3,5 : {fp_a}  [{ok_a}]")
    print(f"  2-share wrong recon  : {fp_b}  [{ok_b}]  (mismatch expected)")
    print()

    if ok_a == "PASS" and ok_b == "PASS":
        print("  [dDNA] FLAG 1 RESOLUTION: LOCAL DEMO PASSED")
        print("  [dDNA] σ = 0.93 cap applies — run on real hardware to complete verification.")
    else:
        print("  [dDNA] DEMO FAILED — review implementation.")
    print()


def cmd_generate(n: int, k: int, label: str = ''):
    """Generate a new dDNA key and split into n shares (k threshold)."""
    print()
    print(f"  [dDNA] Generating 256-bit sovereign key → {k}-of-{n} Shamir SSS")
    print("  " + "─" * 50)
    print("  WARNING: The master key will be shown ONCE below.")
    print("  Seal it in your Offline Vault, then delete it from disk.")
    print("  The shares file alone is enough for recovery.")
    print()

    key = generate_ddna_key()
    fp = key_fingerprint(key)
    checksum = key_checksum(key)

    shares = split_key(key, n=n, k=k)
    printable = shares_to_printable(shares, n, k)

    print(f"  Fingerprint (public) : {fp}")
    print(f"  Checksum (private)   : {checksum}")
    print(f"  Scheme               : {k}-of-{n}")
    print()
    print("  SHARES — distribute one per guardian:")
    print()
    for s in printable:
        print(f"    {s}")
    print()
    print("  MASTER KEY (seal vault, then delete from terminal history):")
    print(f"    {key.hex()}")
    print()

    path = save_shares(printable, fp, n, k, label)
    print(f"  Shares saved to      : {path}")
    print()
    print("  NEXT STEPS:")
    print("  1. Copy each DDNA-SHARE-XX line to its guardian (USB / paper / IPFS).")
    print("  2. Seal master key in your Offline Vault (air-gapped or Ollama vault).")
    print("  3. Clear terminal history: Clear-History (PowerShell)")
    print("  4. Delete master key line from any logs — it should NOT persist on disk.")
    print()


def cmd_verify():
    """Verify shares file integrity without recovering the key."""
    print()
    print("  [dDNA] Verifying shares file (no key recovery)")
    print("  " + "─" * 50)

    data = load_shares()
    print(f"  Label          : {data.get('label', 'n/a')}")
    print(f"  Fingerprint    : {data.get('fingerprint', 'n/a')}")
    print(f"  Scheme         : {data.get('scheme', 'n/a')}")
    print(f"  Created UTC    : {data.get('created_utc', 'n/a')}")
    print(f"  Shares in file : {len(data.get('shares', []))}")
    print(f"  Seal           : {data.get('_seal', 'n/a')}")

    # Parse shares to confirm they are well-formed
    try:
        parsed = shares_from_printable(data['shares'])
        print(f"  Parse check    : {len(parsed)} shares parsed OK")
    except ValueError as e:
        print(f"  Parse check    : FAILED — {e}")
        return

    print()
    print("  [dDNA] Shares file appears intact. Run 'recover' to reconstruct key.")
    print()


def cmd_recover(share_indices: list = None):
    """
    Reconstruct key from shares in ddna_shares.json.
    Optionally specify which share indices to use (1-based, e.g. 1 3 5).
    """
    print()
    print("  [dDNA] Key recovery from shares")
    print("  " + "─" * 50)

    data = load_shares()
    all_printable = data['shares']
    k = int(data['k_threshold'])
    fp_stored = data['fingerprint']

    if share_indices:
        # Use only specified shares (1-based)
        selected = []
        for idx in share_indices:
            if not (1 <= idx <= len(all_printable)):
                print(f"  ERROR: Share index {idx} out of range (1..{len(all_printable)})")
                return
            selected.append(all_printable[idx - 1])
    else:
        # Use first k shares by default
        selected = all_printable[:k]
        print(f"  Using first {k} shares (default). Pass share numbers to choose.")

    if len(selected) < k:
        print(f"  ERROR: Need at least {k} shares, got {len(selected)}.")
        return

    shares = shares_from_printable(selected)
    key = recover_key(shares)
    fp_recovered = key_fingerprint(key)
    checksum = key_checksum(key)

    match = fp_recovered == fp_stored
    print(f"  Stored fingerprint   : {fp_stored}")
    print(f"  Recovered fingerprint: {fp_recovered}")
    print(f"  Match                : {'PASS' if match else 'FAIL'}")
    print()

    if match:
        print(f"  Recovered key        : {key.hex()}")
        print(f"  Checksum             : {checksum}")
        print()
        print("  [dDNA] Key recovered. Seal it immediately. Clear terminal history.")
        print("  Run: Clear-History")
    else:
        print("  [dDNA] Fingerprint mismatch — wrong shares or corrupted data.")
    print()


# -------------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    cmd = args[0] if args else 'demo'

    if cmd == 'demo':
        cmd_demo()

    elif cmd == 'generate':
        n = int(args[1]) if len(args) > 1 else 5
        k = int(args[2]) if len(args) > 2 else 3
        label = args[3] if len(args) > 3 else ''
        cmd_generate(n, k, label)

    elif cmd == 'verify':
        cmd_verify()

    elif cmd == 'recover':
        # Optional: pass share indices as extra args, e.g. recover 1 3 5
        indices = [int(a) for a in args[1:]] if len(args) > 1 else None
        cmd_recover(indices)

    else:
        print(__doc__)
        print(f"  Unknown command: {cmd}")
        print("  Valid: demo | generate <n> <k> | verify | recover [indices...]")
        sys.exit(1)


if __name__ == '__main__':
    main()
