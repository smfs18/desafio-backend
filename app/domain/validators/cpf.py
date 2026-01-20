"""CPF validation utilities"""


def validate_cpf(cpf: str) -> bool:
    """
    Validate Brazilian CPF format.

    Args:
        cpf: CPF string with or without formatting

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_cpf("123.456.789-09")
        True
        >>> validate_cpf("12345678909")
        True
        >>> validate_cpf("111.111.111-11")
        False
    """
    # Remove formatting
    cpf = cpf.replace(".", "").replace("-", "").strip()

    # Check length
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    # Check if all digits are the same (invalid CPF)
    if cpf == cpf[0] * 11:
        return False

    # Validate first check digit
    sum_digits = sum(int(cpf[i]) * (10 - i) for i in range(9))
    first_digit = 11 - (sum_digits % 11)
    first_digit = 0 if first_digit > 9 else first_digit

    if int(cpf[9]) != first_digit:
        return False

    # Validate second check digit
    sum_digits = sum(int(cpf[i]) * (11 - i) for i in range(10))
    second_digit = 11 - (sum_digits % 11)
    second_digit = 0 if second_digit > 9 else second_digit

    if int(cpf[10]) != second_digit:
        return False

    return True


def format_cpf(cpf: str) -> str:
    """
    Format CPF to XXX.XXX.XXX-XX format.

    Args:
        cpf: CPF string without formatting

    Returns:
        Formatted CPF
    """
    cpf = cpf.replace(".", "").replace("-", "").strip()
    if len(cpf) != 11:
        raise ValueError("CPF must have 11 digits")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
