"""Tests for PBKDF2-HMAC password hashing and verification."""

import pytest

from src.password_hashing import (
    generate_salt,
    hash_password,
    verify_password,
    demonstrate_password_hashing,
)


def test_salt_generation():
    salt1 = generate_salt(16)
    salt2 = generate_salt(16)
    assert isinstance(salt1, bytes)
    assert len(salt1) == 16
    # Random salts should be distinct
    assert salt1 != salt2


def test_invalid_salt_length():
    with pytest.raises(ValueError):
        generate_salt(4)


def test_hash_password_structure():
    result = hash_password("MySecurePassword123!", iterations=10_000)
    assert isinstance(result, dict)
    assert "salt_hex" in result
    assert "hash_hex" in result
    assert result["iterations"] == 10_000
    assert result["algorithm"] == "pbkdf2_hmac_sha256"


def test_verify_password_success_and_failure():
    password = "CorrectHorseBatteryStaple"
    hashed = hash_password(password, iterations=10_000)

    # Correct password succeeds
    assert verify_password(
        password=password,
        stored_hash_hex=hashed["hash_hex"],
        salt_hex=hashed["salt_hex"],
        iterations=hashed["iterations"],
    ) is True

    # Incorrect password fails
    assert verify_password(
        password="WrongPasswordAttempt",
        stored_hash_hex=hashed["hash_hex"],
        salt_hex=hashed["salt_hex"],
        iterations=hashed["iterations"],
    ) is False


def test_demonstrate_password_hashing():
    demo = demonstrate_password_hashing(iterations=5_000)
    assert demo["valid_verification"] is True
    assert demo["invalid_verification"] is False
    assert "salt_purpose" in demo["explanation"]
    assert "work_factor_purpose" in demo["explanation"]
    assert "hashing_vs_encryption" in demo["explanation"]
