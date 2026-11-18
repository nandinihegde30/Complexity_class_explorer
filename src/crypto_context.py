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
       - Encryption and decryption use modular exponentiation (pow(m, e, n) and pow(c, d, n)),
         which runs in polynomial time O((log n)^3), making legitimate operations very fast.
       - Security relies on the hardness of the Integer Factorization problem: given n, find p and q.
       - Classical algorithms (e.g. General Number Field Sieve, GNFS) run in sub-exponential
         time O(exp(c * (log n)^(1/3) * (log log n)^(2/3))), not strictly exponential.
       - Integer Factorization is in NP and co-NP, but is NOT known to be NP-complete. It is
         widely believed to be in NP-intermediate.
       - IMPORTANT: RSA security should NOT be described as simply relying on P != NP.
         Even if P != NP in the worst case, cryptography requires average-case hardness.
         Furthermore, Shor's quantum algorithm factors in polynomial time (BQP).
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
        "   - Computing modular exponentiation for encryption c = m^e (mod n) and decryption m = c^d (mod n) "
        "is efficient and runs in polynomial time O((log n)^3).\n"
        "   - Inverting encryption without private key d requires factoring modulus n into p and q.\n"
        "   - Known classical factoring algorithms (such as the General Number Field Sieve) run in "
        "sub-exponential time, not strictly exponential time. Factoring is in NP and co-NP, "
        "and is suspected to be NP-intermediate, not NP-complete.\n"
        "   - Crucially, RSA security does NOT simply rely on P != NP. Cryptography requires average-case "
        "hardness and one-way functions, whereas P != NP is merely a worst-case separation.\n"
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
        "encryption_time": "O((log n)^3) - polynomial time via modular exponentiation.",
        "decryption_time": "O((log n)^3) - polynomial time via modular exponentiation.",
        "factoring_complexity": "Sub-exponential (GNFS), in NP and co-NP (suspected NP-intermediate).",
        "p_vs_np_relation": (
            "P != NP is a necessary condition for public-key cryptography to exist, "
            "but NOT sufficient. Cryptography requires average-case hardness, "
            "whereas NP-completeness defines worst-case hardness. Factoring is not NP-complete."
        ),
        "educational_notice": "Toy RSA uses small primes without OAEP padding; strictly for teaching.",
    }
