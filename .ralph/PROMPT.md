# SuperSearch v1 → v2: Research Tool Transformation

## Mission
Transform SuperSearch from a "cool demo" into a research tool that materials science labs actually want to use. Implement improvements systematically following the 2-week build schedule.

## Current State
- 3D visualization of 5,000 superconductors (sampled from 21,263)
- PCA-reduced composition space (X/Z axes), Tc as height (Y axis)
- Basic hover tooltips, cluster coloring, 34 opportunity regions
- Pure static site (Three.js + JSON data)
- **Problem:** Anonymous data points, no filtering, weak opportunity scoring, no actionable workflows

## Build Schedule (2 Weeks)

### **Week 1, Days 1-2: Data Layer**
**Files:** `data/train.csv`, `analyze_data.py`, `docs/data/analysis_results_fast.json`

1. **Add chemical formula names**
   - Extract formula strings from UCI dataset
   - Add `formula` field to each material in JSON
   - Format subscripts properly (e.g., "HgBa₂Ca₂Cu₃O₈")

2. **Add UMAP coordinates**
   - Install `umap-learn`: `pip install umap-learn`
   - Compute UMAP projection of 81-feature dataset (n_neighbors=15, min_dist=0.1)
   - Add `umap_x`, `umap_y` fields to JSON alongside existing `x`, `y` (PCA)
   - Keep both projection types available

**Deliverable:** Updated `analysis_results_fast.json` with `formula`, `umap_x`, `umap_y` fields

---

### **Week 1, Days 3-4: Core UX**
**Files:** `docs/index.html`

3. **Named materials in tooltips**
   - Display chemical formula prominently in hover tooltip
   - Format: `"HgBa₂Ca₂Cu₃O₈ • Tc: 135K"`
   - Move formula above other stats (atomic mass, radius, etc.)

4. **Click-to-inspect detail card**
   - Click any point → slide-out detail panel from right side
   - Show all available features grouped logically:
     - **Identity:** Chemical formula
     - **Thermal:** Tc, Tc range
     - **Composition:** Atomic mass, radius, valence, density
     - **Clustering:** Cluster assignment, PCA coords, UMAP coords
   - Add "Find Similar" button: Highlight 10 nearest neighbors in 3D view
   - Add "Copy Feature Vector" button (JSON to clipboard)
   - Close with X button or clicking outside

5. **Element text search**
   - Search box in header: "Search elements (e.g., Cu, Hg)"
   - Type element symbol → matching materials highlight in gold/yellow
   - Show count: "42 materials containing Cu"
   - Clear button to reset

**Deliverable:** Interactive tooltips with formulas, detail panel with "Find Similar", element search

---

### **Week 1, Days 5-6: Filtering**
**Files:** `docs/index.html`

6. **Filter control panel** (left sidebar, collapsible)
   - **Tc range slider** (0–185K, dual-handle)
   - **Element filter:** Multi-select checkboxes or text input tags
   - **Cluster toggle:** Show/hide clusters 0, 1, -1 independently
   - **Quick filters:**
     - "Above LN₂" button (Tc > 77K) — scientifically meaningful threshold
     - "High-Tc" (Tc > 100K)
     - "Cuprates" (materials containing Cu + O)
   - **Atomic property sliders:**
     - Mass range
     - Radius range
     - Valence range
   - Apply filters in real-time (animate point visibility transitions)
   - Show active filter count badge

**Deliverable:** Full filtering system with Tc slider, element filter, cluster toggles, quick filters

---

### **Week 1, Day 7: Projection Axis Switching**
**Files:** `docs/index.html`

7. **Axis selector dropdowns**
   - Three dropdowns in header: X-axis, Y-axis, Z-axis
   - Options: Tc, Atomic Mass, Atomic Radius, Valence, Density, PCA-1, PCA-2, UMAP-1, UMAP-2
   - Default: X=PCA-1, Y=Tc, Z=PCA-2
   - **Animate transitions:** Smoothly interpolate point positions over 800ms when axes change
   - Preset buttons:
     - "PCA Overview" (default)
     - "UMAP Overview" (X=UMAP-1, Y=Tc, Z=UMAP-2)
     - "Tc vs Mass" (X=Mass, Y=Tc, Z=Radius)
     - "Valence Space" (X=Valence, Y=Tc, Z=Radius)

**Deliverable:** Axis selection with smooth animated transitions, 4 preset views

---

### **Week 2, Days 1-2: AI Layer**
**Files:** `docs/index.html`

8. **Claude API synthesis candidate explainer**
   - Add "Why is this a good candidate?" button on:
     - Opportunity region cards
     - Material detail panels (when clicked)
   - Call Claude Sonnet API with prompt:
     ```
     You are a materials science research assistant. Analyze this superconductor synthesis candidate:
     
     Region/Material: [feature vector]
     Nearby materials: [list of 5 nearest neighbors with Tc values]
     Cluster context: [cluster stats]
     
     Provide a 2-3 sentence scientific rationale explaining why this is a promising synthesis candidate. Focus on:
     - Composition space position (proximity to high-Tc materials)
     - Sparseness/novelty
     - Relevant superconducting physics (e.g., valence, doping)
     
     Be specific and technically accurate. Use plain scientific language.
     ```
   - Display response in expandable card below button
   - Loading state while API responds
   - Error handling with fallback message

**Deliverable:** AI-powered "Why?" explainer on regions and materials

---

### **Week 2, Days 3-4: Smarter Opportunity Region Scoring**
**Files:** `analyze_data.py`, `docs/data/analysis_results_fast.json`, `docs/index.html`

9. **Multi-factor composite scoring**
   - Upgrade from pure density to weighted composite:
     - **Sparseness score (40%):** Low density = higher score
     - **Proximity to high-Tc (30%):** Average Tc of nearest 10 neighbors
     - **Compositional novelty (20%):** Diversity of cluster membership in neighborhood
     - **Synthesis feasibility proxy (10%):** Penalize extreme atomic radius mismatches
   - Calculate scores in Python preprocessing
   - Add `score`, `score_breakdown` fields to `sparse_regions` in JSON
   - Sort regions by total score (highest first)

10. **Visual score breakdown**
    - In opportunity region cards, show 4 colored horizontal bars:
      - Green: Sparseness
      - Purple: Proximity to high-Tc
      - Blue: Compositional novelty
      - Orange: Synthesis feasibility
    - Bars sum to 100% width
    - Tooltip on each bar shows exact percentage
    - Total score displayed prominently (e.g., "Score: 8.7/10")

**Deliverable:** Multi-factor scoring system with visual breakdown in region cards

---

### **Week 2, Days 5-6: Polish**
**Files:** `docs/index.html`

11. **Interactive onboarding tour**
    - Replace static About modal with 4-step guided tour (first visit only)
    - Use localStorage to track completion
    - Steps:
      1. "These 5,000 points represent known superconductors — height = critical temperature"
      2. "Blue regions are copper-oxide based materials, the current record holders" (highlight cuprate cluster)
      3. "Green spheres are unexplored composition zones — potential discovery targets" (highlight opportunity regions)
      4. "Use the panels on the right to drill in" (highlight side panels)
    - Skip button, "Don't show again" checkbox
    - Overlay with spotlight effect (dim rest of UI)

12. **Periodic table heatmap view**
    - Add "Periodic Table" tab/button in header
    - Show interactive 2D periodic table where each element is colored by:
      - **Frequency in high-Tc materials** (Tc > 77K)
      - Tooltip shows: Average Tc, count in dataset, elements it commonly pairs with
    - Click element → filter 3D view to materials containing it
    - Common superconductor elements highlighted: Cu, Hg, Ba, Ca, La, Y, Bi, Sr, Tl, Pb, Fe, As, etc.

**Deliverable:** 4-step onboarding tour, periodic table heatmap view with click-to-filter

---

### **Week 2, Day 7: Credibility & Sharing**
**Files:** `docs/index.html`, `README.md`

13. **URL state sharing**
    - Encode filter state + pinned materials + current projection in URL hash
    - Format: `#filters=tc:77-185,elements:Cu|Hg&projection=umap&pinned=1234,5678`
    - Update URL on state changes (debounced)
    - Parse URL on load and restore state
    - "Copy shareable link" button

14. **Hypothesis board & export**
    - "Pin to hypothesis board" button on materials and regions
    - Sidebar panel showing pinned items
    - Add text annotations to each pinned item
    - Export to PDF (formatted synthesis candidate report) or CSV (feature vectors)

15. **Citation & provenance panel**
    - Footer section or collapsible panel:
      - Cite UCI dataset: "Hamidieh, K. (2018). A data-driven statistical model for predicting the critical temperature of a superconductor. Computational Materials Science, 154, 346-354."
      - Link to GitHub repo
      - Explain preprocessing: "PCA explained variance: 73.5%; DBSCAN parameters: eps=8, min_samples=50"
      - Open source badge

**Deliverable:** URL state sharing, hypothesis board with export, citation panel

---

## Technical Stack
- **Frontend:** Vanilla JavaScript, Three.js, D3.js (for periodic table)
- **Data processing:** Python (pandas, scikit-learn, umap-learn)
- **AI:** Anthropic Claude API (claude-sonnet-4)
- **Deployment:** Static site (Vercel/GitHub Pages)

## Key Constraints
1. **Keep it static-first:** All features should work without a backend except Claude API calls
2. **Performance:** Maintain sub-second load times, smooth 60fps 3D rendering
3. **Mobile-friendly:** Touch controls for 3D view, responsive layout
4. **Scientific credibility:** Always cite sources, show methodology, avoid exaggeration

## Success Metrics
After implementation, the tool should:
- Load with chemical formulas visible (not anonymous points)
- Allow filtering to "show me all Cu-containing materials with Tc > 77K" in 2 clicks
- Generate AI-powered synthesis rationales on demand
- Support URL-based state sharing for collaboration
- Have a clear visual hierarchy (data → filters → insights → actions)

## Git Workflow
- Create feature branches: `feature/chemical-formulas`, `feature/filtering`, etc.
- Commit frequently with clear messages
- Squash before merging to main
- Tag milestones: `v2.0-data-layer`, `v2.0-filtering`, etc.

## Notes
- Original UCI dataset is at `data/train.csv`
- Current JSON is `docs/data/analysis_results_fast.json`
- Python analysis script is `analyze_data.py`
- All frontend code is in `docs/index.html` (single-file app)
- UMAP is standard in materials informatics — having it ready shows domain competence

## Priority Order (if time-constrained)
1. Chemical formulas (#3) — highest credibility impact
2. Filtering system (#6) — highest utility impact
3. Multi-factor scoring (#9) — highest scientific defensibility
4. AI explainer (#8) — highest "wow factor"
5. UMAP toggle (#7) — signals domain competence
6. Everything else is polish

---

**Start with Week 1, Days 1-2 (data layer). Work systematically through the schedule. Update Reubinator at key milestones.**
