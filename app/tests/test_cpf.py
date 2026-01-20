"""Tests for CPF validation"""

import pytest

from app.domain.validators.cpf import format_cpf, validate_cpf


class TestValidateCPF:
    """Test CPF validation"""

    def test_valid_cpf_with_formatting(self):
        """Test valid CPF with formatting"""
        assert validate_cpf("123.456.789-09") is True

    def test_valid_cpf_without_formatting(self):
        """Test valid CPF without formatting"""
        assert validate_cpf("12345678909") is True

    def test_invalid_cpf_all_same_digits(self):
        """Test invalid CPF with all same digits"""
        assert validate_cpf("111.111.111-11") is False
        assert validate_cpf("00000000000") is False

    def test_invalid_cpf_wrong_length(self):
        """Test invalid CPF with wrong length"""
        assert validate_cpf("123.456.789") is False
        assert validate_cpf("12345678901234") is False

    def test_invalid_cpf_non_numeric(self):
        """Test invalid CPF with non-numeric characters"""
        assert validate_cpf("ABC.DEF.GHI-JK") is False

    def test_invalid_cpf_wrong_check_digit(self):
        """Test invalid CPF with wrong check digit"""
        assert validate_cpf("123.456.789-00") is False


class TestFormatCPF:
    """Test CPF formatting"""

    def test_format_valid_cpf(self):
        """Test formatting a valid CPF"""
        assert format_cpf("12345678909") == "123.456.789-09"

    def test_format_cpf_with_existing_formatting(self):
        """Test formatting a CPF with existing formatting"""
        assert format_cpf("123.456.789-09") == "123.456.789-09"

    def test_format_cpf_invalid_length(self):
        """Test formatting CPF with invalid length"""
        with pytest.raises(ValueError):
            format_cpf("1234567890")
