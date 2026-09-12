"""
Fixture-based tests using pytest conftest fixtures.
Validates the shared fixtures and demonstrates pytest fixture usage.

Student: Akshat Gupta | 24ESKCS019
Course:  DevOps (MT1 – Modules 1-4)
"""

import pytest


class TestFixturesWork:
    """Verify all shared conftest fixtures load and return correct data."""

    def test_all_properties_fixture_returns_full_dataset(self, all_properties):
        assert len(all_properties) >= 5

    def test_apartments_fixture_only_returns_apartments(self, apartments):
        assert all(p["type"] == "Apartment" for p in apartments)
        assert len(apartments) >= 1

    def test_villas_fixture_only_returns_villas(self, villas):
        assert all(p["type"] == "Villa" for p in villas)

    def test_budget_properties_within_price(self, budget_properties):
        assert all(p["price"] <= 7_000_000 for p in budget_properties)

    def test_luxury_properties_above_price(self, luxury_properties):
        assert all(p["price"] > 20_000_000 for p in luxury_properties)

    def test_empty_wishlist_is_empty(self, empty_wishlist):
        assert len(empty_wishlist) == 0

    def test_populated_wishlist_has_3_items(self, populated_wishlist):
        assert len(populated_wishlist) == 3
        assert 1 in populated_wishlist
        assert 2 in populated_wishlist
        assert 3 in populated_wishlist

    def test_project_root_contains_readme(self, project_root):
        import os
        readme = os.path.join(project_root, "README.md")
        assert os.path.isfile(readme)

    def test_project_root_contains_jenkinsfile(self, project_root):
        import os
        jenkinsfile = os.path.join(project_root, "Jenkinsfile")
        assert os.path.isfile(jenkinsfile)

    def test_project_root_contains_gitignore(self, project_root):
        import os
        gitignore = os.path.join(project_root, ".gitignore")
        assert os.path.isfile(gitignore)

    def test_fixtures_are_independent(self, all_properties, apartments):
        """Modifying apartments should not affect all_properties."""
        original_count = len(all_properties)
        apartments.clear()
        assert len(all_properties) == original_count
