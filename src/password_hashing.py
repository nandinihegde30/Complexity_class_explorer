"""Password hashing demonstration using standard library hashlib and secrets.

This module demonstrates secure password hashing using PBKDF2-HMAC-SHA256,
contrasting it with reversible encryption and explaining the role of cryptographic
salts and work factors (computational cost) in defending against offline attacks.
"""

from __future__ import annotations

import hashlib
import secrets
import time


DEFAULT_ITERATIONS = 100_000
DEFAULT_SALT_BYTES = 16


def generate_salt(length: int = DEFAULT_SALT_BYTES) -> bytes:
    """Generate a cryptographically secure random salt using the OS CSPRNG.

    Args:
        length: Number of random bytes (default: 16 bytes / 128 bits).

    Returns:
        Secure random bytes.
    """
    if not isinstance(length, int) or isinstance(length, bool) or length < 8:
        raise ValueError("Salt length must be an integer of at least 8 bytes.")
    return secrets.token_bytes(length)


def hash_password(
    password: str,
    salt: bytes | None = None,
    iterations: int = DEFAULT_ITERATIONS,
    hash_name: str = "sha256",
) -> dict:
    """Hash a password using PBKDF2-HMAC.

    PBKDF2 applies a pseudorandom function (HMAC-SHA256) repeatedly to slow
    down password cracking.

    Args:
        password: The input password string.
        salt: Optional salt bytes. If omitted, a fresh random salt is generated.
        iterations: Work factor specifying the iteration count.
        hash_name: Underlying hash function (default: 'sha256').

    Returns:
        Dictionary with salt (hex), hash (hex), iterations, and algorithm.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations < 1:
        raise ValueError("Iterations must be a positive integer.")

    if salt is None:
        salt = generate_salt()
    elif not isinstance(salt, (bytes, bytearray)):
        raise TypeError("Salt must be bytes or bytearray.")

    dk = hashlib.pbkdf2_hmac(
        hash_name,
        password.encode("utf-8"),
        salt,
        iterations,
    )

    return {
        "salt_hex": salt.hex(),
        "hash_hex": dk.hex(),
        "iterations": iterations,
        "algorithm": f"pbkdf2_hmac_{hash_name}",
    }


def verify_password(
    password: str,
    stored_hash_hex: str,
    salt_hex: str,
    iterations: int = DEFAULT_ITERATIONS,
    hash_name: str = "sha256",
) -> bool:
    """Verify a password against stored hash and salt using constant-time comparison.

    Uses secrets.compare_digest to prevent side-channel timing attacks.

    Args:
        password: Candidate password to verify.
        stored_hash_hex: Hex string of the stored hash.
        salt_hex: Hex string of the salt used during hashing.
        iterations: Iteration count used during hashing.
        hash_name: Hash algorithm name.

    Returns:
        True if the candidate password matches the stored hash, False otherwise.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")
    if not isinstance(stored_hash_hex, str) or not isinstance(salt_hex, str):
        raise TypeError("Hash and salt must be hex strings.")

    try:
        salt = bytes.fromhex(salt_hex)
    except ValueError as exc:
        raise ValueError("Invalid hex format for salt.") from exc

    candidate = hash_password(
        password=password,
        salt=salt,
        iterations=iterations,
        hash_name=hash_name,
    )

    # secrets.compare_digest avoids timing differences that could leak information.
    return secrets.compare_digest(candidate["hash_hex"], stored_hash_hex)


def benchmark_work_factors(
    test_password: str = "SampleBenchmarkPass#2026",
    iteration_counts: tuple[int, ...] = (10_000, 50_000, 100_000, 200_000),
) -> list[dict]:
    """Demonstrate how tuning the work factor directly controls computational cost."""
    results = []
    salt = generate_salt()

    for iters in iteration_counts:
        t0 = time.perf_counter()
        hash_password(test_password, salt=salt, iterations=iters)
        elapsed_ms = (time.perf_counter() - t0) * 1000

        results.append({
            "iterations": iters,
            "time_ms": elapsed_ms,
        })
    return results


def demonstrate_password_hashing(
    sample_password: str = "SecureDemoP@ssword2026",
    wrong_password: str = "WrongPasswordGuess",
    iterations: int = DEFAULT_ITERATIONS,
) -> dict:
    """Demonstrate end-to-end password hashing, verification, and failure handling."""
    # 1. Hash the password with a newly generated random salt
    hashed = hash_password(sample_password, iterations=iterations)

    # 2. Verify with the correct password
    valid_verification = verify_password(
        password=sample_password,
        stored_hash_hex=hashed["hash_hex"],
        salt_hex=hashed["salt_hex"],
        iterations=hashed["iterations"],
    )

    # 3. Verify with an incorrect password
    invalid_verification = verify_password(
        password=wrong_password,
        stored_hash_hex=hashed["hash_hex"],
        salt_hex=hashed["salt_hex"],
        iterations=hashed["iterations"],
    )

    return {
        "algorithm": hashed["algorithm"],
        "iterations": hashed["iterations"],
        "salt_hex": hashed["salt_hex"],
        "hash_hex": hashed["hash_hex"],
        "valid_verification": valid_verification,
        "invalid_verification": invalid_verification,
        "explanation": {
            "salt_purpose": (
                "A random cryptographic salt ensures that two users with the same password "
                "have completely different hashes, neutralizing precomputed rainbow tables."
            ),
            "work_factor_purpose": (
                f"The work factor ({iterations:,} iterations) forces an attacker to spend significant "
                "CPU cycles per guess, making brute-force dictionary attacks infeasible while "
                "requiring only a tiny fraction of a second for legitimate login."
            ),
            "hashing_vs_encryption": (
                "Password hashing is a one-way (irreversible) function used to verify credentials "
                "without storing the secret. Encryption is a two-way (reversible) operation "
                "intended to protect data confidentiality while allowing authorized decryption."
            ),
        },
    }


if __name__ == "__main__":
    demo = demonstrate_password_hashing()
    print("===== PASSWORD HASHING DEMONSTRATION =====")
    print(f"Algorithm: {demo['algorithm']}")
    print(f"Iterations (Work Factor): {demo['iterations']}")
    print(f"Salt (Hex): {demo['salt_hex']}")
    print(f"Derived Hash (Hex): {demo['hash_hex'][:32]}... (truncated)")
    print(f"Correct Password Verification: {demo['valid_verification']}")
    print(f"Wrong Password Verification: {demo['invalid_verification']}")
