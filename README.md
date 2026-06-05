# VANTAGE

> AI perception platform for law enforcement — marketing site with reference Python modules.

[![CI](https://github.com/pawell11/vantage/actions/workflows/ci.yml/badge.svg)](https://github.com/pawell11/vantage/actions/workflows/ci.yml)
[![Website](https://img.shields.io/badge/live-81.17.102.42-blue)](http://81.17.102.42/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Overview

VANTAGE is an AI perception concept for law enforcement — multi-camera tracking,
persistent re-identification, and behavioral analytics across CCTV, drones,
bodycams, and city networks.

This repository contains the static marketing site plus reference Python modules
that demonstrate the architecture concepts.

## Repository structure

```
├── index.html              # Marketing landing page
├── docs.html               # Documentation page
├── styles.css              # Dark-themed stylesheet
├── script.js               # Tab switching, modal, scroll animations
├── src/
│   ├── api/main.py         # FastAPI app (health, stream registration, ReID)
│   ├── ingestion/
│   │   └── stream_manager.py  # Stream lifecycle management
│   ├── tracking/
│   │   └── reid.py         # Re-identification embedding engine
│   └── fusion/__init__.py  # Sensor fusion stubs
├── tests/
│   └── test_core.py        # 10 pytest tests covering all modules
├── hermes/                 # AI agent deployment config
├── .github/workflows/      # CI pipeline
├── LICENSE                 # MIT
├── CONTRIBUTING.md
└── SECURITY.md
```

## Quick start

```bash
# Serve the marketing site
python3 -m http.server 8080

# Run tests
pip install pytest numpy fastapi pytest-asyncio
python -m pytest tests/ -v

# Start the API
uvicorn src.api.main:app --port 8443
```

## Live

- **Marketing site:** http://81.17.102.42/
- **GitHub Pages:** https://pawell11.github.io/vantage/

## Contact

**Email:** [vantageaiservices@gmail.com](mailto:vantageaiservices@gmail.com)