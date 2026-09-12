"""
Additional edge-case tests for the RealEstate Property Discovery Platform.
Validates boundary conditions, empty inputs, and stress scenarios.

All helper functions are defined inline to avoid cross-module import issues.

Student: Akshat Gupta | 24ESKCS019
Course:  DevOps (MT1 – Modules 1-4)
"""

import unittest


# ---------------------------------------------------------------------------
# Inline property data and helpers (mirrors test_properties.py)
# ---------------------------------------------------------------------------

PROPERTIES = [
    {
        "id": 1, "title": "Luxury Sky Villa", "type": "Villa",
        "price": 15000000, "bedrooms": 4, "location": "Mumbai",
        "furnishing": "Furnished", "area": 3200,
    },
    {
        "id": 2, "title": "Modern Studio Apartment", "type": "Apartment",
        "price": 4500000, "bedrooms": 1, "location": "Bangalore",
        "furnishing": "Semi-Furnished", "area": 650,
    },
    {
        "id": 3, "title": "Premium Penthouse", "type": "Penthouse",
        "price": 35000000, "bedrooms": 5, "location": "Delhi",
        "furnishing": "Furnished", "area": 5500,
    },
    {
        "id": 4, "title": "Commercial Office Space", "type": "Commercial",
        "price": 8000000, "bedrooms": 0, "location": "Hyderabad",
        "furnishing": "Unfurnished", "area": 2100,
    },
    {
        "id": 5, "title": "Cosy 2BHK Apartment", "type": "Apartment",
        "price": 6200000, "bedrooms": 2, "location": "Pune",
        "furnishing": "Semi-Furnished", "area": 950,
    },
]


def filter_by_type(properties, prop_type):
    if not prop_type or prop_type.lower() == "all":
        return properties
    return [p for p in properties if p["type"].lower() == prop_type.lower()]


def filter_by_price(properties, min_price=0, max_price=float("inf")):
    return [p for p in properties if min_price <= p["price"] <= max_price]


def filter_by_bedrooms(properties, bedrooms):
    if bedrooms is None:
        return properties
    return [p for p in properties if p["bedrooms"] == bedrooms]


def filter_by_furnishing(properties, furnishing):
    if not furnishing:
        return properties
    return [p for p in properties if p["furnishing"].lower() == furnishing.lower()]


def search_properties(properties, query):
    q = query.strip().lower()
    if not q:
        return properties
    return [p for p in properties if q in p["title"].lower() or q in p["location"].lower()]


def calculate_price_per_sqft(price, area):
    if area <= 0:
        raise ValueError("Area must be greater than zero.")
    return round(price / area, 2)


def add_to_wishlist(wishlist, property_id):
    wishlist.add(property_id)
    return wishlist


def remove_from_wishlist(wishlist, property_id):
    wishlist.discard(property_id)
    return wishlist


def sort_properties(properties, key="price", reverse=False):
    return sorted(properties, key=lambda p: p.get(key, 0), reverse=reverse)


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

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
        results = filter_by_price(results, 0, 100)
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
