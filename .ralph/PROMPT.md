# SuperSearch - Complete Implementation for Periodic Labs

## Mission
Build a production-quality superconductor visualization tool that demonstrates clear value to Periodic Labs' autonomous lab and AI scientist systems.

## Success Criteria (ALL Must Pass)

### Content/Features (Most Important)
- [ ] **Opportunity Regions Panel:** 5-10 ranked unexplored composition regions
  - Region coordinates and size
  - Why valuable (near high-Tc, experimental gaps)
  - Priority ranking (which to synthesize first)
  - Visual highlighting on 3D viz
- [ ] **High-Tc Materials List:** Top 10-20 materials by transition temperature
  - Formula, Tc value, composition details
  - Position in 3D space
- [ ] **Cluster Analysis Display:**
  - Number of clusters identified
  - Average properties per cluster
  - Composition patterns
- [ ] **Strategic Context (About Overlay):**
  - How this complements GNoME predictions
  - How it guides autonomous lab prioritization
  - Hypothesis generation capability
  - Integration roadmap with Periodic Labs systems
- [ ] **Interactive Features:**
  - Click on regions to see details
  - Hover tooltips on points
  - Toggle different views/insights

### Visual/Branding
- [ ] Cream background (#F5F3ED) matches periodiclabs.com
- [ ] Fragment Mono font throughout
- [ ] Dark text on light background
- [ ] Minimal, professional design
- [ ] No dark mode appearance

### Technical
- [ ] All features work without overlapping UI
- [ ] Loads in <2 seconds
- [ ] No console errors
- [ ] 3D visualization visible on light background
- [ ] Point colors adjusted for visibility
- [ ] Controls work (rotate, zoom)

## Data Available
File: `data/analysis_results_fast.json` contains:
- 5,000 materials with x, y, tc (transition temp), cluster assignments
- metadata.sparse_regions: List of opportunity regions with coordinates
- Materials have: atomic_mass, atomic_radius, valence fields

## Implementation Priority
**Phase 1:** Core content (opportunity regions, top materials, clusters)
**Phase 2:** Styling (cream background, Fragment Mono)
**Phase 3:** Interactive features
**Phase 4:** About overlay with strategic context

## Value Proposition for Periodic Labs
**"Where should our autonomous lab synthesize next?"**
- Sparse region analysis → experimental priorities
- Composition gap identification → unexplored space
- High-Tc patterns → hypothesis generation
- Complements GNoME predictions with experimental coverage analysis

## UI Layout
```
┌─────────────────────────────────────────────┐
│ Header: SuperSearch                         │
│ Subtitle: Superconductor Composition Explorer│
├─────────────────────────────────────────────┤
│                                             │
│          [3D Visualization]                 │
│                                             │
│                                             │
│  [Opportunity Regions]    [Top Materials]   │
│  - Region 1: coords...    - Material 1...   │
│  - Region 2: coords...    - Material 2...   │
│  - Region 3: coords...                      │
│                                             │
│  [Cluster Stats]                            │
│  - 3 clusters identified                    │
│  - Avg Tc per cluster                       │
│                                             │
│  [About] button → overlay with strategic    │
│           context for Periodic Labs         │
└─────────────────────────────────────────────┘
```

## Files to Modify
- `docs/index.html` - main implementation file

## Testing Checklist
- [ ] Load locally, verify all content displays
- [ ] Check opportunity regions load from data
- [ ] Check top materials sorted by Tc
- [ ] Check cluster stats calculated correctly
- [ ] Verify cream background
- [ ] Verify Fragment Mono font loaded
- [ ] Verify no UI overlaps
- [ ] Test on 1920x1080 display
- [ ] Check console for errors
- [ ] Deploy to GitHub Pages
- [ ] Verify live site works

## Report Format on Completion
```
✓ Opportunity regions panel: 5 regions displayed with priorities
✓ Top materials list: 20 materials sorted by Tc
✓ Cluster analysis: 3 clusters with stats
✓ Strategic context overlay: complete
✓ Cream background + Fragment Mono
✓ All features functional, no overlaps
✓ Tested locally - passes all criteria
✓ Deployed to GitHub Pages
✓ Verified live: https://reubenrunacres.github.io/supersearch/
```
