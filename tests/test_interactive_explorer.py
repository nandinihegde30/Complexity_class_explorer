"""Tests for the Interactive Explore Mode in src/interactive_explorer.py."""

from unittest.mock import patch
import pytest

from src.interactive_explorer import (
    prompt_integers,
    run_merge_sort_interactive,
    run_subset_sum_interactive,
    run_halting_interactive,
    run_crypto_interactive,
    view_complexity_concepts,
    main_interactive_menu,
)


def test_prompt_integers_valid():
    with patch("builtins.input", return_value="10 20 -5 0 99"):
        result = prompt_integers("prompt")
        assert result == [10, 20, -5, 0, 99]


def test_prompt_integers_empty(capsys):
    with patch("builtins.input", return_value="   "):
        result = prompt_integers("prompt")
        assert result is None
        captured = capsys.readouterr()
        assert "cannot be empty" in captured.out


def test_prompt_integers_invalid_token(capsys):
    with patch("builtins.input", return_value="10 abc 30"):
        result = prompt_integers("prompt")
        assert result is None
        captured = capsys.readouterr()
        assert "not a valid integer" in captured.out


def test_run_merge_sort_interactive_success(capsys):
    with patch("builtins.input", return_value="45 12 89 3 21 7"):
        run_merge_sort_interactive()
        captured = capsys.readouterr()
        assert "Sorted Array:   [3, 7, 12, 21, 45, 89]" in captured.out
        assert "Execution Time:" in captured.out
        assert "O(n log n)" in captured.out


def test_run_merge_sort_interactive_invalid(capsys):
    with patch("builtins.input", return_value=""):
        run_merge_sort_interactive()
        captured = capsys.readouterr()
        assert "cannot be empty" in captured.out


def test_run_subset_sum_interactive_solution_found(capsys):
    inputs = iter(["2 3 7 8 10", "11"])
    with patch("builtins.input", side_effect=inputs):
        run_subset_sum_interactive()
        captured = capsys.readouterr()
        assert "Subset Found:" in captured.out
        assert "Subset Sum:   11" in captured.out
        assert "O(n * 2^n)" in captured.out
        assert "Polynomial-time Certificate Verification: True" in captured.out


def test_run_subset_sum_interactive_no_solution(capsys):
    inputs = iter(["2 4 6 8", "11"])
    with patch("builtins.input", side_effect=inputs):
        run_subset_sum_interactive()
        captured = capsys.readouterr()
        assert "No subset found summing to target 11" in captured.out


def test_run_subset_sum_interactive_invalid_target(capsys):
    inputs = iter(["1 2 3", "invalid_target"])
    with patch("builtins.input", side_effect=inputs):
        run_subset_sum_interactive()
        captured = capsys.readouterr()
        assert "not a valid integer" in captured.out


def test_run_subset_sum_interactive_large_n_abort(capsys):
    # n = 23, user inputs 'n' to abort
    large_input = " ".join(str(i) for i in range(23))
    inputs = iter([large_input, "100", "n"])
    with patch("builtins.input", side_effect=inputs):
        run_subset_sum_interactive()
        captured = capsys.readouterr()
        assert "Warning: Input size n=23" in captured.out
        assert "search aborted by user" in captured.out


def test_run_halting_interactive_halting_machine(capsys):
    # Choice 1 (Bit inverter), 50 steps, default tape
    inputs = iter(["1", "50", "1101"])
    with patch("builtins.input", side_effect=inputs):
        run_halting_interactive()
        captured = capsys.readouterr()
        assert "Result:         HALTED" in captured.out
        assert "Steps Executed: 5" in captured.out


def test_run_halting_interactive_diagonalization(capsys):
    # Choice 2 (Diagonalization)
    with patch("builtins.input", return_value="2"):
        run_halting_interactive()
        captured = capsys.readouterr()
        assert "TURING'S DIAGONALIZATION PROOF" in captured.out
        assert "Contradiction" in captured.out
        assert "UNDECIDABLE" in captured.out


def test_run_halting_interactive_invalid_choice(capsys):
    with patch("builtins.input", return_value="99"):
        run_halting_interactive()
        captured = capsys.readouterr()
        assert "Invalid choice" in captured.out


def test_run_crypto_interactive_rsa(capsys):
    # Submenu choice 1 (RSA), message 42
    inputs = iter(["1", "42"])
    with patch("builtins.input", side_effect=inputs):
        run_crypto_interactive()
        captured = capsys.readouterr()
        assert "RSA PUBLIC-KEY CRYPTOGRAPHY" in captured.out
        assert "Original Message:   42" in captured.out
        assert "Decrypted Message:  42" in captured.out
        assert "Success:            True" in captured.out


def test_run_crypto_interactive_password_hashing(capsys):
    # Submenu choice 2 (Password Hashing), default password
    inputs = iter(["2", ""])
    with patch("builtins.input", side_effect=inputs):
        run_crypto_interactive()
        captured = capsys.readouterr()
        assert "PASSWORD HASHING (PBKDF2-HMAC-SHA256)" in captured.out
        assert "Verification with Correct Password: True" in captured.out
        assert "Verification with Wrong Password:   False" in captured.out


def test_view_complexity_concepts(capsys):
    view_complexity_concepts()
    captured = capsys.readouterr()
    assert "P" in captured.out
    assert "NP" in captured.out
    assert "Undecidable" in captured.out
    assert "O(n log n)" in captured.out


def test_main_interactive_menu_exit(capsys):
    # Option 7: Exit
    with patch("builtins.input", return_value="7"):
        main_interactive_menu()
        captured = capsys.readouterr()
        assert "Thank you for exploring Complexity Class Explorer." in captured.out
