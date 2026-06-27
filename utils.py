"""Display products in a formatted table."""
def print_products(products):
    print("\nID | Name | Qty | Price | Category")
    print("-------------------------------------")

    for p in products:
        print(f"{p[0]} | {p[1]} | {p[2]} | {p[3]} | {p[4]}")