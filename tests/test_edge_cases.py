"""
Additional edge-case tests for the RealEstate Property Discovery Platform.
Validates boundary conditions, empty inputs, and stress scenarios.

Student: Akshat Gupta | 24ESKCS019
Course:  DevOps (MT1 – Modules 1-4)
"""

import unittest
from tests.test_properties import (
    PROPERTIES,
    filter_by_type,
    filter_by_price,
    filter_by_bedrooms,
    filter_by_furnishing,
    search_properties,
    calculate_price_per_sqft,
    add_to_wishlist,
    remove_from_wishlist,
    sort_properties,
)


class TestEdgeCasesEmptyDataset(unittest.TestCase):
    """Tests with an empty property dataset."""

    def test_filter_type_empty_dataset(self):
        self.assertEqual(filter_by_type([], "Apartment"), [])

    def test_filter_price_empty_dataset(self):
        self.assertEqual(filter_by_price([], 0, 9999999), [])

    def test_search_empty_dataset(self):
        self.assertEqual(search_properties([], "Mumbai"), [])

    def test_sort_empty_dataset(self):
        self.assertEqual(sort_properties([]), [])

    def test_filter_bedrooms_empty_dataset(self):
        self.assertEqual(filter_by_bedrooms([], 2), [])


class TestPricePerSqftEdgeCases(unittest.TestCase):
    """Boundary tests for price-per-sqft."""

    def test_large_price_small_area(self):
        result = calculate_price_per_sqft(100_000_000, 1)
        self.assertEqual(result, 100_000_000.0)

    def test_small_price_large_area(self):
        result = calculate_price_per_sqft(1, 1_000_000)
        self.assertEqual(result, 0.0)

    def test_equal_price_and_area(self):
        result = calculate_price_per_sqft(500, 500)
        self.assertEqual(result, 1.0)


class TestWishlistEdgeCases(unittest.TestCase):
    """Edge cases for wishlist operations."""

    def test_empty_wishlist_remove_no_error(self):
        wishlist = set()
        result = remove_from_wishlist(wishlist, 42)
        self.assertEqual(len(result), 0)

    def test_add_string_id_to_wishlist(self):
        wishlist = set()
        add_to_wishlist(wishlist, "prop-999")
        self.assertIn("prop-999", wishlist)

    def test_wishlist_large_number_of_items(self):
        wishlist = set()
        for i in range(1000):
            add_to_wishlist(wishlist, i)
        self.assertEqual(len(wishlist), 1000)


class TestSearchEdgeCases(unittest.TestCase):
    """Edge case tests for search functionality."""

    def test_search_whitespace_only_returns_all(self):
        result = search_properties(PROPERTIES, "   ")
        self.assertEqual(len(result), len(PROPERTIES))

    def test_search_single_character(self):
        # 'a' matches many titles/locations
        result = search_properties(PROPERTIES, "a")
        self.assertGreater(len(result), 0)

    def test_search_special_characters_returns_empty(self):
        result = search_properties(PROPERTIES, "!@#$%^&*()")
        self.assertEqual(result, [])


class TestSortingEdgeCases(unittest.TestCase):
    """Edge case tests for sorting."""

    def test_sort_single_item(self):
        single = [PROPERTIES[0]]
        result = sort_properties(single, "price")
        self.assertEqual(len(result), 1)

    def test_sort_does_not_modify_original(self):
        original_prices = [p["price"] for p in PROPERTIES]
        sort_properties(PROPERTIES, "price", reverse=True)
        current_prices = [p["price"] for p in PROPERTIES]
        self.assertEqual(original_prices, current_prices)


class TestFilterChaining(unittest.TestCase):
    """Advanced chaining scenarios."""

    def test_all_filters_returning_empty(self):
        results = filter_by_type(PROPERTIES, "Villa")
        results = filter_by_price(results, 0, 100)   # way too low price
        self.assertEqual(results, [])

    def test_chain_does_not_mutate_original(self):
        count_before = len(PROPERTIES)
        filter_by_type(PROPERTIES, "Apartment")
        self.assertEqual(len(PROPERTIES), count_before)

    def test_multiple_type_checks(self):
        apartments = filter_by_type(PROPERTIES, "Apartment")
        villas = filter_by_type(PROPERTIES, "Villa")
        penthouses = filter_by_type(PROPERTIES, "Penthouse")
        commercial = filter_by_type(PROPERTIES, "Commercial")
        total = len(apartments) + len(villas) + len(penthouses) + len(commercial)
        self.assertEqual(total, len(PROPERTIES))


if __name__ == "__main__":
    unittest.main(verbosity=2)
