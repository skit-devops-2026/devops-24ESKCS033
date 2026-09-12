"""
Unit tests for RealEstate Property Discovery Platform.
Tests core property data structures, filter logic, and business rules.

Student: Akshat Gupta | 24ESKCS019
Course:  DevOps (MT1 – Modules 1-4)
"""

import unittest


# ---------------------------------------------------------------------------
# Lightweight in-memory model mirroring the JS data in script.js
# ---------------------------------------------------------------------------

PROPERTIES = [
    {
        "id": 1,
        "title": "Luxury Sky Villa",
        "type": "Villa",
        "price": 15000000,
        "bedrooms": 4,
        "location": "Mumbai",
        "furnishing": "Furnished",
        "area": 3200,
    },
    {
        "id": 2,
        "title": "Modern Studio Apartment",
        "type": "Apartment",
        "price": 4500000,
        "bedrooms": 1,
        "location": "Bangalore",
        "furnishing": "Semi-Furnished",
        "area": 650,
    },
    {
        "id": 3,
        "title": "Premium Penthouse",
        "type": "Penthouse",
        "price": 35000000,
        "bedrooms": 5,
        "location": "Delhi",
        "furnishing": "Furnished",
        "area": 5500,
    },
    {
        "id": 4,
        "title": "Commercial Office Space",
        "type": "Commercial",
        "price": 8000000,
        "bedrooms": 0,
        "location": "Hyderabad",
        "furnishing": "Unfurnished",
        "area": 2100,
    },
    {
        "id": 5,
        "title": "Cosy 2BHK Apartment",
        "type": "Apartment",
        "price": 6200000,
        "bedrooms": 2,
        "location": "Pune",
        "furnishing": "Semi-Furnished",
        "area": 950,
    },
]


# ---------------------------------------------------------------------------
# Helper functions (mirror business logic from script.js)
# ---------------------------------------------------------------------------

def filter_by_type(properties, prop_type):
    """Return properties matching the given type (case-insensitive)."""
    if not prop_type or prop_type.lower() == "all":
        return properties
    return [p for p in properties if p["type"].lower() == prop_type.lower()]


def filter_by_price(properties, min_price=0, max_price=float("inf")):
    """Return properties within the given price range."""
    return [p for p in properties if min_price <= p["price"] <= max_price]


def filter_by_bedrooms(properties, bedrooms):
    """Return properties matching the bedroom count; None means no filter."""
    if bedrooms is None:
        return properties
    return [p for p in properties if p["bedrooms"] == bedrooms]


def filter_by_furnishing(properties, furnishing):
    """Return properties matching the furnishing status; None means no filter."""
    if not furnishing:
        return properties
    return [
        p for p in properties
        if p["furnishing"].lower() == furnishing.lower()
    ]


def search_properties(properties, query):
    """Simple keyword search across title and location."""
    q = query.strip().lower()
    if not q:
        return properties
    return [
        p for p in properties
        if q in p["title"].lower() or q in p["location"].lower()
    ]


def calculate_price_per_sqft(price, area):
    """Return price-per-square-foot, raising ValueError for zero area."""
    if area <= 0:
        raise ValueError("Area must be greater than zero.")
    return round(price / area, 2)


def add_to_wishlist(wishlist, property_id):
    """Add a property id to the wishlist set; idempotent."""
    wishlist.add(property_id)
    return wishlist


def remove_from_wishlist(wishlist, property_id):
    """Remove a property id from the wishlist; no-op if absent."""
    wishlist.discard(property_id)
    return wishlist


def sort_properties(properties, key="price", reverse=False):
    """Sort properties by the given key."""
    return sorted(properties, key=lambda p: p.get(key, 0), reverse=reverse)


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

class TestPropertyDataIntegrity(unittest.TestCase):
    """Validate the sample dataset itself."""

    def test_all_properties_have_required_keys(self):
        required = {"id", "title", "type", "price", "bedrooms", "location",
                    "furnishing", "area"}
        for prop in PROPERTIES:
            self.assertTrue(required.issubset(prop.keys()),
                            f"Property {prop.get('id')} missing keys.")

    def test_all_prices_are_positive(self):
        for prop in PROPERTIES:
            self.assertGreater(prop["price"], 0,
                               f"Property {prop['id']} has non-positive price.")

    def test_all_areas_are_positive(self):
        for prop in PROPERTIES:
            self.assertGreater(prop["area"], 0,
                               f"Property {prop['id']} has non-positive area.")

    def test_unique_ids(self):
        ids = [p["id"] for p in PROPERTIES]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate property IDs found.")

    def test_dataset_has_minimum_properties(self):
        self.assertGreaterEqual(len(PROPERTIES), 5,
                                "Dataset must contain at least 5 properties.")


class TestFilterByType(unittest.TestCase):
    """Tests for type-based filtering."""

    def test_filter_apartments(self):
        result = filter_by_type(PROPERTIES, "Apartment")
        self.assertTrue(all(p["type"] == "Apartment" for p in result))
        self.assertEqual(len(result), 2)

    def test_filter_villas(self):
        result = filter_by_type(PROPERTIES, "Villa")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Luxury Sky Villa")

    def test_filter_commercial(self):
        result = filter_by_type(PROPERTIES, "Commercial")
        self.assertEqual(len(result), 1)

    def test_filter_all_returns_all(self):
        result = filter_by_type(PROPERTIES, "all")
        self.assertEqual(len(result), len(PROPERTIES))

    def test_filter_case_insensitive(self):
        result_lower = filter_by_type(PROPERTIES, "villa")
        result_upper = filter_by_type(PROPERTIES, "VILLA")
        self.assertEqual(len(result_lower), len(result_upper))

    def test_filter_nonexistent_type_returns_empty(self):
        result = filter_by_type(PROPERTIES, "Bungalow")
        self.assertEqual(result, [])


class TestFilterByPrice(unittest.TestCase):
    """Tests for price-range filtering."""

    def test_filter_budget_properties(self):
        result = filter_by_price(PROPERTIES, 0, 5000000)
        self.assertTrue(all(p["price"] <= 5000000 for p in result))

    def test_filter_luxury_properties(self):
        result = filter_by_price(PROPERTIES, 30000000)
        self.assertTrue(all(p["price"] >= 30000000 for p in result))
        self.assertEqual(len(result), 1)

    def test_no_properties_in_impossible_range(self):
        result = filter_by_price(PROPERTIES, 999999999, 999999999)
        self.assertEqual(result, [])

    def test_all_properties_in_full_range(self):
        result = filter_by_price(PROPERTIES, 0, float("inf"))
        self.assertEqual(len(result), len(PROPERTIES))


class TestFilterByBedrooms(unittest.TestCase):
    """Tests for bedroom count filtering."""

    def test_filter_1_bhk(self):
        result = filter_by_bedrooms(PROPERTIES, 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Modern Studio Apartment")

    def test_filter_4_bhk(self):
        result = filter_by_bedrooms(PROPERTIES, 4)
        self.assertEqual(len(result), 1)

    def test_no_filter_returns_all(self):
        result = filter_by_bedrooms(PROPERTIES, None)
        self.assertEqual(len(result), len(PROPERTIES))

    def test_commercial_zero_bedrooms(self):
        result = filter_by_bedrooms(PROPERTIES, 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "Commercial")


class TestFilterByFurnishing(unittest.TestCase):
    """Tests for furnishing status filtering."""

    def test_furnished_properties(self):
        result = filter_by_furnishing(PROPERTIES, "Furnished")
        self.assertTrue(all(p["furnishing"] == "Furnished" for p in result))

    def test_unfurnished_properties(self):
        result = filter_by_furnishing(PROPERTIES, "Unfurnished")
        self.assertEqual(len(result), 1)

    def test_semi_furnished(self):
        result = filter_by_furnishing(PROPERTIES, "Semi-Furnished")
        self.assertEqual(len(result), 2)

    def test_empty_furnishing_returns_all(self):
        result = filter_by_furnishing(PROPERTIES, "")
        self.assertEqual(len(result), len(PROPERTIES))


class TestSearchProperties(unittest.TestCase):
    """Tests for keyword search logic."""

    def test_search_by_city(self):
        result = search_properties(PROPERTIES, "Mumbai")
        self.assertEqual(len(result), 1)

    def test_search_by_partial_title(self):
        result = search_properties(PROPERTIES, "Penthouse")
        self.assertEqual(len(result), 1)

    def test_search_empty_returns_all(self):
        result = search_properties(PROPERTIES, "")
        self.assertEqual(len(result), len(PROPERTIES))

    def test_search_case_insensitive(self):
        result_lower = search_properties(PROPERTIES, "mumbai")
        result_upper = search_properties(PROPERTIES, "MUMBAI")
        self.assertEqual(len(result_lower), len(result_upper))

    def test_search_no_match(self):
        result = search_properties(PROPERTIES, "zxqwerty999")
        self.assertEqual(result, [])


class TestPricePerSqft(unittest.TestCase):
    """Tests for price-per-square-foot calculations."""

    def test_standard_calculation(self):
        result = calculate_price_per_sqft(3200000, 1000)
        self.assertAlmostEqual(result, 3200.0)

    def test_zero_area_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_price_per_sqft(5000000, 0)

    def test_negative_area_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_price_per_sqft(5000000, -100)

    def test_result_is_rounded(self):
        result = calculate_price_per_sqft(10000, 3)
        self.assertEqual(result, round(10000 / 3, 2))


class TestWishlistOperations(unittest.TestCase):
    """Tests for wishlist add/remove behaviour."""

    def test_add_property_to_wishlist(self):
        wishlist = set()
        add_to_wishlist(wishlist, 1)
        self.assertIn(1, wishlist)

    def test_add_duplicate_keeps_one_entry(self):
        wishlist = set()
        add_to_wishlist(wishlist, 1)
        add_to_wishlist(wishlist, 1)
        self.assertEqual(len(wishlist), 1)

    def test_remove_property_from_wishlist(self):
        wishlist = {1, 2, 3}
        remove_from_wishlist(wishlist, 2)
        self.assertNotIn(2, wishlist)

    def test_remove_nonexistent_is_safe(self):
        wishlist = {1}
        remove_from_wishlist(wishlist, 99)
        self.assertIn(1, wishlist)

    def test_multiple_properties_in_wishlist(self):
        wishlist = set()
        for pid in [1, 2, 3, 4]:
            add_to_wishlist(wishlist, pid)
        self.assertEqual(len(wishlist), 4)


class TestSortProperties(unittest.TestCase):
    """Tests for property sorting."""

    def test_sort_by_price_ascending(self):
        result = sort_properties(PROPERTIES, key="price", reverse=False)
        prices = [p["price"] for p in result]
        self.assertEqual(prices, sorted(prices))

    def test_sort_by_price_descending(self):
        result = sort_properties(PROPERTIES, key="price", reverse=True)
        prices = [p["price"] for p in result]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_sort_by_area(self):
        result = sort_properties(PROPERTIES, key="area")
        areas = [p["area"] for p in result]
        self.assertEqual(areas, sorted(areas))

    def test_sort_preserves_all_properties(self):
        result = sort_properties(PROPERTIES, key="price")
        self.assertEqual(len(result), len(PROPERTIES))


class TestCombinedFilters(unittest.TestCase):
    """Tests combining multiple filters (simulating the UI filter chain)."""

    def test_apartment_under_7m(self):
        results = filter_by_type(PROPERTIES, "Apartment")
        results = filter_by_price(results, 0, 7000000)
        self.assertTrue(all(
            p["type"] == "Apartment" and p["price"] <= 7000000
            for p in results
        ))

    def test_furnished_villa_in_mumbai(self):
        results = filter_by_type(PROPERTIES, "Villa")
        results = filter_by_furnishing(results, "Furnished")
        results = search_properties(results, "Mumbai")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["location"], "Mumbai")

    def test_2bhk_semi_furnished(self):
        results = filter_by_bedrooms(PROPERTIES, 2)
        results = filter_by_furnishing(results, "Semi-Furnished")
        self.assertEqual(len(results), 1)

    def test_penthouse_above_30m(self):
        results = filter_by_type(PROPERTIES, "Penthouse")
        results = filter_by_price(results, 30000000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Premium Penthouse")


if __name__ == "__main__":
    unittest.main(verbosity=2)
