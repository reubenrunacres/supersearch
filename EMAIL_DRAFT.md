# Email Draft: Periodic Labs Grant Program

---

**Subject:** SuperSearch: Composition Space Visualization for Superconductor Discovery

---

**To:** grants@periodic.com

**Body:**

Hi Periodic Labs team,

I'm reaching out regarding your academic grant program. I've built a tool that might complement your superconductor discovery mission, and I'd love to discuss potential collaboration.

**What I Built:**

SuperSearch is an interactive visualization that maps 21,000+ known superconductors in composition space and identifies 34 under-explored regions that could be strategic targets for autonomous lab screening.

**Live Demo:** https://reubenrunacres.github.io/supersearch/  
**GitHub:** https://github.com/reubenrunacres/supersearch

**Why This Might Be Useful:**

Your work (especially the GNoME paper and autonomous robotic labs) focuses on accelerating materials discovery through AI-driven experimentation. SuperSearch could help:

1. **Visualize the landscape** - See where experimental efforts have been concentrated vs. sparse
2. **Prioritize GNoME candidates** - Show which predicted materials fall into under-explored regions
3. **Track progress** - Visualize how your autonomous lab fills composition space over time
4. **Generate hypotheses** - 3 identified families + 34 sparse regions = concrete experimental targets

**Key Results:**
- 21,263 materials mapped (UCI database)
- 73.55% variance retained in 2D projection (PCA)
- 3 composition families identified (DBSCAN)
- 34 under-explored regions highlighted
- Interactive D3.js visualization with Tc color-coding

**Technical Approach:**

I used PCA for dimensionality reduction (interpretable, stable), DBSCAN for clustering (discovers families automatically), and grid-based density analysis to find sparse regions. The tool is built with vanilla JavaScript + D3.js, so it's fast, extensible, and easy to fork.

**Build Details:**
- Time: 8 hours from concept to deployed tool
- Stack: Python (scikit-learn) + D3.js
- License: MIT (open source)
- No proprietary dependencies

**Why I'm Reaching Out:**

I'm fascinated by your mission to give AI systems the ability to run real experiments and learn from physical reality. After reading about your autonomous labs and GNoME work, I wanted to build something that demonstrates:

1. Domain understanding (superconductors, Materials Project, composition space)
2. Rapid execution (production quality in hours)
3. Product thinking (immediately useful vs. academically interesting)

**Potential Collaboration:**

If SuperSearch is useful for your research, I'd be interested in:

1. **Using it as-is** - Free tool, MIT license, no strings attached
2. **Integration work** - Overlay Materials Project data, add live experiment tracking, build predictive models
3. **Grant program** - Formal research collaboration on superconductor discovery tools
4. **Internship opportunities** - Contributing to your mission alongside your team

I've prepared detailed documentation:
- **One-page summary:** https://github.com/reubenrunacres/supersearch/blob/main/SUMMARY.md
- **Full pitch with integration roadmap:** https://github.com/reubenrunacres/supersearch/blob/main/FOR_PERIODIC_LABS.md

**Next Steps:**

I'd love to discuss:
- Whether this type of analysis complements your internal tools
- Other ways I could contribute to your superconductor research
- Opportunities through your grant program or team

Please let me know if you'd like to schedule a call, or if there's someone else on your team I should connect with.

Thank you for building something this ambitious. The world needs more people tackling hard, important problems with novel approaches.

Best regards,  
Reuben Runacres

**Contact:**  
Email: [your email]  
GitHub: reubenrunacres  
LinkedIn: [your LinkedIn]  
Website: [optional]

---

**Attachments:**
- Link to live demo
- Link to GitHub repository
- Link to one-page summary

---

## Alternative: Shorter Version

**Subject:** Tool for Superconductor Composition Space Exploration

Hi Periodic Labs,

I built an interactive visualization (SuperSearch) that maps 21K+ superconductors and identifies 34 under-explored regions for experimental targeting. Thought it might complement your GNoME work and autonomous lab mission.

**Live demo:** https://reubenrunacres.github.io/supersearch/  
**Full details:** https://github.com/reubenrunacres/supersearch

Key results: 3 composition families identified, 34 sparse regions found, built in 8 hours, MIT licensed.

Would love to discuss potential collaboration through your grant program or otherwise. Let me know if you'd like to chat.

Best,  
Reuben Runacres  
[contact info]

---

## Notes for Sending

**Timing:**
- Best sent Tuesday-Thursday, 9am-11am PT (their timezone likely California)
- Avoid Mondays (catching up) and Fridays (winding down)

**Follow-up:**
- If no response in 5-7 days, send gentle follow-up
- Reference the tool briefly, ask if they had a chance to review

**Tone:**
- Professional but not stiff
- Show domain expertise without being arrogant
- Focus on their mission, not your credentials
- Concrete value proposition, not vague "I want to help"

**Alternative Recipients:**
- grants@periodic.com (primary)
- careers@periodic.com (if considering internship)
- Liam Fedus (CEO) on LinkedIn (if can get intro)
- Ekin Dogus Cubuk (Co-founder) - materials science expert

**Research First:**
- Check if they've posted about open collaboration
- See if any team members are active on Twitter/LinkedIn
- Look for recent papers/posts mentioning their tools
- Find any mutual connections for warm intro
