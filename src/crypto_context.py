
def crypto_context() -> str:
    """Explain the cryptography concepts used in the project."""
    return (
        "Cryptography and Complexity:\n"
        "1. RSA security relies partly on the difficulty of factoring "
        "large integers that are products of large prime numbers.\n"
        "2. Passwords should be stored using secure password-hashing "
        "algorithms, not as plain text.\n"
        "3. A unique random salt is added to each password before hashing "
        "to help prevent precomputed hash attacks and identical hashes "
        "for identical passwords.\n"
        "4. A work factor controls how computationally expensive password "
        "hashing is. A suitable work factor makes guessing passwords "
        "slower for attackers.\n"
        "5. RSA factoring and password hashing illustrate how "
        "computational difficulty supports security."
    )
