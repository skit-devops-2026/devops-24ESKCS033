"""
conftest.py – Shared pytest fixtures for RealEstate test suite.

NOTE: This file intentionally does NOT import from other test modules.
conftest.py is loaded by pytest before test collection and relative
imports inside it are unreliable across all pytest invocation modes.
All fixtures are self-contained.

Student: Akshat Gupta | 24ESKCS019
Course:  DevOps (MT1 – Modules 1-4)
"""

import pytest
import os


# ---------------------------------------------------------------------------
# Inline property data (mirrors tests/test_properties.py PROPERTIES list)
# ---------------------------------------------------------------------------

_PROPERTIES = [
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


def _filter_by_type(properties, prop_type):
    if not prop_type or prop_type.lower() == "all":
        return properties
    return [p for p in properties if p["type"].lower() == prop_type.lower()]


def _filter_by_price(properties, min_price=0, max_price=float("inf")):
    return [p for p in properties if min_price <= p["price"] <= max_price]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def all_properties():
    """Return a fresh copy of the full property dataset."""
    return list(_PROPERTIES)


@pytest.fixture
def apartments(all_properties):
    """Return only Apartment-type properties."""
    return _filter_by_type(all_properties, "Apartment")


@pytest.fixture
def villas(all_properties):
    """Return only Villa-type properties."""
    return _filter_by_type(all_properties, "Villa")


@pytest.fixture
def budget_properties(all_properties):
    """Return properties priced at or below 7,000,000."""
    return _filter_by_price(all_properties, 0, 7_000_000)


@pytest.fixture
def luxury_properties(all_properties):
    """Return properties priced above 20,000,000."""
    return _filter_by_price(all_properties, 20_000_001)


@pytest.fixture
def empty_wishlist():
    """Return an empty wishlist set."""
    return set()


@pytest.fixture
def populated_wishlist():
    """Return a wishlist pre-populated with property IDs 1–3."""
    return {1, 2, 3}


@pytest.fixture
def project_root():
    """Return the absolute path to the project root directory."""
    # conftest.py lives at <root>/tests/conftest.py
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
