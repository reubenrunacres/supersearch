# Agent Configuration

## Project Context
Three.js visualization of 21,263 superconductors for Periodic Labs demo. Self-contained HTML file deployment.

## Build Commands
```bash
# No build step needed - static HTML site
# But can minify for production:
# npx html-minifier --collapse-whitespace --remove-comments docs/index.html > docs/index.min.html
```

## Test Commands
```bash
# Start local server
cd docs && python3 -m http.server 8766

# Open in browser
open http://localhost:8766

# Check for errors
# Manual: Open Chrome DevTools Console
# Performance: Chrome DevTools Performance tab
```

## Deploy Commands
```bash
# Commit and push to GitHub Pages
git add docs/index.html
git commit -m "Enhancement: [description]"
git push origin main

# Verify deployment
curl -I https://reubenrunacres.github.io/supersearch/
```

## Verification Checklist
- [ ] No console errors
- [ ] Loads in < 3 seconds
- [ ] 60fps rendering
- [ ] All interactive features work
- [ ] Data loads successfully
- [ ] Tooltips appear on hover
- [ ] Camera presets functional
- [ ] Legend filters work
- [ ] Responsive on different screen sizes

## Code Style
- ES6+ JavaScript
- 2-space indentation
- camelCase for variables
- PascalCase for classes
- Descriptive function names
- JSDoc comments for public functions

## Critical Files
- `docs/index.html` - Main visualization (edit this)
- `data/analysis_results.json` - Data source (don't modify)
- Local server for testing: port 8766

## Performance Constraints
- Must render 21,263 points smoothly
- Target: 60fps on MacBook Pro M1
- File size: Keep under 50KB (currently 28KB)
- No external dependencies except CDN scripts

## Browser Targets
- Chrome 90+ (primary)
- Safari 14+ (secondary)
- Firefox 88+ (tertiary)
- Mobile: iOS Safari, Chrome Android (bonus)
