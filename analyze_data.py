#!/usr/bin/env python3
"""
SuperSearch Data Analysis v2
Analyzes superconductor datasets to identify composition patterns and under-explored regions.
Outputs enriched JSON with chemical formulas, UMAP coordinates, element composition,
and multi-factor opportunity scoring.
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import json
import re
import subprocess
import sys

# Ensure umap-learn is available
try:
    import umap
except ImportError:
    print("Installing umap-learn...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "umap-learn"])
    import umap

# ---------------------------------------------------------------------------
# 1. Load datasets
# ---------------------------------------------------------------------------
print("Loading datasets...")

uci_data = pd.read_csv('data/train.csv')
print(f"UCI dataset: {len(uci_data)} materials")

# unique_m.csv has the same rows as train.csv but includes chemical formulas
formulas_data = pd.read_csv('data/unique_m.csv')
print(f"Formulas dataset: {len(formulas_data)} materials")

assert len(uci_data) == len(formulas_data), "Row count mismatch between train.csv and unique_m.csv"

# Attach formula and element composition columns to uci_data
uci_data['formula'] = formulas_data['material']

# Extract element symbols present in each formula from unique_m.csv columns
# Columns 0-85 in unique_m.csv are element symbols (H, He, Li, ... Rn)
element_cols = [c for c in formulas_data.columns if c not in ('critical_temp', 'material')]
for col in element_cols:
    formulas_data[col] = pd.to_numeric(formulas_data[col], errors='coerce').fillna(0)

# Build elements list per material (elements with non-zero amounts)
def get_elements(row):
    return [col for col in element_cols if row[col] > 0]

uci_data['elements'] = formulas_data[element_cols].apply(
    lambda row: [col for col in element_cols if row[col] > 0], axis=1
)

# ---------------------------------------------------------------------------
# 2. Filter to superconductors and clean
# ---------------------------------------------------------------------------
uci_superconductors = uci_data[uci_data['critical_temp'] > 0].copy()
print(f"Superconductors in UCI: {len(uci_superconductors)}")

composition_features = [
    'mean_atomic_mass', 'wtd_mean_atomic_mass',
    'mean_atomic_radius', 'wtd_mean_atomic_radius',
    'mean_Valence', 'wtd_mean_Valence',
    'mean_fie', 'wtd_mean_fie',
    'mean_Density', 'wtd_mean_Density'
]

# Keep indices aligned with uci_superconductors
mask = uci_superconductors[composition_features + ['critical_temp']].notna().all(axis=1)
X = uci_superconductors.loc[mask].copy()
print(f"Clean samples for analysis: {len(X)}")

features = X[composition_features]
tc_values = X['critical_temp']

# ---------------------------------------------------------------------------
# 3. Standardize and project
# ---------------------------------------------------------------------------
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# PCA
print("\nPerforming PCA...")
pca = PCA(n_components=2)
coords_pca = pca.fit_transform(features_scaled)
print(f"Explained variance: PC1={pca.explained_variance_ratio_[0]:.2%}, PC2={pca.explained_variance_ratio_[1]:.2%}")

# UMAP (primary projection)
print("Performing UMAP projection...")
umap_reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=42)
coords_umap = umap_reducer.fit_transform(features_scaled)
print(f"UMAP projection complete: {coords_umap.shape}")

# UMAP uncertainty (bootstrap with multiple random seeds)
N_UMAP_RUNS = 10
print(f"Computing UMAP uncertainty ({N_UMAP_RUNS} bootstrap runs)...")
umap_runs = [coords_umap]  # Include the primary run
for seed in range(1, N_UMAP_RUNS):
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=seed * 7 + 13)
    run_coords = reducer.fit_transform(features_scaled)
    # Align to primary projection using Procrustes-like alignment (translation + rotation)
    # Simple approach: align centroids and scale
    run_centered = run_coords - run_coords.mean(axis=0)
    primary_centered = coords_umap - coords_umap.mean(axis=0)
    # Procrustes: find optimal rotation via SVD
    H = run_centered.T @ primary_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    aligned = run_centered @ R.T + coords_umap.mean(axis=0)
    umap_runs.append(aligned)
    print(f"  UMAP run {seed + 1}/{N_UMAP_RUNS} done")

umap_stack = np.stack(umap_runs, axis=0)  # (N_UMAP_RUNS, n_materials, 2)
umap_std = np.std(umap_stack, axis=0)  # (n_materials, 2)
umap_uncertainty = np.sqrt(umap_std[:, 0]**2 + umap_std[:, 1]**2)  # Combined uncertainty
print(f"UMAP uncertainty range: {umap_uncertainty.min():.4f} — {umap_uncertainty.max():.4f}")

# ---------------------------------------------------------------------------
# 4. Clustering
# ---------------------------------------------------------------------------
print("\nClustering composition families...")
clustering = DBSCAN(eps=0.5, min_samples=10)
clusters = clustering.fit_predict(coords_pca)

n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
n_noise = list(clusters).count(-1)
print(f"Found {n_clusters} composition families ({n_noise} outliers)")

# ---------------------------------------------------------------------------
# 5. Format chemical formulas with Unicode subscripts
# ---------------------------------------------------------------------------
SUBSCRIPT_MAP = str.maketrans('0123456789.', '₀₁₂₃₄₅₆₇₈₉.')

def format_formula(raw):
    """Convert 'Ba0.2La1.8Cu1O4' → 'Ba₀.₂La₁.₈CuO₄' (drop subscript 1)."""
    if not isinstance(raw, str):
        return "Unknown"
    # Replace element-1 patterns (exact 1, not 1.x or 10+)
    formatted = re.sub(r'(?<=[A-Za-z])1(?=[A-Z]|$)', '', raw)
    # Apply subscript mapping to digits and dots that follow element symbols
    result = []
    i = 0
    while i < len(formatted):
        ch = formatted[i]
        if ch.isdigit() or (ch == '.' and i > 0 and (formatted[i-1].isdigit() or formatted[i-1].translate(SUBSCRIPT_MAP) != formatted[i-1])):
            result.append(ch.translate(SUBSCRIPT_MAP))
        else:
            result.append(ch)
        i += 1
    return result if not result else ''.join(result)

# ---------------------------------------------------------------------------
# 6. Build material records
# ---------------------------------------------------------------------------
print("\nBuilding material records...")

output_data = []
for i in range(len(coords_pca)):
    row = X.iloc[i]
    output_data.append({
        'x': round(float(coords_pca[i, 0]), 4),
        'y': round(float(coords_pca[i, 1]), 4),
        'tc': round(float(tc_values.iloc[i]), 3),
        'cluster': int(clusters[i]),
        'atomic_mass': round(float(row['mean_atomic_mass']), 2),
        'atomic_radius': round(float(row['mean_atomic_radius']), 2),
        'valence': round(float(row['mean_Valence']), 2),
        'density': round(float(row['mean_Density']), 2),
        'formula': format_formula(row.get('formula', '')),
        'formula_raw': str(row.get('formula', '')),
        'elements': row.get('elements', []),
        'umap_x': round(float(coords_umap[i, 0]), 4),
        'umap_y': round(float(coords_umap[i, 1]), 4),
        'umap_uncertainty': round(float(umap_uncertainty[i]), 4),
    })

print(f"Built {len(output_data)} material records")

# ---------------------------------------------------------------------------
# 7. Multi-factor opportunity region scoring
# ---------------------------------------------------------------------------
print("\nIdentifying under-explored regions with multi-factor scoring...")

# Grid-based density calculation
grid_size = 20
x_bins = np.linspace(coords_pca[:, 0].min(), coords_pca[:, 0].max(), grid_size)
y_bins = np.linspace(coords_pca[:, 1].min(), coords_pca[:, 1].max(), grid_size)

density_map = np.zeros((grid_size - 1, grid_size - 1))
for point in coords_pca:
    x_idx = np.searchsorted(x_bins, point[0]) - 1
    y_idx = np.searchsorted(y_bins, point[1]) - 1
    if 0 <= x_idx < grid_size - 1 and 0 <= y_idx < grid_size - 1:
        density_map[x_idx, y_idx] += 1

# Nearest neighbors model for proximity scoring
nn_model = NearestNeighbors(n_neighbors=10, metric='euclidean')
nn_model.fit(coords_pca)

# Cluster assignments for novelty scoring
cluster_arr = np.array(clusters)
tc_arr = np.array(tc_values)

threshold = np.percentile(density_map[density_map > 0], 25)
max_density = density_map.max()

sparse_regions = []
for i in range(grid_size - 1):
    for j in range(grid_size - 1):
        if 0 < density_map[i, j] < threshold:
            x_center = (x_bins[i] + x_bins[i + 1]) / 2
            y_center = (y_bins[j] + y_bins[j + 1]) / 2
            center = np.array([[x_center, y_center]])

            # --- Sparseness score (40%) ---
            # Lower density = higher score (inverse normalized)
            sparseness = 1.0 - (density_map[i, j] / max_density) if max_density > 0 else 0.5

            # --- Proximity to high-Tc (30%) ---
            distances, indices = nn_model.kneighbors(center)
            neighbor_tcs = tc_arr[indices[0]]
            avg_neighbor_tc = float(np.mean(neighbor_tcs))
            max_tc = float(tc_arr.max())
            tc_proximity = avg_neighbor_tc / max_tc if max_tc > 0 else 0

            # --- Compositional novelty (20%) ---
            neighbor_clusters = cluster_arr[indices[0]]
            unique_clusters = len(set(neighbor_clusters))
            total_possible = max(n_clusters + 1, 1)  # +1 for noise cluster
            novelty = unique_clusters / total_possible

            # --- Synthesis feasibility (10%) ---
            # Penalize extreme atomic radius mismatches in neighbors
            neighbor_indices = indices[0]
            radii = np.array([float(X.iloc[idx]['mean_atomic_radius']) for idx in neighbor_indices])
            radius_cv = np.std(radii) / np.mean(radii) if np.mean(radii) > 0 else 1.0
            feasibility = max(0, 1.0 - radius_cv)

            # Composite score
            score = (
                0.40 * sparseness +
                0.30 * tc_proximity +
                0.20 * novelty +
                0.10 * feasibility
            )

            # Nearest neighbor details for the region card
            nn_materials = []
            for idx in indices[0][:5]:
                nn_materials.append({
                    'formula': format_formula(X.iloc[idx].get('formula', '')),
                    'tc': round(float(tc_arr[idx]), 1),
                })

            # --- Bootstrap 95% CI on avg neighbor Tc ---
            n_bootstrap = 1000
            bootstrap_means = []
            rng_bs = np.random.RandomState(42 + i * 100 + j)
            for _ in range(n_bootstrap):
                sample = rng_bs.choice(neighbor_tcs, size=len(neighbor_tcs), replace=True)
                bootstrap_means.append(float(np.mean(sample)))
            ci_low = round(float(np.percentile(bootstrap_means, 2.5)), 1)
            ci_high = round(float(np.percentile(bootstrap_means, 97.5)), 1)
            ci_width = ci_high - ci_low

            # Confidence level based on material count and CI width
            n_nearby = int(density_map[i, j])
            if n_nearby >= 5 and ci_width < 30:
                confidence = 'high'
            elif n_nearby >= 3 and ci_width < 60:
                confidence = 'medium'
            else:
                confidence = 'low'

            sparse_regions.append({
                'x': round(float(x_center), 4),
                'y': round(float(y_center), 4),
                'density': n_nearby,
                'score': round(float(score * 10), 1),  # Scale to 0-10
                'score_breakdown': {
                    'sparseness': round(float(sparseness * 100), 1),
                    'tc_proximity': round(float(tc_proximity * 100), 1),
                    'novelty': round(float(novelty * 100), 1),
                    'feasibility': round(float(feasibility * 100), 1),
                },
                'avg_neighbor_tc': round(avg_neighbor_tc, 1),
                'tc_ci_low': ci_low,
                'tc_ci_high': ci_high,
                'confidence': confidence,
                'nearest_materials': nn_materials,
            })

# Sort by score (highest first)
sparse_regions.sort(key=lambda r: r['score'], reverse=True)
print(f"Identified {len(sparse_regions)} under-explored regions (scored)")

# ---------------------------------------------------------------------------
# 8. Sample for fast loading
# ---------------------------------------------------------------------------
FAST_SAMPLE_SIZE = 5000

if len(output_data) > FAST_SAMPLE_SIZE:
    rng = np.random.RandomState(42)
    indices_sample = rng.choice(len(output_data), FAST_SAMPLE_SIZE, replace=False)
    indices_sample.sort()
    fast_data = [output_data[i] for i in indices_sample]
else:
    fast_data = output_data

# ---------------------------------------------------------------------------
# 9. Build element frequency stats for periodic table heatmap
# ---------------------------------------------------------------------------
print("Computing element frequency statistics...")

# Count how often each element appears in materials with Tc > 77K (liquid nitrogen)
high_tc_mask = X['critical_temp'] > 77
all_elements_list = X['elements'].tolist()
high_tc_elements_list = X.loc[high_tc_mask, 'elements'].tolist()

element_stats = {}
for elem in element_cols:
    total_count = sum(1 for elems in all_elements_list if elem in elems)
    high_tc_count = sum(1 for elems in high_tc_elements_list if elem in elems)
    if total_count > 0:
        # Average Tc for materials containing this element
        elem_mask = X['elements'].apply(lambda e: elem in e)
        avg_tc = float(X.loc[elem_mask, 'critical_temp'].mean())

        # Find common co-occurring elements
        co_elements = {}
        for elems in X.loc[elem_mask, 'elements']:
            for co in elems:
                if co != elem:
                    co_elements[co] = co_elements.get(co, 0) + 1
        top_co = sorted(co_elements.items(), key=lambda x: x[1], reverse=True)[:5]

        element_stats[elem] = {
            'count': total_count,
            'high_tc_count': high_tc_count,
            'avg_tc': round(avg_tc, 1),
            'top_co_elements': [{'element': e, 'count': c} for e, c in top_co],
        }

print(f"Element stats computed for {len(element_stats)} elements")

# ---------------------------------------------------------------------------
# 10. Save results
# ---------------------------------------------------------------------------
print("\nSaving results...")

metadata = {
    'total_materials': len(output_data),
    'displayed_materials': len(fast_data),
    'n_clusters': n_clusters,
    'pca_variance': {
        'pc1': round(float(pca.explained_variance_ratio_[0]), 4),
        'pc2': round(float(pca.explained_variance_ratio_[1]), 4),
    },
    'tc_range': {
        'min': round(float(tc_values.min()), 5),
        'max': round(float(tc_values.max()), 1),
        'mean': round(float(tc_values.mean()), 2),
    },
    'note': 'SuperSearch v3 — enriched with formulas, UMAP + uncertainty, element data, multi-factor scoring with CIs',
}

# Full results
full_results = {
    'materials': output_data,
    'sparse_regions': sparse_regions,
    'element_stats': element_stats,
    'metadata': {**metadata, 'displayed_materials': len(output_data)},
}
with open('data/analysis_results.json', 'w') as f:
    json.dump(full_results, f)
print(f"  ✓ Full results: data/analysis_results.json ({len(output_data)} materials)")

# Fast-loading version
fast_results = {
    'materials': fast_data,
    'sparse_regions': sparse_regions,
    'element_stats': element_stats,
    'metadata': metadata,
}
with open('docs/data/analysis_results_fast.json', 'w') as f:
    json.dump(fast_results, f)
print(f"  ✓ Fast results: docs/data/analysis_results_fast.json ({len(fast_data)} materials)")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SuperSearch v2 Analysis Complete!")
print("=" * 60)
print(f"  Materials:      {len(output_data)} total, {len(fast_data)} in fast sample")
print(f"  Clusters:       {n_clusters} families + {n_noise} outliers")
print(f"  Sparse regions: {len(sparse_regions)} scored opportunities")
print(f"  Elements:       {len(element_stats)} with frequency stats")
print(f"  Tc range:       {metadata['tc_range']['min']}K → {metadata['tc_range']['max']}K (avg {metadata['tc_range']['mean']}K)")
print(f"  PCA variance:   {metadata['pca_variance']['pc1']:.1%} + {metadata['pca_variance']['pc2']:.1%}")
print(f"\n  Fields per material:  formula, formula_raw, elements, umap_x, umap_y, density, umap_uncertainty")
print(f"  Fields per region:   score, score_breakdown, avg_neighbor_tc, tc_ci_low, tc_ci_high, confidence")
print(f"  Top-level:           element_stats (periodic table heatmap data)")
