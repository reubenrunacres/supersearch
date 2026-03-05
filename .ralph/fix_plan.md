# SuperSearch Enhancement Plan - Granular Steps

## PRIORITY 1: VISUAL IMPACT (Immediate "Wow")

### 1.1: Bloom Post-Processing
**Step 1.1.1:** Set up EffectComposer
- Import ShaderPass, CopyShader from Three.js examples
- Create composer: `new THREE.EffectComposer(renderer)`
- Add RenderPass as first pass
- Test basic composer renders correctly

**Step 1.1.2:** Add UnrealBloomPass
- Create bloom pass: `new THREE.UnrealBloomPass()`
- Configure parameters: strength=0.8, radius=0.4, threshold=0.85
- Add to composer pipeline
- Verify bloom effect appears

**Step 1.1.3:** Selective Bloom by Tc
- Create separate layers for high-Tc vs low-Tc points
- Apply bloom only to high-Tc layer
- Test performance impact
- Adjust threshold if needed

**Step 1.1.4:** Performance Optimization
- Measure FPS before/after bloom
- Reduce bloom quality if FPS drops below 50
- Add toggle button in UI to disable bloom
- Document performance settings

---

### 1.2: Enhanced Particle Rendering
**Step 1.2.1:** Replace PointsMaterial with Custom Shader
- Create vertex shader for size attenuation
- Create fragment shader for better color/alpha
- Replace existing material with ShaderMaterial
- Verify particles still render

**Step 1.2.2:** Distance-Based Size Scaling
- Calculate distance from camera in vertex shader
- Scale point size: `size = baseSize / distance * scale`
- Test at different zoom levels
- Fine-tune scale factor

**Step 1.2.3:** HDR Color Mapping for High-Tc
- Map Tc to HDR color space (extended range)
- Enhance brightness for Tc > 100K
- Add color saturation boost
- Verify color gradient still readable

**Step 1.2.4:** LOD Implementation
- Create 3 detail levels: high (all points), medium (50%), low (25%)
- Switch based on camera distance/zoom
- Test performance at each level
- Add smooth transitions between LODs

**Step 1.2.5:** Improved Sprite Textures
- Generate better radial gradient sprite
- Add soft edges (Gaussian falloff)
- Test multiple sprite variations
- Pick most visually appealing

---

### 1.3: Composition Family Convex Hulls
**Step 1.3.1:** Calculate Convex Hulls
- Extract points for each cluster (0, 1, 2)
- Use convex hull algorithm (QuickHull or similar)
- Store hull vertices for each family
- Verify hulls contain all cluster points

**Step 1.3.2:** Create Hull Meshes
- Build THREE.Geometry from hull vertices
- Create transparent material (opacity 15%)
- Color-match to family (blue/purple/pink)
- Add to scene

**Step 1.3.3:** Add Wireframe Edges
- Extract edges from hull mesh
- Create LineSegments with same color
- Set line opacity to 30%
- Render both filled + wireframe

**Step 1.3.4:** Breathing Animation
- Add subtle scale animation (0.98 → 1.02)
- Use sine wave for smooth oscillation
- Period: 4 seconds
- Phase offset per family for variety

**Step 1.3.5:** Interactive Highlighting
- Detect hover over hull surface
- Increase opacity on hover (15% → 25%)
- Show family info in tooltip
- Restore opacity on mouse out

---

## PRIORITY 2: SCIENTIFIC INSIGHTS

### 2.1: Annotate Key Materials
**Step 2.1.1:** Identify Top Materials
- Sort materials by Tc (descending)
- Select top 10 highest-Tc materials
- Extract formulas + Tc values
- Store in array for labeling

**Step 2.1.2:** Create Text Sprites
- Use THREE.Sprite for each label
- Render text to canvas, use as texture
- Format: "[Formula]\nTc: [value]K"
- Test text readability

**Step 2.1.3:** Position Labels
- Place near material point (offset +5 units Y)
- Implement label occlusion check
- Adjust position if overlapping
- Connect label to point with line

**Step 2.1.4:** Make Labels Interactive
- Detect click on label
- Highlight all similar materials (same cluster)
- Fade other points to 20% opacity
- Show detail panel with properties

**Step 2.1.5:** Add Known Breakthroughs
- Check for YBaCuO, MgB2, H₃S, etc. in dataset
- Mark with special icon (star/badge)
- Include discovery year if available
- Link to references

---

### 2.2: Opportunity Ranking for Sparse Regions
**Step 2.2.1:** Calculate Proximity Score
- For each sparse region, measure distance to nearest high-Tc cluster
- Closer = higher score (inverse distance)
- Normalize to 0-100 scale
- Store score per region

**Step 2.2.2:** Calculate Density Score
- Count materials within 2-unit radius
- Fewer materials = higher opportunity
- Normalize to 0-100 scale
- Combine with proximity score

**Step 2.2.3:** Calculate Gradient Score
- Sample Tc values around region boundary
- Calculate directional gradient magnitude
- Steeper gradient = higher score
- Weight: 30% proximity, 30% density, 40% gradient

**Step 2.2.4:** Composite Opportunity Score
- Combine 3 sub-scores with weights
- Rank regions 1-34 by total score
- Store ranking in data structure
- Validate scores make intuitive sense

**Step 2.2.5:** Color-Code Sparse Boxes
- Map score to color: green (low) → yellow → red (high)
- Update box materials with new colors
- Add opacity variation (higher score = more visible)
- Update tooltip with score explanation

**Step 2.2.6:** Display Top 5 Regions
- Create UI panel "Top Opportunities"
- List top 5 with scores
- Add "Jump to Region" button per item
- Camera animates to region on click

---

### 2.3: Gradient Visualization
**Step 2.3.1:** Calculate Composition-Space Gradients
- For each sparse region, compute gradient vector
- Direction: toward nearest high-Tc cluster
- Magnitude: proportional to Tc difference
- Store gradient vectors

**Step 2.3.2:** Create Arrow Geometries
- Use THREE.ArrowHelper for each gradient
- Scale arrow by gradient magnitude
- Color: match destination cluster
- Position at region center

**Step 2.3.3:** Add Toggle Control
- Create "Show Gradients" checkbox in UI
- Toggle arrow visibility on/off
- Default: off (can be visually noisy)
- Animate fade in/out (0.5s transition)

**Step 2.3.4:** Interactive Arrow Tooltips
- Hover over arrow shows info
- Display: "Follow gradient to [Cluster Name]"
- Show expected Tc range at destination
- Explain "Discovery Path" concept

---

## PRIORITY 3: CODE QUALITY

### 3.1: Performance Optimization
**Step 3.1.1:** Profile Current Performance
- Open Chrome DevTools Performance tab
- Record 30 seconds of interaction
- Identify bottlenecks (rendering, raycasting, etc.)
- Document baseline FPS

**Step 3.1.2:** Implement Frustum Culling
- Check if point is in camera view frustum
- Skip rendering for off-screen points
- Use THREE.Frustum for checks
- Measure FPS improvement

**Step 3.1.3:** Optimize Raycasting
- Reduce raycaster.params.Points.threshold if too slow
- Implement spatial indexing (octree) for faster lookups
- Only raycast when mouse moves (debounce)
- Cache raycast results for 50ms

**Step 3.1.4:** Use Instanced Rendering
- Replace Points with InstancedMesh if possible
- Batch draw calls for sparse region boxes
- Reduce number of draw calls from ~70 to ~5
- Test compatibility with bloom

**Step 3.1.5:** Lazy-Load Data in Chunks
- If FPS still low, split materials into chunks
- Load/render in batches (5K points at a time)
- Show loading progress
- Stream data over 2-3 seconds

**Step 3.1.6:** Performance Target Validation
- Test on MacBook Pro M1 (target hardware)
- Verify 60fps at all zoom levels
- Test with all features enabled
- Document min/max FPS achieved

---

### 3.2: Code Refactoring
**Step 3.2.1:** Extract DataLoader Module
- Move fetch + data parsing to function
- Create `DataLoader.load()` method
- Return Promise with parsed data
- Handle errors gracefully

**Step 3.2.2:** Extract Renderer Module
- Move scene/camera/renderer setup to class
- Create `Renderer.init()` method
- Encapsulate render loop
- Expose public methods: `start()`, `stop()`, `screenshot()`

**Step 3.2.3:** Extract UIManager Module
- Move all UI creation/updates to class
- Create `UIManager.init()` method
- Handle button clicks, legend interactions
- Emit events for app logic

**Step 3.2.4:** Extract CameraController Module
- Move OrbitControls + presets to class
- Create `CameraController.setView(preset)` method
- Smooth transitions with easing
- Store/restore camera state

**Step 3.2.5:** Add JSDoc Comments
- Document all public functions
- Include @param, @return, @throws tags
- Add usage examples for complex functions
- Generate docs with JSDoc tool

**Step 3.2.6:** Consistent Naming Conventions
- Review all variable names
- Use camelCase consistently
- Prefix private methods with underscore
- Rename ambiguous variables

**Step 3.2.7:** Remove Dead Code
- Search for unused functions
- Remove commented-out code
- Delete old test variables
- Clean up console.log statements

---

### 3.3: Error Handling
**Step 3.3.1:** Graceful Data Load Failure
- Catch fetch errors
- Show user-friendly message: "Could not load data"
- Offer retry button
- Log error details to console

**Step 3.3.2:** WebGL Compatibility Check
- Detect if WebGL is available
- Check for required extensions
- Show fallback message if unsupported
- Link to WebGL troubleshooting

**Step 3.3.3:** Meaningful Error Messages
- Replace generic errors with specific ones
- Include actionable suggestions
- Example: "Camera too close (min: 30)" instead of "Invalid distance"
- User-facing, not developer jargon

**Step 3.3.4:** Improve Loading State
- Show spinner during data fetch
- Display progress percentage
- Update text: "Loading materials... 45%"
- Smooth fade-in when complete

**Step 3.3.5:** Network Retry Logic
- Retry failed fetch 3 times
- Exponential backoff (1s, 2s, 4s)
- Show retry attempt number
- Give up after 3 failures

---

## PRIORITY 4: UX POLISH

### 4.1: Guided Tour Mode
**Step 4.1.1:** Tour Step 1 - Overview
- Camera flies to (80, 60, 80) position
- Show narration: "21,263 superconductors in 3D space"
- Highlight stats panel
- Duration: 3 seconds

**Step 4.1.2:** Tour Step 2 - Composition Families
- Camera transitions to top-down view (0, 100, 0)
- Narration: "3 major composition families identified"
- Pulse convex hulls (if implemented)
- Duration: 4 seconds

**Step 4.1.3:** Tour Step 3 - Sparse Regions
- Camera moves to (50, 30, 50)
- Narration: "34 under-explored regions highlighted"
- Highlight one sparse box with glow
- Duration: 4 seconds

**Step 4.1.4:** Tour Step 4 - High-Tc Materials
- Camera zooms to high-Tc cluster
- Narration: "Materials with Tc > 100K shown in pink"
- Point to labeled material
- Duration: 4 seconds

**Step 4.1.5:** Tour Step 5 - Opportunities
- Camera returns to overview
- Narration: "Opportunity scores guide discovery"
- Show top 5 panel
- Duration: 3 seconds

**Step 4.1.6:** Tour Infrastructure
- Create "Start Tour" button in header
- Implement camera transition animations (easeInOutCubic)
- Pause auto-rotate during tour
- Allow skip/exit at any time

**Step 4.1.7:** Narration Overlays
- Create overlay div for text
- Fade in/out with camera transitions
- Position: bottom-center
- Style: glass-morphism panel

---

### 4.2: Search/Filter Functionality
**Step 4.2.1:** Add Search Box
- Create input field in controls panel
- Placeholder: "Search material formula..."
- Listen for input events
- Debounce to avoid lag

**Step 4.2.2:** Implement Material Search
- Filter materials by formula substring match
- Highlight matching points (full opacity)
- Dim non-matching points (10% opacity)
- Show match count

**Step 4.2.3:** Tc Range Slider
- Add dual-handle slider (min-max range)
- Range: 0K to 185K
- Update filter on slider change
- Show current range in label

**Step 4.2.4:** Element Filter Checkboxes
- Extract unique elements from dataset
- Create checkbox list (Cu, Y, Ba, O, etc.)
- Filter materials containing selected elements
- Combine with other filters (AND logic)

**Step 4.2.5:** Filter Combination Logic
- Apply all filters simultaneously
- Update visible points in real-time
- Show active filter tags
- "Clear Filters" button

**Step 4.2.6:** Display Match Count
- Show "Showing X of 21,263 materials"
- Update dynamically as filters change
- Highlight in stats panel
- Pulse animation when count updates

---

### 4.3: Export Features
**Step 4.3.1:** Screenshot Current View
- Add "📷 Screenshot" button
- Capture canvas at 2x resolution
- Download as PNG
- Filename: `supersearch-[timestamp].png`

**Step 4.3.2:** Export Camera State
- Serialize camera position + target
- Encode as URL query params
- Copy shareable link to clipboard
- Show "Link copied!" toast

**Step 4.3.3:** Restore Camera from URL
- Parse query params on load
- Set camera position/target
- Transition smoothly to saved view
- Handle invalid/missing params

**Step 4.3.4:** Download Filtered Data
- Export currently visible materials as JSON
- Include all properties (Tc, cluster, etc.)
- Offer CSV format option
- Download button in controls panel

**Step 4.3.5:** Share Button UI
- Add "🔗 Share View" button
- Click → copy URL + show toast
- Include all filter states in URL
- Test shareable links work

---

## PRIORITY 5: INTEGRATION STORY

### 5.1: Materials Project Mock Integration
**Step 5.1.1:** Add Placeholder Data Structure
- Define schema for MP predicted materials
- Example: `{ formula, tc_predicted, confidence, ... }`
- Create empty array in code
- Add comment: "// Future: fetch from MP API"

**Step 5.1.2:** Overlay Predicted Materials
- Render predicted materials as different shape (cubes)
- Use semi-transparent color (orange)
- Position based on composition similarity
- Toggle visibility with checkbox

**Step 5.1.3:** Highlight Novel Predictions
- Show predicted materials in unexplored regions
- Use star icon for high-confidence predictions
- Tooltip shows prediction metadata
- "These could be tested next"

**Step 5.1.4:** Mock API Integration Code
- Write commented-out fetch() call
- Show expected API endpoint structure
- Document response format
- Demonstrate understanding of their data

---

### 5.2: Experiment Tracking Visualization
**Step 5.2.1:** Mock "Upload Results" Feature
- Add file upload button (disabled, placeholder)
- Show expected CSV format in tooltip
- Comment: "Future: parse experimental results"
- UI wireframe only

**Step 5.2.2:** Visualize Tested Materials
- Add overlay layer for "tested" materials
- Mark tested points with checkmark icon
- Color by result: green (success), red (fail), yellow (inconclusive)
- Show test date in tooltip

**Step 5.2.3:** Heatmap of Explored Regions
- Calculate exploration density per region
- Render heatmap overlay on grid
- Color: blue (unexplored) → red (heavily explored)
- Toggle with checkbox

**Step 5.2.4:** Time-Lapse Animation Concept
- Add commented code for time-lapse
- Show how materials would appear chronologically
- Slider to scrub through time
- "Replay Discovery History" button (disabled)

---

### 5.3: Documentation for Researchers
**Step 5.3.1:** Create USAGE.md
- Step-by-step guide for scientists
- Screenshot annotations
- Explain each UI element
- Include keyboard shortcuts reference

**Step 5.3.2:** Document PCA Interpretation
- Explain PC1 and PC2 meaning
- What does position in space represent?
- Why 3D instead of 2D?
- Reference papers on PCA for materials

**Step 5.3.3:** Opportunity Scoring Methodology
- Describe algorithm in detail
- Show formula for each sub-score
- Justify weight choices
- Link to similar approaches in literature

**Step 5.3.4:** Add Scientific References
- SuperCon database citation
- PCA/DBSCAN papers
- GNoME paper reference
- Materials Project reference

**Step 5.3.5:** Create VIDEO_SCRIPT.md
- Write narration for 2-minute demo video
- Shot list for screen recording
- Key talking points
- Call-to-action at end

---

## PRIORITY 6: FINAL POLISH

### 6.1: Loading Experience
**Step 6.1.1:** Animated Logo Intro
- Show FlightClaim or Periodic Labs logo (if available)
- Fade in with scale animation
- Hold for 1 second
- Fade out before main viz appears

**Step 6.1.2:** Progress Bar with Milestones
- Show loading bar 0-100%
- Display stages: "Loading data... 30%", "Building scene... 60%", "Rendering... 90%"
- Smooth progress animation
- Transition to viz when complete

**Step 6.1.3:** "Did You Know?" Facts
- Show random fact during load
- Examples: "Highest Tc material: 185K", "34 unexplored regions identified"
- Rotate facts every 2 seconds
- Educational + engaging

**Step 6.1.4:** Smooth Fade-In
- When ready, fade out loading screen
- Fade in visualization
- Duration: 1 second
- Remove loading DOM elements

---

### 6.2: Accessibility
**Step 6.2.1:** Keyboard Navigation
- Arrow keys rotate camera
- +/- keys zoom in/out
- 1-4 keys select camera presets
- Space toggles auto-rotate
- Test all shortcuts work

**Step 6.2.2:** Screen Reader Labels
- Add aria-label to all buttons
- Describe canvas: "3D visualization of superconductors"
- Add aria-live region for status updates
- Test with VoiceOver/NVDA

**Step 6.2.3:** High Contrast Mode
- Add "High Contrast" toggle in settings
- Increase color saturation 50%
- Boost text/UI contrast
- Ensure WCAG AA compliance

**Step 6.2.4:** Reduced Motion Option
- Detect prefers-reduced-motion
- Disable auto-rotate by default
- Instant camera transitions (no easing)
- Remove subtle animations

---

### 6.3: Mobile Optimization
**Step 6.3.1:** Touch Gesture Support
- Implement pinch-to-zoom
- Two-finger swipe to rotate
- One-finger swipe to pan
- Test on iOS Safari

**Step 6.3.2:** Simplified UI for Small Screens
- Collapse panels to tabs/accordion
- Reduce font sizes
- Hide non-essential UI elements
- Maintain core functionality

**Step 6.3.3:** Performance Mode for Mobile
- Detect mobile device
- Reduce particle count to 10K (from 21K)
- Disable bloom on mobile
- Target 30fps minimum

**Step 6.3.4:** Portrait/Landscape Responsive
- Test both orientations
- Adjust UI layout for portrait
- Ensure visualization fills screen
- No horizontal scroll

---

## IMPLEMENTATION ORDER

**Phase 1: Maximum Visual Impact (2-3 hours)**
1. Bloom post-processing (1.1.1 → 1.1.4)
2. Enhanced particles (1.2.1 → 1.2.5)
3. Convex hulls (1.3.1 → 1.3.5)

**Phase 2: Scientific Depth (2 hours)**
4. Annotated materials (2.1.1 → 2.1.5)
5. Opportunity ranking (2.2.1 → 2.2.6)
6. Gradient visualization (2.3.1 → 2.3.4)

**Phase 3: Code Quality (1 hour)**
7. Performance optimization (3.1.1 → 3.1.6)
8. Code refactoring (3.2.1 → 3.2.7)
9. Error handling (3.3.1 → 3.3.5)

**Phase 4: UX & Integration (2 hours)**
10. Guided tour (4.1.1 → 4.1.7)
11. Search/filter (4.2.1 → 4.2.6)
12. Export features (4.3.1 → 4.3.5)
13. Integration story (5.1.1 → 5.3.5)

**Phase 5: Final Polish (1 hour)**
14. Loading experience (6.1.1 → 6.1.4)
15. Accessibility (6.2.1 → 6.2.4)
16. Mobile optimization (6.3.1 → 6.3.4)

**Total: ~8 hours to production quality**

---

## SUCCESS CRITERIA

- [ ] FPS never drops below 50 at any zoom level
- [ ] Page loads in < 3 seconds on fast connection
- [ ] All interactive features respond within 200ms
- [ ] Zero console errors or warnings
- [ ] Works in Chrome, Safari, Firefox
- [ ] Top 3 opportunities visible in first 10 seconds
- [ ] Code is modular, commented, documented
- [ ] Looks impressive on 4K display
- [ ] Mobile-friendly (bonus achievement)

## TESTING CHECKLIST

- [ ] Load time profiled
- [ ] FPS measured at min/max zoom
- [ ] All camera presets tested
- [ ] Tooltips appear correctly
- [ ] Filters work in combination
- [ ] Export features functional
- [ ] Tour mode plays smoothly
- [ ] Keyboard shortcuts work
- [ ] Screen reader accessible
- [ ] Mobile gestures responsive
- [ ] No memory leaks after 10 min use
- [ ] GitHub Pages deployment verified
