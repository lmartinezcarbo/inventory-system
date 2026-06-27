import re

def validate_name(name):
    return bool(re.match(r"^[A-Za-z0-9\s\-]+$", name))

def validate_category(category):
    return bool(re.match(r"^[A-Za-z\s\-]+$", category))

def validate_quantity(quantity):
    return quantity.isdigit()

def validate_price(price):
    try:
        float(price)
        return True
    except ValueError:
        return False