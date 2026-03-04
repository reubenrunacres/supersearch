#!/usr/bin/env python3
"""
SuperSearch Data Analysis
Analyzes superconductor datasets to identify composition patterns and under-explored regions
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import json

print("Loading datasets...")

# Load UCI dataset
uci_data = pd.read_csv('data/train.csv')
print(f"UCI dataset: {len(uci_data)} materials")

# Load 3DSC dataset
dsc_data = pd.read_csv('data/3DSC_MP.csv', comment='#')
print(f"3DSC dataset: {len(dsc_data)} materials")

# Focus on materials with Tc > 0 (actual superconductors)
uci_superconductors = uci_data[uci_data['critical_temp'] > 0].copy()
print(f"Superconductors in UCI: {len(uci_superconductors)}")

# Get key features for composition analysis
# Using elemental statistics: atomic mass, radius, valence, etc.
composition_features = [
    'mean_atomic_mass', 'wtd_mean_atomic_mass',
    'mean_atomic_radius', 'wtd_mean_atomic_radius', 
    'mean_Valence', 'wtd_mean_Valence',
    'mean_fie', 'wtd_mean_fie',
    'mean_Density', 'wtd_mean_Density'
]

# Filter to only rows with complete data
X = uci_superconductors[composition_features + ['critical_temp']].dropna()
print(f"Clean samples for analysis: {len(X)}")

# Separate features and target
features = X[composition_features]
tc_values = X['critical_temp']

# Standardize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# PCA to 2D for visualization
print("\nPerforming PCA...")
pca = PCA(n_components=2)
coords_2d = pca.fit_transform(features_scaled)

print(f"Explained variance: PC1={pca.explained_variance_ratio_[0]:.2%}, PC2={pca.explained_variance_ratio_[1]:.2%}")

# Clustering to identify composition families
print("\nClustering composition families...")
clustering = DBSCAN(eps=0.5, min_samples=10)
clusters = clustering.fit_predict(coords_2d)

n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
n_noise = list(clusters).count(-1)
print(f"Found {n_clusters} composition families ({n_noise} outliers)")

# Create output data
output_data = []
for i in range(len(coords_2d)):
    output_data.append({
        'x': float(coords_2d[i, 0]),
        'y': float(coords_2d[i, 1]),
        'tc': float(tc_values.iloc[i]),
        'cluster': int(clusters[i]),
        # Store original feature values for tooltip
        'atomic_mass': float(X.iloc[i]['mean_atomic_mass']),
        'atomic_radius': float(X.iloc[i]['mean_atomic_radius']),
        'valence': float(X.iloc[i]['mean_Valence'])
    })

# Identify sparse regions (potential opportunities)
print("\nIdentifying under-explored regions...")

# Grid-based density calculation
x_bins = np.linspace(coords_2d[:, 0].min(), coords_2d[:, 0].max(), 20)
y_bins = np.linspace(coords_2d[:, 1].min(), coords_2d[:, 1].max(), 20)

density_map = np.zeros((len(x_bins)-1, len(y_bins)-1))
for point in coords_2d:
    x_idx = np.searchsorted(x_bins, point[0]) - 1
    y_idx = np.searchsorted(y_bins, point[1]) - 1
    if 0 <= x_idx < len(x_bins)-1 and 0 <= y_idx < len(y_bins)-1:
        density_map[x_idx, y_idx] += 1

# Find low-density regions adjacent to high-Tc clusters
sparse_regions = []
threshold = np.percentile(density_map[density_map > 0], 25)  # Bottom quartile
for i in range(len(x_bins)-1):
    for j in range(len(y_bins)-1):
        if 0 < density_map[i, j] < threshold:
            x_center = (x_bins[i] + x_bins[i+1]) / 2
            y_center = (y_bins[j] + y_bins[j+1]) / 2
            sparse_regions.append({
                'x': float(x_center),
                'y': float(y_center),
                'density': int(density_map[i, j])
            })

print(f"Identified {len(sparse_regions)} under-explored regions")

# Save analysis results
print("\nSaving results...")
results = {
    'materials': output_data,
    'sparse_regions': sparse_regions,
    'metadata': {
        'total_materials': len(output_data),
        'n_clusters': n_clusters,
        'pca_variance': {
            'pc1': float(pca.explained_variance_ratio_[0]),
            'pc2': float(pca.explained_variance_ratio_[1])
        },
        'tc_range': {
            'min': float(tc_values.min()),
            'max': float(tc_values.max()),
            'mean': float(tc_values.mean())
        }
    }
}

with open('data/analysis_results.json', 'w') as f:
    json.dump(results, f)

print("✓ Analysis complete!")
print(f"  - {len(output_data)} materials mapped to 2D composition space")
print(f"  - {n_clusters} composition families identified")
print(f"  - {len(sparse_regions)} under-explored regions found")
print(f"  - Tc range: {results['metadata']['tc_range']['min']:.1f}K to {results['metadata']['tc_range']['max']:.1f}K")
