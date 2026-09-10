"
Unit test suite for the Food Expression cart module.
Tests cart total calculations, promotional discounts, tax calculations,
and full order summary assembly, including edge cases and exception handling.
"

import pytest
from cart import (
    cart_total,
    apply_discount,
    calculate_tax,
    calculate_order_summary
)


def test_cart_total_standard():
    items = [
        {price: 100, qty: 2},
        {price: 50, qty: 1}
    ]
    assert cart_total(items) == 250.0


def test_cart_total_empty():
    assert cart_total([]) == 0.0


def test_cart_total_single_item():
    items = [{price: 19.99, qty: 3}]
    assert cart_total(items) == 59.97


def test_cart_total_invalid_item():
    with pytest.raises(KeyError):
        cart_total([{price: 100}])


def test_cart_total_negative_price():
    with pytest.raises(ValueError):
        cart_total([{price: -10, qty: 2}])


def test_cart_total_negative_qty():
    with pytest.raises(ValueError):
        cart_total([{price: 10, qty: -2}])


def test_apply_discount_standard():
    assert apply_discount(200, 10) == 180.0


def test_apply_discount_zero():
    assert apply_discount(100, 0) == 100.0


def test_apply_discount_hundred_percent():
    assert apply_discount(150, 100) == 0.0


def test_apply_discount_negative_raises():
    with pytest.raises(ValueError):
        apply_discount(100, -5)


def test_apply_discount_over_hundred_raises():
    with pytest.raises(ValueError):
        apply_discount(100, 105)


def test_calculate_tax_standard():
    assert calculate_tax(100.0, 5.0) == 5.0


def test_calculate_tax_zero():
    assert calculate_tax(100.0, 0.0) == 0.0


def test_calculate_tax_negative_rate():
    with pytest.raises(ValueError):
        calculate_tax(100.0, -2.0)


def test_calculate_order_summary():
    items = [
        {price: 50, qty: 2},
        {price: 100, qty: 1}
    ]
    summary = calculate_order_summary(items, discount_percent=10.0, tax_rate=5.0)

    assert summary[subtotal] == 200.0
    assert summary[discount_percent] == 10.0
    assert summary[discount_amount] == 20.0
    assert summary[discounted_subtotal] == 180.0
    assert summary[tax_rate] == 5.0
    assert summary[tax_amount] == 9.0
    assert summary[final_total] == 189.0
