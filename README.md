# Video Downloader MVP

A simple URL-based downloader web app for media sources that are permitted to be downloaded.
It intentionally does not bypass DRM, authentication, paywalls, or platform protections.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Deploy

This project can be deployed to a Python-compatible VPS/container host.
For a free public URL, use a provider's free-tier subdomain where available.
