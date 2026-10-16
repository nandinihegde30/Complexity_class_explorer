
from src.crypto_context import crypto_context


def test_crypto_context_returns_text():
    result = crypto_context()

    assert isinstance(result, str)
    assert len(result) > 0


def test_crypto_context_explains_rsa():
    result = crypto_context().lower()

    assert "rsa" in result
    assert "factoring" in result


def test_crypto_context_explains_password_hashing():
    result = crypto_context().lower()

    assert "salt" in result
    assert "work factor" in result
    assert "password" in result
