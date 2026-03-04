# SuperSearch - Superconductor Composition Explorer

**Interactive visualization tool mapping 21,000+ known superconductors to identify under-explored regions that could yield novel high-Tc materials.**

Built for [Periodic Labs](https://periodic.com) to demonstrate understanding of their superconductor discovery mission and ability to build production-quality research tools.

![SuperSearch Preview](docs/preview.png) _(coming soon)_

---

## 🎯 The Problem

With 21,000+ known superconductors documented in literature, researchers face a challenge:

- **Where have experimental efforts been concentrated?**
- **Which composition spaces remain under-explored?**
- **Where are the most promising "white spaces" for discovery?**

Manual analysis of this landscape is time-consuming and doesn't scale.

## 💡 The Solution

SuperSearch uses machine learning to:

1. **Map the landscape** - PCA reduces 81 compositional features to 2D space (73.55% variance retained)
2. **Identify families** - DBSCAN clustering reveals 3 major composition families
3. **Find opportunities** - Grid-based density analysis highlights 34 under-explored regions
4. **Enable exploration** - Interactive D3.js visualization with hover tooltips and Tc color-coding

## 🔬 Key Insights

From analysis of the UCI Superconductivity Database:

- **21,263 materials** mapped to composition space
- **3 composition families** identified via clustering
- **34 under-explored regions** found adjacent to high-Tc clusters
- **Tc range:** 0-185K in dataset (avg: 34.4K)
- **High-Tc materials:** 5,872 with Tc > 50K (28%), 1,423 with Tc > 100K (7%)

## 🚀 Why This Matters for Periodic Labs

Your mission is accelerating superconductor discovery through AI-driven autonomous experimentation. SuperSearch complements this by:

### 1. Research Leverage
Visualizes the experimental landscape to show where efforts have been sparse vs. concentrated.

### 2. Hypothesis Generation
Sparse regions adjacent to high-Tc clusters = concrete targets for your autonomous lab to screen systematically.

### 3. Strategic Planning
Shows composition families worth exploring with your Materials Project integration and GNoME predictions.

### 4. Progress Tracking
Could integrate with your experimental results to visualize how your lab fills in white spaces over time.

## 🛠️ Technical Stack

- **Data:** UCI Superconductivity Database (21K materials, 81 features)
- **Analysis:** Python (pandas, scikit-learn) - PCA, DBSCAN clustering, density analysis
- **Visualization:** Vanilla JavaScript + D3.js (no framework bloat)
- **Design:** Modern dark UI inspired by materials science research tools

## 📂 Project Structure

```
supersearch/
├── data/
│   ├── train.csv              # UCI dataset (21K materials)
│   ├── analysis_results.json  # Processed data for viz
│   └── ...
├── web/
│   └── index.html            # Standalone visualization
├── analyze_data.py           # PCA + clustering + density analysis
├── README.md                 # This file
└── FOR_PERIODIC_LABS.md      # Detailed pitch document
```

## 🎮 Running Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/supersearch.git
cd supersearch

# Serve the visualization
cd web
python3 -m http.server 8000

# Open http://localhost:8000 in your browser
```

## 📊 Regenerate Analysis (Optional)

If you want to modify the analysis:

```bash
# Install dependencies
pip install pandas scikit-learn numpy

# Run analysis
python analyze_data.py

# Output: data/analysis_results.json
```

## 🎨 Visualization Features

- **Color gradient:** Tc encoded as blue → purple → pink (0K → 185K)
- **Interactive tooltips:** Hover to see material formula, Tc, cluster assignment
- **Highlighted regions:** 34 under-explored zones shown with boundary boxes
- **Zoom & pan:** Standard D3 controls for exploration
- **Responsive design:** Works on desktop and tablet

## 🔮 Possible Extensions

If useful for your research, could be extended to:

1. **Integrate Materials Project data** - Overlay your predicted/synthesized materials
2. **Real-time experiment tracking** - Show where your autonomous lab has tested
3. **Filtering & search** - By crystal structure, synthesis feasibility, elements
4. **Gradient-based prioritization** - Rank sparse regions by predicted property gradients
5. **Historical tracking** - Animate how composition space has been explored over decades

## 📈 Build Details

- **Time:** ~8 hours from concept to production-ready
- **Lines of code:** ~400 Python (analysis) + ~600 JavaScript (viz)
- **Deployment:** Static site (no backend needed) - ready for GitHub Pages/Vercel

## 🤝 Why I Built This

I'm deeply interested in Periodic Labs' mission to accelerate scientific discovery through AI + autonomous experimentation. After researching your work (the GNoME paper, autonomous robotic labs), I wanted to demonstrate:

1. **Domain understanding** - I get what you're building and why it matters
2. **Technical execution** - I can ship production-quality research tools quickly
3. **Product sense** - Focus on what's immediately useful vs. just technically impressive
4. **Rapid iteration** - Concept to working demo in hours, not weeks

## 📬 Contact

Built as part of application to Periodic Labs.

**[Your Name]**  
Email: [your email]  
GitHub: [your github]  
LinkedIn: [your linkedin]

---

## 📄 License

MIT License - Free to use, modify, and distribute.

## 🙏 Acknowledgments

- UCI Machine Learning Repository for the Superconductivity Database
- D3.js community for excellent documentation
- Periodic Labs for inspiring this project

---

**Looking forward to discussing how this type of analysis could complement your internal tools and contribute to your superconductor research mission.**
