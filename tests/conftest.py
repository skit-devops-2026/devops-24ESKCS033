"""
conftest.py – Shared pytest fixtures for RealEstate test suite.

Student: Akshat Gupta | 24ESKCS019
Course:  DevOps (MT1 – Modules 1-4)
"""

import pytest
import os

from tests.test_properties import (
    PROPERTIES,
    filter_by_type,
    filter_by_price,
    add_to_wishlist,
    remove_from_wishlist,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def all_properties():
    """Return a fresh copy of the full property dataset."""
    return list(PROPERTIES)


@pytest.fixture
def apartments(all_properties):
    """Return only Apartment-type properties."""
    return filter_by_type(all_properties, "Apartment")


@pytest.fixture
def villas(all_properties):
    """Return only Villa-type properties."""
    return filter_by_type(all_properties, "Villa")


@pytest.fixture
def budget_properties(all_properties):
    """Return properties priced at or below 7,000,000."""
    return filter_by_price(all_properties, 0, 7_000_000)


@pytest.fixture
def luxury_properties(all_properties):
    """Return properties priced above 20,000,000."""
    return filter_by_price(all_properties, 20_000_001)


@pytest.fixture
def empty_wishlist():
    """Return an empty wishlist set."""
    return set()


@pytest.fixture
def populated_wishlist():
    """Return a wishlist pre-populated with property IDs 1–3."""
    wishlist = set()
    for pid in [1, 2, 3]:
        add_to_wishlist(wishlist, pid)
    return wishlist


@pytest.fixture
def project_root():
    """Return the absolute path to the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
