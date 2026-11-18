"""Theoretical context connecting cryptography with computational complexity.

This module explains why RSA integer factorization and password hashing
are considered computationally hard, their relationship with complexity classes
(P, NP, NP-intermediate), and common academic misconceptions about P vs NP.
"""


def crypto_context() -> str:
    """Explain the cryptography concepts and complexity relationships in the project.

    Key academic concepts covered:
    1. RSA Public-Key Cryptography:
       - Keys are derived from two large distinct primes (p and q).
       - The modulus n = p * q is made public; the totient phi(n) = (p-1)*(q-1) is kept secret.
       - RSA encryption and decryption use modular exponentiation, which requires a polynomial
         number of bit operations in the size of the modulus under standard arithmetic models.
       - Security relies on the hardness of the Integer Factorization problem: given n, find p and q.
       - Classical algorithms (e.g. General Number Field Sieve, GNFS) run in sub-exponential
         time O(exp(c * (log n)^(1/3) * (log log n)^(2/3))), not strictly exponential.
       - In its decision formulation (determining whether n has a prime factor <= k), integer
         factorization belongs to both NP and co-NP, and is widely suspected to be NP-intermediate
         rather than NP-complete.
       - IMPORTANT: Modern cryptographic systems rely on the assumed computational hardness of
         specific mathematical problems. The unresolved P versus NP question alone neither establishes
         nor guarantees cryptographic security. Furthermore, Shor's quantum algorithm factors in
         polynomial time (BQP).
       - Toy implementations (like RSAdemo.py) using small primes and textbook RSA without padding
         (such as OAEP) are strictly educational and vulnerable to trivial factorization and attacks.

    2. Password Hashing and Storage:
       - Passwords must never be stored as plain text or using raw, fast hashes (like MD5 or SHA-256).
       - A cryptographic salt (cryptographically secure random bytes from secrets) ensures that
         identical passwords produce distinct hashes and defeats precomputed rainbow tables.
       - A configurable work factor (iteration count in PBKDF2, or memory cost in Argon2) deliberately
         makes the hashing function computationally expensive.
       - High work factors slow down offline dictionary and brute-force attacks by several orders
         of magnitude while imposing negligible overhead on legitimate authentications.
       - Password hashing is a one-way transformation (irreversible), fundamentally distinct
         from two-way encryption (reversible using a decryption key).
    """
    return (
        "Cryptography and Computational Complexity:\n\n"
        "1. RSA Encryption and Integer Factorization:\n"
        "   - Public key (e, n) and private key (d, n) are derived from primes p and q where n = p * q.\n"
        "   - RSA encryption and decryption use modular exponentiation, which requires a polynomial "
        "number of bit operations in the size of the modulus under standard arithmetic models.\n"
        "   - Inverting encryption without private key d requires factoring modulus n into p and q.\n"
        "   - Known classical factoring algorithms (such as the General Number Field Sieve) run in "
        "sub-exponential time, not strictly exponential time. Integer factorization in its decision "
        "formulation belongs to both NP and co-NP, and is suspected to be NP-intermediate rather than NP-complete.\n"
        "   - Crucially, modern cryptographic systems rely on the assumed computational hardness of specific "
        "mathematical problems. The unresolved P versus NP question alone neither establishes nor guarantees "
        "cryptographic security.\n"
        "   - Note: The toy RSA implementation uses small primes and textbook formulas without OAEP padding, "
        "meaning it is intended solely for educational demonstration and is NOT secure for real-world use.\n\n"
        "2. Password Hashing and Computational Work:\n"
        "   - Passwords must be hashed using a dedicated slow key derivation function (e.g., PBKDF2-HMAC-SHA256).\n"
        "   - A unique random salt is added to each password before hashing to defeat precomputed rainbow tables "
        "and ensure identical passwords yield different hash values.\n"
        "   - A tunable work factor (iteration count) deliberately increases the CPU and time cost for hashing, "
        "severely penalizing offline brute-force and dictionary attacks.\n"
        "   - Password hashing is a one-way, irreversible transformation, whereas encryption is two-way and reversible."
    )


def rsa_theory_notes() -> dict:
    """Return structured academic summary of RSA and complexity theory."""
    return {
        "modulus_generation": "n = p * q, where p and q are distinct primes.",
        "totient": "phi(n) = (p - 1) * (q - 1).",
        "public_exponent": "e such that 1 < e < phi(n) and gcd(e, phi(n)) == 1.",
        "private_exponent": "d = e^(-1) mod phi(n), computed via Extended Euclidean Algorithm.",
        "encryption_efficiency": "Polynomial number of bit operations in modulus size under standard arithmetic models.",
        "decryption_efficiency": "Polynomial number of bit operations in modulus size under standard arithmetic models.",
        "factoring_complexity": "Sub-exponential (GNFS); decision formulation in NP and co-NP (suspected NP-intermediate).",
        "p_vs_np_relation": (
            "Modern cryptographic systems rely on the assumed computational hardness of specific mathematical problems. "
            "The unresolved P versus NP question alone neither establishes nor guarantees cryptographic security."
        ),
        "educational_notice": "Toy RSA uses small primes without OAEP padding; strictly for teaching.",
    }
