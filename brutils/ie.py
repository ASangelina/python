import re

# FORMATTING
############

def remove_symbols(ie: str) -> str:
    """
    Remove símbolos de uma Inscrição Estadual (IE).

    Args:
        ie (str): Inscrição Estadual com ou sem formatação.

    Returns:
        str: IE apenas com números.

    Example:
        >>> remove_symbols("110.042.490.114")
        '110042490114'
    """
    return re.sub(r"[^\d]", "", ie)


def format_ie(ie: str) -> str | None:
    """
    Formata uma IE de forma genérica: separa com pontos a cada 3 ou 4 dígitos.

    NOTE: A formatação exata varia por UF. Aqui é só ilustrativa.

    Args:
        ie (str): IE apenas com dígitos.

    Returns:
        str | None: IE formatada ou None se inválida.

    Example:
        >>> format_ie("110042490114")
        '110.042.490.114'
    """
    clean = remove_symbols(ie)
    if not clean or not clean.isdigit():
        return None

    # Exemplo simples de formatação genérica
    if len(clean) == 12:
        return f"{clean[:3]}.{clean[3:6]}.{clean[6:9]}.{clean[9:]}"
    elif len(clean) == 13:
        return f"{clean[:3]}.{clean[3:6]}.{clean[6:9]}.{clean[9:11]}.{clean[11:]}"
    return clean


# VALIDATION
############

def is_valid(ie: str, uf: str) -> bool:
    """
    Valida uma Inscrição Estadual (IE) de acordo com a UF.

    Args:
        ie (str): Inscrição Estadual.
        uf (str): Unidade Federativa (ex: 'SP', 'MG', 'RJ', 'RS').

    Returns:
        bool: True se a IE for válida para a UF, False caso contrário.

    Example:
        >>> is_valid("110042490114", "SP")
        True
    """
    clean_ie = remove_symbols(ie)
    uf = uf.upper()

    validators = {
        'SP': _validate_sp,
        'MG': _validate_mg,
        'RJ': _validate_rj,
        'RS': _validate_rs,
    }

    if uf not in validators:
        return False  # ou raise NotImplementedError

    return validators[uf](clean_ie)


# Implementações específicas por UF
# ---------------------------------

def _validate_sp(ie: str) -> bool:
    if len(ie) == 12:
        body = ie[:8]
        d1 = _sp_digit1(body)
        d2 = _sp_digit2(ie[:11])
        return d1 == ie[8] and d2 == ie[-1]
    elif len(ie) == 13 and ie.startswith("P"):
        body = ie[1:9]
        check = _sp_digit1(body)
        return check == ie[9]
    return False

def _sp_digit1(digits: str) -> str:
    weights = [1, 3, 4, 5, 6, 7, 8, 10]
    soma = sum(int(d) * w for d, w in zip(digits, weights))
    resto = soma % 11
    return "0" if resto == 10 else str(resto)

def _sp_digit2(digits: str) -> str:
    weights = [3, 2, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(d) * w for d, w in zip(digits, weights))
    resto = soma % 11
    return "0" if resto == 10 else str(resto)

def _validate_mg(ie: str) -> bool:
    if len(ie) != 13:
        return False

    body = ie[:11]
    d1 = _mg_digit1(body)
    d2 = _mg_digit2(body + d1)
    return d1 == ie[11] and d2 == ie[12]

def _mg_digit1(digits: str) -> str:
    new_digits = digits[:3] + '0' + digits[3:]
    weights = [1, 2] * 6
    total = 0
    for i, d in enumerate(new_digits):
        prod = int(d) * weights[i]
        total += sum(map(int, str(prod)))
    resto = total % 10
    return str(0 if resto == 0 else 10 - resto)

def _mg_digit2(digits: str) -> str:
    weights = list(range(3, 0, -1)) + list(range(10, 1, -1))
    total = sum(int(d) * w for d, w in zip(digits, weights))
    resto = total % 11
    return str(0 if resto < 2 else 11 - resto)

def _validate_rj(ie: str) -> bool:
    if len(ie) != 8:
        return False
    weights = [2, 7, 6, 5, 4, 3, 2]
    total = sum(int(d) * w for d, w in zip(ie[:7], weights))
    resto = total % 11
    dv = 0 if resto <= 1 else 11 - resto
    return str(dv) == ie[-1]

def _validate_rs(ie: str) -> bool:
    if len(ie) != 10:
        return False
    weights = list(range(2, 10))[::-1]
    total = sum(int(d) * w for d, w in zip(ie[:9], weights))
    resto = 11 - (total % 11)
    dv = 0 if resto >= 10 else resto
    return str(dv) == ie[-1]
