import re


def validate_name(name: str) -> bool:
    """
    Validate product name.
    Allows letters, numbers, spaces and hyphens.
    """
    return bool(re.match(r"^[A-Za-z0-9\s\-]+$", name.strip()))


def validate_category(category: str) -> bool:
    """
    Validate category name.
    Allows letters, spaces and hyphens.
    """
    return bool(re.match(r"^[A-Za-z\s\-]+$", category.strip()))


def validate_quantity(quantity: str) -> bool:
    """
    Validate quantity.
    Must be a positive integer.
    """
    return quantity.isdigit()


def validate_price(price: str) -> bool:
    """
    Validate price.
    Must be numeric.
    """
    try:
        float(price)
        return True
    except ValueError:
        return False