"""Tests for RSAdemo key generation, encryption, and decryption."""

import pytest

from RSAdemo import is_prime, generate_keys, encrypt, decrypt, demo_rsa


def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(17) is True
    assert is_prime(61) is True
    assert is_prime(1) is False
    assert is_prime(0) is False
    assert is_prime(-7) is False
    assert is_prime(15) is False


def test_generate_keys_valid():
    p, q = 61, 53
    pub, priv, phi = generate_keys(p, q)

    e, n = pub
    d, n_priv = priv

    assert n == p * q
    assert n == n_priv
    assert phi == (p - 1) * (q - 1)
    # e * d = 1 (mod phi)
    assert (e * d) % phi == 1


def test_generate_keys_invalid():
    # Non-primes
    with pytest.raises(ValueError):
        generate_keys(4, 7)

    # Identical primes
    with pytest.raises(ValueError):
        generate_keys(11, 11)


def test_encryption_and_decryption_cycle():
    p, q = 61, 53
    pub, priv, _ = generate_keys(p, q)

    message = 42
    ciphertext = encrypt(message, pub)
    decrypted = decrypt(ciphertext, priv)

    assert ciphertext != message
    assert decrypted == message


def test_message_out_of_range():
    p, q = 11, 13
    pub, _, _ = generate_keys(p, q)
    n = p * q

    with pytest.raises(ValueError):
        encrypt(n + 10, pub)


def test_demo_rsa_runs_successfully():
    result = demo_rsa(p=61, q=53, message=99)
    assert result["success"] is True
    assert result["decrypted"] == 99
