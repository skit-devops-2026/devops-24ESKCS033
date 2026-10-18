# ============================================================
# RealEstate – Property Discovery Platform
# Dockerfile
# Serves static HTML/CSS/JS via Python's built-in HTTP server
# ============================================================

# ── Base image ───────────────────────────────────────────────
FROM python:3.11-slim

# ── Metadata labels ──────────────────────────────────────────
LABEL maintainer="Akshat Gupta <24ESKCS019>"
LABEL project="RealEstate – Property Discovery Platform"
LABEL course="DevOps 24ESKCS033"
LABEL version="1.0.0"

# ── Working directory ────────────────────────────────────────
WORKDIR /app

# ── Copy static site files ───────────────────────────────────
COPY index.html   ./index.html
COPY style.css    ./style.css
COPY script.js    ./script.js

# ── Copy test suite (kept for CI parity, not used at runtime) ─
COPY tests/       ./tests/
COPY pytest.ini   ./pytest.ini

# ── Environment configuration ────────────────────────────────
# PORT can be overridden at runtime via -e PORT=xxxx
ENV PORT=8000

# ── Expose the HTTP server port ──────────────────────────────
EXPOSE 8000

# ── Health check ─────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}')" || exit 1

# ── Start the application ────────────────────────────────────
# Uses Python's built-in HTTP server to serve the static files.
# Shell form is intentional so $PORT is evaluated at runtime.
CMD python -m http.server $PORT
