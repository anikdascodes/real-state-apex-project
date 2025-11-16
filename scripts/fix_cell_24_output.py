#!/usr/bin/env python3
"""
Fix Cell 24 - Execute summary statistics cell and update notebook with output
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from io import StringIO
import sys

# Load the notebook
notebook_path = Path('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb')
with open(notebook_path, 'r') as f:
    notebook = json.load(f)

# Load the data (same way as in the notebook)
df = pd.read_csv('data/AmesHousing.csv')

print("Executing Cell 24 - Summary Statistics...")
print("="*80)

# Capture the output of Cell 24
output_buffer = StringIO()
sys.stdout = output_buffer

# Execute the exact code from Cell 24
print("="*70)
print("SUMMARY STATISTICS - NUMERICAL FEATURES")
print("="*70)
print("\nDescriptive Statistics for All Numerical Features:")
print(df.describe())

print("\n" + "="*70)
print("SUMMARY STATISTICS - TARGET VARIABLE (SalePrice)")
print("="*70)
target_stats = df['SalePrice'].describe()
print(target_stats)
print(f"\nPrice Range: ${df['SalePrice'].min():,.0f} to ${df['SalePrice'].max():,.0f}")
print(f"Price Spread (IQR): ${target_stats['75%'] - target_stats['25%']:,.0f}")

# Key insights from statistics
print("\n" + "="*70)
print("KEY STATISTICAL INSIGHTS")
print("="*70)
print(f"1. SalePrice Distribution:")
print(f"   - Mean: ${df['SalePrice'].mean():,.0f}")
print(f"   - Median: ${df['SalePrice'].median():,.0f}")
print(f"   - Shows {'right' if df['SalePrice'].mean() > df['SalePrice'].median() else 'left'}-skewed distribution")
print(f"\n2. Living Area Variability:")
print(f"   - Range: {df['Gr Liv Area'].min():.0f} to {df['Gr Liv Area'].max():.0f} sq ft")
print(f"   - Coefficient of Variation: {(df['Gr Liv Area'].std()/df['Gr Liv Area'].mean())*100:.1f}%")
print(f"\n3. Age Distribution:")
print(f"   - Newest: {df['Year Built'].max()}")
print(f"   - Oldest: {df['Year Built'].min()}")
print(f"   - Span: {df['Year Built'].max() - df['Year Built'].min()} years")
print("\n✓ Statistical foundation established for analysis")

# Get the captured output
sys.stdout = sys.__stdout__
output_text = output_buffer.getvalue()

print(output_text)
print()
print("="*80)
print("Updating notebook with Cell 24 output...")

# Update Cell 24 (index 23) with the output
cell_24 = notebook['cells'][23]
cell_24['outputs'] = [
    {
        'output_type': 'stream',
        'name': 'stdout',
        'text': output_text.split('\n')  # Convert to list of lines
    }
]
cell_24['execution_count'] = 24

# Save the updated notebook
with open(notebook_path, 'w') as f:
    json.dump(notebook, f, indent=2)

print("✅ Cell 24 output successfully added to notebook")
print(f"✅ Notebook saved: {notebook_path}")
print()
print("Verification:")
with open(notebook_path, 'r') as f:
    updated_notebook = json.load(f)
    cell_24_updated = updated_notebook['cells'][23]
    print(f"   Cell 24 output count: {len(cell_24_updated.get('outputs', []))}")
    print(f"   Cell 24 has output: {'✅ Yes' if cell_24_updated.get('outputs') else '❌ No'}")
