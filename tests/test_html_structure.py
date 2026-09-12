"""
Unit tests for HTML structure of the RealEstate Property Discovery Platform.
Validates that index.html contains the required DOM elements and metadata.

Student: Akshat Gupta | 24ESKCS019
Course:  DevOps (MT1 – Modules 1-4)
"""

import unittest
import os
import re


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_FILE = os.path.join(BASE_DIR, "index.html")


def read_html():
    """Read and return the full contents of index.html."""
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

class TestHTMLFileExists(unittest.TestCase):
    """Ensure index.html is present."""

    def test_html_file_exists(self):
        self.assertTrue(os.path.isfile(HTML_FILE),
                        f"index.html not found at {HTML_FILE}")

    def test_html_file_is_not_empty(self):
        self.assertGreater(os.path.getsize(HTML_FILE), 0,
                           "index.html must not be empty.")


class TestHTMLMetadata(unittest.TestCase):
    """Validate key HTML meta tags and document structure."""

    def setUp(self):
        self.html = read_html()

    def test_has_doctype(self):
        self.assertIn("<!DOCTYPE html>", self.html,
                      "index.html must start with <!DOCTYPE html>.")

    def test_has_title_tag(self):
        self.assertIn("<title>", self.html, "index.html must have a <title> tag.")

    def test_has_viewport_meta(self):
        self.assertIn("viewport", self.html,
                      "index.html must include a viewport meta tag.")

    def test_has_charset_meta(self):
        self.assertIn("charset", self.html,
                      "index.html must include a charset declaration.")

    def test_has_html_lang_attribute(self):
        self.assertRegex(self.html, r'<html[^>]+lang=',
                         "index.html must declare a lang attribute on <html>.")


class TestHTMLStructure(unittest.TestCase):
    """Validate the required sections and components exist in the HTML."""

    def setUp(self):
        self.html = read_html()

    def test_has_header(self):
        self.assertIn("<header", self.html,
                      "index.html must contain a <header> element.")

    def test_has_nav(self):
        self.assertIn("<nav", self.html,
                      "index.html must contain a <nav> element.")

    def test_has_main_content_area(self):
        has_main = "<main" in self.html or 'id="main"' in self.html or 'class="main' in self.html
        self.assertTrue(has_main, "index.html must contain a main content area.")

    def test_has_footer(self):
        self.assertIn("<footer", self.html,
                      "index.html must contain a <footer> element.")

    def test_has_search_input(self):
        has_search = 'type="search"' in self.html or 'id="search' in self.html or 'search' in self.html.lower()
        self.assertTrue(has_search, "index.html must contain a search input.")

    def test_has_property_grid_or_container(self):
        has_grid = ('property' in self.html.lower() and
                    ('grid' in self.html.lower() or 'container' in self.html.lower()
                     or 'list' in self.html.lower()))
        self.assertTrue(has_grid, "index.html must contain a properties display section.")

    def test_has_filter_section(self):
        has_filter = 'filter' in self.html.lower() or 'Filter' in self.html
        self.assertTrue(has_filter, "index.html must include property filter controls.")

    def test_stylesheet_linked(self):
        self.assertIn("style.css", self.html,
                      "index.html must link to style.css.")

    def test_script_linked(self):
        self.assertIn("script.js", self.html,
                      "index.html must link to script.js.")


class TestHTMLAccessibility(unittest.TestCase):
    """Basic accessibility checks."""

    def setUp(self):
        self.html = read_html()

    def test_images_have_alt_attributes(self):
        img_tags = re.findall(r'<img[^>]*>', self.html, re.IGNORECASE)
        for img in img_tags:
            self.assertIn("alt=", img,
                          f"All <img> tags must have an alt attribute. Found: {img[:80]}")

    def test_has_aria_or_role_attributes(self):
        has_aria = "aria-" in self.html or 'role="' in self.html
        self.assertTrue(has_aria,
                        "index.html should include ARIA attributes for accessibility.")

    def test_form_inputs_have_labels_or_placeholders(self):
        input_tags = re.findall(r'<input[^>]*>', self.html, re.IGNORECASE)
        for inp in input_tags:
            has_label = ("placeholder=" in inp or "aria-label=" in inp or
                         "id=" in inp or "type=\"hidden\"" in inp)
            self.assertTrue(has_label,
                            f"Input must have a placeholder or label: {inp[:80]}")


class TestAdditionalProjectFiles(unittest.TestCase):
    """Confirm required project files are present."""

    def test_gitignore_exists(self):
        path = os.path.join(BASE_DIR, ".gitignore")
        self.assertTrue(os.path.isfile(path), ".gitignore must exist.")

    def test_readme_exists(self):
        path = os.path.join(BASE_DIR, "README.md")
        self.assertTrue(os.path.isfile(path), "README.md must exist.")

    def test_jenkinsfile_exists(self):
        path = os.path.join(BASE_DIR, "Jenkinsfile")
        self.assertTrue(os.path.isfile(path), "Jenkinsfile must exist.")

    def test_ci_workflow_exists(self):
        path = os.path.join(BASE_DIR, ".github", "workflows", "ci.yml")
        self.assertTrue(os.path.isfile(path),
                        ".github/workflows/ci.yml must exist.")

    def test_stylesheet_exists(self):
        path = os.path.join(BASE_DIR, "style.css")
        self.assertTrue(os.path.isfile(path), "style.css must exist.")

    def test_script_exists(self):
        path = os.path.join(BASE_DIR, "script.js")
        self.assertTrue(os.path.isfile(path), "script.js must exist.")


class TestReadmeCompleteness(unittest.TestCase):
    """Verify README.md contains expected project documentation sections."""

    def setUp(self):
        readme_path = os.path.join(BASE_DIR, "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            self.readme = f.read()

    def test_readme_has_project_title(self):
        self.assertIn("RealEstate", self.readme,
                      "README.md must mention the project name.")

    def test_readme_has_author_info(self):
        has_author = "Akshat Gupta" in self.readme or "24ESKCS019" in self.readme
        self.assertTrue(has_author, "README.md must include author information.")

    def test_readme_has_getting_started(self):
        has_gs = "Getting Started" in self.readme or "Installation" in self.readme or "Clone" in self.readme
        self.assertTrue(has_gs, "README.md must include getting-started instructions.")

    def test_readme_has_ci_badge(self):
        has_badge = "CI Pipeline" in self.readme or "badge" in self.readme.lower() or "actions" in self.readme.lower()
        self.assertTrue(has_badge, "README.md should include a CI badge.")

    def test_readme_mentions_tests(self):
        has_tests = "test" in self.readme.lower() or "pytest" in self.readme.lower()
        self.assertTrue(has_tests, "README.md must mention the test suite.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
