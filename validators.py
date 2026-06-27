import re


def validate_name(name: str) -> bool:
    """Validate the product name using a simple character rule."""
    # Allow letters, numbers, spaces, and hyphens for a product name.
    return bool(re.match(r"^[A-Za-z0-9\s\-]+$", name.strip()))


def validate_category(category: str) -> bool:
    """Validate the category name using a simple character rule."""
    # Allow letters, spaces, and hyphens for a category name.
    return bool(re.match(r"^[A-Za-z\s\-]+$", category.strip()))


def validate_quantity(quantity: str) -> bool:
    try:
        return int(quantity) >= 0
    except ValueError:
        return False


def validate_price(price: str) -> bool:
    """Validate that the price is a non-negative numeric value."""
    try:
        return float(price) >= 0
    except ValueError:
        return False

def validate_product_data(name, qty, price, category):
    """
    Validate all product fields at once.
    Returns (is_valid, error_message).
    """

    if not validate_name(name):
        return False, "Name contains invalid characters"

    if not validate_category(category):
        return False, "Category contains invalid characters"

    if not validate_quantity(qty):
        return False, "Quantity must be a non-negative integer"

    if not validate_price(price):
        return False, "Price must be a non-negative number"

    return True, ""