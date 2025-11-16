#!/usr/bin/env python3
"""
Comprehensive Cell-by-Cell Notebook Review
Reviews all 94 cells systematically with detailed analysis
"""

import json
from pathlib import Path

# Load notebook
nb_path = Path('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb')
with open(nb_path, 'r') as f:
    nb = json.load(f)

cells = nb['cells']
total_cells = len(cells)

print("="*80)
print("COMPREHENSIVE NOTEBOOK REVIEW - ALL CELLS")
print("="*80)
print(f"Total Cells: {total_cells}")
print()

# Track phase boundaries
phase_markers = {
    "Phase 1: Data Acquisition": (0, 27),
    "Phase 2A: Preprocessing & EDA": (28, 60),
    "Phase 2B: Feature Engineering": (61, 68),
    "Phase 3: Modeling & Evaluation": (69, 93)
}

# Review each cell
for i, cell in enumerate(cells):
    # Check if we're starting a new phase
    for phase_name, (start, end) in phase_markers.items():
        if i == start:
            print("\n" + "="*80)
            print(f"{phase_name.upper()} (Cells {start+1}-{end+1})")
            print("="*80)
            print()

    cell_type = cell['cell_type']
    source = ''.join(cell.get('source', []))

    # Cell header
    print(f"Cell {i+1:3d} [{cell_type.upper():8s}]", end="")

    # For markdown cells
    if cell_type == 'markdown':
        # Check if it's an educational cell
        is_educational = '🎓 Understanding' in source
        is_header = source.strip().startswith('#') and not is_educational

        if is_educational:
            # Extract topic
            topic = source.split('🎓 Understanding')[1].split('\n')[0].strip()
            print(f" [EDUCATIONAL] 🎓 {topic}")

            # Count LaTeX formulas
            latex_count = source.count('$$') // 2
            if latex_count > 0:
                print(f"      LaTeX formulas: {latex_count}")

            # Check structure
            has_what = 'What' in source or 'what' in source[:200]
            has_why = 'Why' in source or 'why' in source[:200]
            has_formula = '$$' in source

            structure_check = []
            if has_what: structure_check.append("WHAT✅")
            if has_why: structure_check.append("WHY✅")
            if has_formula: structure_check.append("FORMULAS✅")

            if structure_check:
                print(f"      Structure: {', '.join(structure_check)}")

        elif is_header:
            # Extract first header line
            first_line = source.strip().split('\n')[0]
            # Remove markdown formatting
            header_text = first_line.replace('#', '').replace('*', '').replace('_', '').strip()
            if header_text:
                print(f" {header_text[:60]}")
        else:
            # Regular markdown
            preview = source.strip()[:70].replace('\n', ' ')
            print(f" {preview}...")

    # For code cells
    elif cell_type == 'code':
        outputs = cell.get('outputs', [])
        has_output = len(outputs) > 0

        # Get first line of code
        code_lines = source.strip().split('\n')
        first_code_line = code_lines[0] if code_lines else ''

        # Identify what the code does
        if 'import' in first_code_line:
            print(f" Import libraries")
        elif 'read_csv' in source.lower() or 'load' in first_code_line.lower():
            print(f" Load dataset")
        elif 'describe(' in source:
            print(f" Summary statistics")
        elif 'isnull' in source or 'fillna' in source:
            print(f" Handle missing values")
        elif 'plot' in source or 'plt.' in source or 'sns.' in source:
            print(f" Visualization")
        elif 'train_test_split' in source:
            print(f" Train-test split")
        elif 'LinearRegression' in source or '.fit(' in source:
            print(f" Train model")
        elif 'predict' in source:
            print(f" Make predictions")
        elif 'r2_score' in source or 'mean_squared_error' in source:
            print(f" Evaluate model")
        else:
            # Show first meaningful line
            preview = first_code_line[:60]
            print(f" {preview}")

        # Output status
        if has_output:
            output_types = [o.get('output_type', 'unknown') for o in outputs]
            unique_types = list(set(output_types))
            print(f"      Output: {', '.join(unique_types)}")
        else:
            # Check if it should have output
            if 'import' not in source and '=' in first_code_line and 'print' not in source:
                print(f"      Output: None (assignment)")
            else:
                print(f"      ⚠️  Output: MISSING!")

    print()

# Summary statistics
print("\n" + "="*80)
print("REVIEW SUMMARY")
print("="*80)
print()

# Count cell types
code_cells = sum(1 for c in cells if c['cell_type'] == 'code')
md_cells = sum(1 for c in cells if c['cell_type'] == 'markdown')
educational_cells = sum(1 for c in cells if c['cell_type'] == 'markdown' and '🎓 Understanding' in ''.join(c.get('source', [])))

print(f"Total Cells: {total_cells}")
print(f"  Code cells: {code_cells}")
print(f"  Markdown cells: {md_cells}")
print(f"  Educational cells: {educational_cells}")
print()

# Count cells with output
code_with_output = sum(1 for c in cells if c['cell_type'] == 'code' and len(c.get('outputs', [])) > 0)
print(f"Code cells with output: {code_with_output}/{code_cells} ({100*code_with_output//code_cells}%)")
print()

# Count LaTeX formulas
total_latex = 0
for c in cells:
    if c['cell_type'] == 'markdown':
        source = ''.join(c.get('source', []))
        total_latex += source.count('$$') // 2

print(f"Total LaTeX formulas: {total_latex}")
print()

# List all educational cells
print("="*80)
print("EDUCATIONAL CELLS LIST")
print("="*80)
print()

for i, c in enumerate(cells):
    if c['cell_type'] == 'markdown':
        source = ''.join(c.get('source', []))
        if '🎓 Understanding' in source:
            topic = source.split('🎓 Understanding')[1].split('\n')[0].strip()
            latex_count = source.count('$$') // 2
            print(f"Cell {i+1:3d}: {topic:50s} ({latex_count} formulas)")

print()
print("="*80)
print("REVIEW COMPLETE")
print("="*80)
