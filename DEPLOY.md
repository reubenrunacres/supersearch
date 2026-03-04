# Deployment Guide

SuperSearch is a static site (HTML + JS + JSON data) and can be deployed anywhere static files are served.

## Quick Deploy Options

### Option 1: GitHub Pages (Recommended)

```bash
# 1. Create GitHub repo
gh repo create supersearch --public --source=. --remote=origin

# 2. Push to GitHub
git push -u origin main

# 3. Enable GitHub Pages
gh repo edit --enable-pages --pages-branch main --pages-path /web

# Done! Site will be live at:
# https://yourusername.github.io/supersearch/
```

### Option 2: Vercel (Fastest)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy (from project root)
vercel

# Follow prompts to link project
# Vercel will auto-detect static site

# Set build settings:
# - Framework Preset: Other
# - Root Directory: web
# - Output Directory: web

# Done! Site will be at:
# https://supersearch-abc123.vercel.app
```

### Option 3: Netlify

1. Go to https://app.netlify.com/drop
2. Drag the `/web` folder onto the page
3. Done! Instant deploy with random URL

Or use Netlify CLI:

```bash
npm install -g netlify-cli
cd web
netlify deploy --prod
```

### Option 4: Manual Server

Any web server can host the `web/` directory:

```bash
# Python
cd web && python3 -m http.server 8000

# Node.js
npm install -g http-server
cd web && http-server -p 8000

# Nginx
# Copy web/ to /var/www/html/supersearch/
```

## Configuration

### Update README Links

After deployment, update these in `README.md`:

```markdown
[View Live Demo](https://your-deployed-url.com)
```

### Custom Domain (Optional)

**GitHub Pages:**
1. Add `CNAME` file to `web/` with your domain
2. Configure DNS A records to GitHub Pages IPs
3. Enable HTTPS in repo settings

**Vercel:**
1. Go to project settings → Domains
2. Add custom domain
3. Follow DNS instructions

**Netlify:**
1. Go to Domain settings
2. Add custom domain
3. Follow DNS setup

## Data Updates

The visualization loads data from `/data/analysis_results.json`. To update:

```bash
# 1. Update source data (data/train.csv)
# 2. Re-run analysis
python analyze_data.py

# 3. Copy results to web directory
cp data/analysis_results.json web/data/

# 4. Commit and push
git add web/data/analysis_results.json
git commit -m "Update analysis results"
git push
```

## Performance Optimization

The site is already optimized, but for even faster loading:

### 1. Compress JSON
```bash
# Gzip the data file (most hosts auto-decompress)
gzip -9 web/data/analysis_results.json
```

### 2. Use CDN
- GitHub Pages: Automatically uses Fastly CDN
- Vercel: Built-in Edge Network
- Netlify: Built-in CDN
- Custom: CloudFlare (free tier)

### 3. Minify (Optional)
The HTML is already minimal, but if needed:

```bash
npm install -g html-minifier
html-minifier --collapse-whitespace --remove-comments \
  web/index.html -o web/index.min.html
```

## Troubleshooting

### Data not loading
- Check browser console for 404 errors
- Verify `analysis_results.json` path is correct
- Ensure JSON is valid (run through JSONLint)

### Blank visualization
- Open browser DevTools → Network tab
- Check if D3.js loaded (should see d3.v7.min.js)
- Verify no JavaScript errors in console

### Slow loading
- Check data file size (should be ~3.2MB)
- Consider compressing with gzip
- Use a CDN for faster global delivery

## Local Development

```bash
# Serve locally
cd web
python3 -m http.server 8000

# Open http://localhost:8000
```

## CI/CD (Optional)

### GitHub Actions
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./web
```

### Vercel Auto-Deploy
- Connected repos auto-deploy on push
- Preview deployments for pull requests
- Production deployment on merge to main

---

**Questions?** Open an issue on GitHub or contact [your email].
