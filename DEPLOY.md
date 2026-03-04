# Deployment Guide

## Quick Start (Local)

```bash
cd web
python3 -m http.server 8000
# Open http://localhost:8000
```

## Deploy to Production

### Option 1: GitHub Pages (Free)

```bash
# 1. Create new repo on GitHub
# 2. Push this project
# 3. Enable GitHub Pages in repo settings
# 4. Point to /web folder or move index.html to root
```

### Option 2: Vercel/Netlify (Free)

```bash
# 1. Connect GitHub repo to Vercel/Netlify
# 2. Set build output to /web
# 3. Deploy
```

### Option 3: Self-hosted

```bash
# Copy /web folder to web server
# Ensure data/analysis_results.json is accessible
# Serve as static files
```

## Testing Locally

```bash
# Verify all files present
ls web/index.html
ls data/analysis_results.json

# Check JSON is valid
python3 -c "import json; json.load(open('data/analysis_results.json'))"

# Start server
cd web && python3 -m http.server 8000

# Visit http://localhost:8000 in browser
```

## Requirements

- Static web server (any)
- No backend needed
- No build step required
- All assets inline (D3.js loaded from CDN)

## File Structure for Deployment

```
/
├── index.html (from web/)
└── data/
    └── analysis_results.json (3.1MB)
```

That's it! Single HTML file + one JSON data file.
