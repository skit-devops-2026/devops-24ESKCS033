# Food Expression

[![CI Pipeline](https://github.com/guptaakshat6917-cell/food-expression/actions/workflows/ci.yml/badge.svg)](https://github.com/guptaakshat6917-cell/food-expression/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Food Expression** is a modular Python-based order calculation and shopping cart engine designed for modern food delivery and restaurant platforms. It provides reliable, well-tested business logic for computing cart totals, applying promotional discounts with strict validation, calculating regional sales tax, and assembling final order summaries.

---

## Features

- **Cart Subtotal Calculation**: Safely computes totals across multi-item orders accounting for unit pricing and quantities.
- **Discount Engine**: Validates discount boundaries (0% to 100%) and accurately applies promotional reductions.
- **Tax Calculation**: Calculates sales tax based on applicable rates with robust input verification.
- **Order Summary Generation**: Produces comprehensive order breakdowns including subtotal, discount, taxable base, tax amount, and net payable total.
- **Automated Testing Suite**: High-coverage unit tests powered by pytest.
- **CI/CD Pipelines**: Continuous Integration configured via GitHub Actions and enterprise automation ready via Jenkins.

---

## Project Structure

`
food-expression/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI automated test workflow
├── cart.py                    # Core business logic for cart and checkout
├── test_cart.py               # Automated unit test suite (pytest)
├── Jenkinsfile                # Declarative Jenkins CI/CD pipeline definition
├── .gitignore                 # Repository ignore rules (prevents build artifacts)
└── README.md                  # Project documentation and developer guide
`

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip package manager

### Installation

1. Clone the repository:
   `ash
   git clone https://github.com/guptaakshat6917-cell/food-expression.git
   cd food-expression
   `

2. Create and activate a virtual environment:
   `ash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   `

3. Install testing dependencies:
   `ash
   pip install pytest pytest-cov flake8
   `

---

## Running Tests Locally

Run the complete test suite using pytest:

`ash
pytest -v
`

To run tests with code coverage:

`ash
pytest --cov=cart --cov-report=term-missing
`

To run lint checks:

`ash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
`

---

## CI/CD Pipeline

### GitHub Actions (.github/workflows/ci.yml)

The repository includes a GitHub Actions workflow that automatically executes on:
- Every push to any branch.
- Every pull_request targeting the main branch.
- Manual trigger (workflow_dispatch).

The pipeline performs:
1. Multi-version testing against Python 3.10 and 3.11.
2. Dependency installation (pytest, lake8).
3. Code quality inspection and lint checks.
4. Execution of the automated test suite with JUnit XML reporting.

### Jenkins Pipeline (Jenkinsfile)

A declarative Jenkins pipeline is provided to execute automated builds on local or dedicated Jenkins nodes.
Stages include:
1. **Checkout**: Retrieves source code from Git SCM.
2. **Setup**: Prepares Python virtual environment and installs requirements.
3. **Lint**: Validates syntax and code cleanliness with Flake8.
4. **Test**: Executes tests and generates JUnit-compatible test reports.
5. **Archive**: Collects and archives test artifacts and results.

---

## Git Workflow & Branching Strategy

Development follows standard Git Flow and Pull Request conventions:
- main: Production-ready, stable code branch. All changes are merged deliberately via reviewed Pull Requests.
- eature/*: Short-lived feature branches for bug fixes, enhancements, and CI/CD integration.
- Direct pushes to main are avoided in favor of documented, traceable pull requests.
