# SuperSearch: Superconductor Composition Explorer
## One-Page Summary for Periodic Labs

---

### The Tool
**Interactive visualization mapping 21,000+ known superconductors to identify under-explored composition regions for experimental targeting.**

**Live Demo:** https://reubenrunacres.github.io/supersearch/  
**GitHub:** https://github.com/reubenrunacres/supersearch

---

### The Problem You're Solving
Periodic Labs is building AI scientists + autonomous labs to accelerate superconductor discovery. But with thousands of known materials scattered across literature, **where should an autonomous lab focus its experimental efforts?**

### What SuperSearch Provides
1. **Visual landscape** - See the entire composition space at a glance (PCA → 2D)
2. **Composition families** - 3 major clusters identified via DBSCAN
3. **Concrete targets** - 34 under-explored regions adjacent to high-Tc materials
4. **Interactive exploration** - Hover, zoom, filter by Tc range

---

### Key Results
From UCI Superconductivity Database analysis:
- **21,263 materials** mapped to composition space
- **73.55% variance** retained in 2D projection (PCA)
- **3 composition families** identified
- **34 sparse regions** found (potential discovery opportunities)
- **Tc range:** 0-185K (5,872 materials > 50K, 1,423 > 100K)

---

### Why This Matters for Your Mission

**1. Complements GNoME Work**
- Your Nature paper predicted 2.2M stable materials
- SuperSearch shows which fall into under-explored composition space
- Prioritize GNoME candidates that fill white spaces

**2. Strategic Lab Targets**
- 34 concrete regions for autonomous lab to screen
- Not random - adjacent to known superconductors
- Under-represented = less prior experimental effort

**3. Progress Tracking**
- Visualize how your lab fills composition space over time
- See where unexpected results cluster
- Guide hypothesis generation for next experiments

**4. Integration Ready**
- Materials Project overlay: 1 day
- Live experiment tracking: 1 week
- Predictive prioritization: 2-3 weeks

---

### Technical Stack
- **Data:** UCI database (21K materials, 81 features)
- **Analysis:** Python + scikit-learn (PCA, DBSCAN, density analysis)
- **Visualization:** D3.js + vanilla JavaScript
- **Deployment:** GitHub Pages (static site, no backend)
- **Build time:** 8 hours concept → production

---

### What Makes It Useful
Unlike academic visualization papers:
- ✅ **Interactive** - Not static plots
- ✅ **Fast** - No framework bloat, instant load
- ✅ **Actionable** - 34 regions = concrete targets
- ✅ **Extensible** - Easy to integrate your data

---

### Proposed Collaboration

**Phase 1: Use As-Is (Now)**
- Internal tool for hypothesis generation
- Share with researchers
- Reference in papers/grants

**Phase 2: Data Integration (1-2 days)**
- Overlay Materials Project predictions
- Filter by synthesis feasibility
- Show GNoME candidates in sparse regions

**Phase 3: Live Tracking (1 week)**
- Connect to autonomous lab results
- Real-time updates as experiments complete
- Visualize success/failure patterns

**Phase 4: Predictive Loop (2-3 weeks)**
- ML model to rank regions by gradients
- Active learning: results → model → new targets
- Close the simulation ↔ experiment loop

---

### About Me
Built this in 8 hours to demonstrate:
1. **Domain understanding** - I get superconductors, GNoME, Materials Project
2. **Rapid execution** - Production quality in hours, not months
3. **Product thinking** - Immediately useful vs. academically interesting
4. **System design** - Clean architecture, extensible, well-documented

**I'm interested in contributing to your mission** - whether through your grant program, internship opportunities, or other collaboration.

---

### Contact & Links
**Live Demo:** https://reubenrunacres.github.io/supersearch/  
**Repository:** https://github.com/reubenrunacres/supersearch  
**Full Pitch:** [FOR_PERIODIC_LABS.md](FOR_PERIODIC_LABS.md)

**Reuben Runacres**  
Email: [To be added]  
GitHub: reubenrunacres  
LinkedIn: [To be added]

---

### Quick Stats
| Metric | Value |
|--------|-------|
| Materials Analyzed | 21,263 |
| Composition Features | 81 |
| Families Identified | 3 |
| Sparse Regions | 34 |
| Tc Range | 0-185K |
| High-Tc Materials (>50K) | 5,872 (28%) |
| Build Time | 8 hours |
| Lines of Code | ~1,000 |
| License | MIT (open source) |

---

*"Technological progress is limited by our ability to design the physical world."* - Periodic Labs

**SuperSearch helps you find where to look next.**
