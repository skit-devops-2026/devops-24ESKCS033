"""
Food Expression - Shopping Cart & Order Calculation Engine
Provides business logic for calculating cart subtotals, validating and
applying promotional discounts, computing regional sales tax, and
compiling comprehensive order summaries.
"""


def cart_total(items):
    """
    Calculate the total cost of all items in the cart.
    Each item must have a 'price' (non-negative number) and 'qty' (positive integer).
    """
    if not items:
        return 0.0

    total = 0.0
    for item in items:
        if "price" not in item or "qty" not in item:
            raise KeyError("Item must contain 'price' and 'qty' keys")
        if item["price"] < 0:
            raise ValueError("Item price cannot be negative")
        if item["qty"] < 0:
            raise ValueError("Item quantity cannot be negative")
        total += item["price"] * item["qty"]
    return round(total, 2)


def apply_discount(total, percent):
    """
    Apply a promotional discount percentage to the subtotal.
    Validates that discount percent is between 0 and 100 inclusive.
    """
    if percent < 0 or percent > 100:
        raise ValueError("percent must be between 0 and 100")
    discount_amount = total * (percent / 100.0)
    return round(total - discount_amount, 2)


def calculate_tax(amount, tax_rate):
    """
    Calculate the sales tax amount on a given taxable subtotal.
    tax_rate is expected as a percentage (e.g. 5 for 5%, 8.25 for 8.25%).
    """
    if tax_rate < 0:
        raise ValueError("tax_rate cannot be negative")
    if amount < 0:
        raise ValueError("amount cannot be negative")
    return round(amount * (tax_rate / 100.0), 2)


def calculate_order_summary(items, discount_percent=0.0, tax_rate=0.0):
    """
    Calculate a comprehensive order summary.
    Returns a dictionary containing subtotal, discount, taxable total,
    tax amount, and final total.
    """
    subtotal = cart_total(items)
    discounted_subtotal = apply_discount(subtotal, discount_percent)
    discount_amount = round(subtotal - discounted_subtotal, 2)
    tax_amount = calculate_tax(discounted_subtotal, tax_rate)
    final_total = round(discounted_subtotal + tax_amount, 2)

    return {
        "subtotal": subtotal,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "discounted_subtotal": discounted_subtotal,
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "final_total": final_total
    }
