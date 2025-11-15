# Automation Scripts - Practical Examples

Real-world examples for common automation tasks.

## Table of Contents

1. [Basic Operations](#basic-operations)
2. [Navigation & Viewing](#navigation--viewing)
3. [Cell Editing](#cell-editing)
4. [Cell Execution](#cell-execution)
5. [Batch Operations](#batch-operations)
6. [Validation & Testing](#validation--testing)
7. [CI/CD Integration](#cicd-integration)
8. [Advanced Automation](#advanced-automation)

## Basic Operations

### Example 1: Load and Inspect Notebook

```python
from automation.notebook_controller.notebook_controller import NotebookController

# Load notebook
nb = NotebookController('analysis.ipynb')

# Get basic info
print(f"Total cells: {nb.get_cell_count()}")
print(f"Current cell: {nb.current_cell_index}")

# Show statistics
nb.get_stats()
```

### Example 2: View Specific Cells

```python
# View first cell
nb.first_cell()
nb.view_cell()

# View cell 10
nb.view_cell(index=10)

# View without printing
cell = nb.view_cell(index=5, show_output=False)
source = ''.join(cell.get('source', []))
print(f"Cell 5 content: {source[:100]}...")
```

## Navigation & Viewing

### Example 3: Navigate Through Notebook

```python
nb = NotebookController('notebook.ipynb')

# Sequential navigation
nb.first_cell()
for i in range(10):
    nb.view_cell()
    nb.next_cell()

# Jump to specific cells
nb.jump_to_cell(25)
nb.jump_to_cell(-1)  # Last cell
nb.jump_to_cell(-10)  # 10th from end
```

### Example 4: Search for Content

```python
# Simple text search
matches = nb.search_cells('pandas')

# Regex search
matches = nb.search_cells(r'def \w+\(.*\):', regex=True)

# Search only code cells
matches = nb.search_cells('import', cell_type='code')

# Search only markdown
matches = nb.search_cells('## ', cell_type='markdown')

# Process matches
for cell_idx, source in matches:
    print(f"Found in cell {cell_idx}")
```

### Example 5: List and Filter Cells

```python
# List all cells
nb.list_all_cells()

# List with content preview
nb.list_all_cells(show_content=True)

# Filter by type
code_cells = nb.filter_cells('code')
markdown_cells = nb.filter_cells('markdown')

print(f"Code cells: {len(code_cells)}")
print(f"Markdown cells: {len(markdown_cells)}")

# Process code cells only
for idx in code_cells:
    cell = nb.view_cell(idx, show_output=False)
    # ... process
```

## Cell Editing

### Example 6: Edit Cell Content

```python
# Edit current cell
nb.edit_cell("print('Hello World')")

# Edit specific cell
nb.edit_cell("import pandas as pd", index=0)

# Edit and change type
nb.edit_cell("# Data Analysis", index=5, cell_type='markdown')

# Append to cell
nb.append_to_cell("\nprint('More code')")
```

### Example 7: Insert New Cells

```python
# Insert code cell after current
nb.insert_cell("print('New cell')", cell_type='code', position='after')

# Insert markdown before cell 5
nb.insert_cell("## New Section", cell_type='markdown', index=5, position='before')

# Replace cell
nb.insert_cell("Completely new content", index=10, position='replace')

# Insert at end
nb.last_cell()
nb.insert_cell("# Conclusion", cell_type='markdown', position='after')
```

### Example 8: Delete and Duplicate Cells

```python
# Duplicate current cell
nb.duplicate_cell()

# Duplicate specific cell
nb.duplicate_cell(index=5)

# Delete cell
nb.delete_cell(index=10)

# Clear cell content (don't delete)
nb.clear_cell(index=5)
```

### Example 9: Using Undo/Redo

```python
# Make some changes
original_count = nb.get_cell_count()
nb.delete_cell(5)
nb.delete_cell(6)

# Undo deletions
nb.undo()  # Restore cell 6
nb.undo()  # Restore cell 5

# Redo if needed
nb.redo()

# View history
nb.show_history()
```

## Cell Execution

### Example 10: Execute Single Cell

```python
# Execute current cell
success, msg = nb.execute_cell()

if success:
    print("Cell executed successfully")
    # View output
    cell = nb.view_cell(show_output=False)
    outputs = cell.get('outputs', [])
    for output in outputs:
        print(output)
else:
    print(f"Execution failed: {msg}")
```

### Example 11: Execute with Custom Timeout

```python
# Long-running cell
success, msg = nb.execute_cell(index=10, timeout=300)  # 5 minutes

if not success:
    print(f"Timeout or error: {msg}")
```

### Example 12: Execute Range of Cells

```python
# Execute cells 0-20
nb.execute_all_cells(start_index=0, end_index=20)

# Execute from cell 25 to end
nb.execute_all_cells(start_index=25)

# Execute all cells
nb.execute_all_cells()
```

### Example 13: Clear Outputs

```python
# Clear specific cell output
nb.clear_outputs(index=5)

# Clear current cell
nb.clear_outputs()

# Clear all outputs
nb.clear_all_outputs()

# Save clean notebook
nb.save_as('notebook_clean.ipynb')
```

## Batch Operations

### Example 14: Search and Replace

```python
# Find first
matches = nb.search_cells('old_function_name')
print(f"Found {len(matches)} occurrences")

# Replace all
nb.replace_in_all_cells('old_function_name', 'new_function_name')

# Replace only in code cells
nb.replace_in_all_cells('import old', 'import new', cell_type='code')

# Replace only in markdown
nb.replace_in_all_cells('old title', 'new title', cell_type='markdown')

nb.save()
```

### Example 15: Merge Cells

```python
# Merge cells 5-10 into one
nb.merge_cells(start_index=5, end_index=10)

# Merge with custom separator
nb.merge_cells(start_index=15, end_index=20, separator='\n\n# ---\n\n')

nb.save()
```

### Example 16: Extract and Export

```python
# Export single cell
nb.export_cell(index=10, output_file='imports.py')

# Export all code cells
code_cells = nb.filter_cells('code')
for idx in code_cells:
    nb.export_cell(index=idx, output_file=f'cell_{idx}.py')

# Get cell content
content = nb.export_cell(index=5)
print(content)
```

### Example 17: Import from Files

```python
# Import Python file as code cell
nb.import_from_file('helper.py', cell_type='code', position='after')

# Import markdown
nb.import_from_file('notes.md', cell_type='markdown', position='before')
```

## Validation & Testing

### Example 18: Check for Empty Cells

```python
nb = NotebookController('notebook.ipynb', auto_backup=False)

empty_cells = []
for i in range(nb.get_cell_count()):
    cell = nb.view_cell(i, show_output=False)
    source = ''.join(cell.get('source', []))
    if not source.strip():
        empty_cells.append(i)

if empty_cells:
    print(f"Found {len(empty_cells)} empty cells: {empty_cells}")
else:
    print("No empty cells found")
```

### Example 19: Check for Execution Errors

```python
code_cells = nb.filter_cells('code')
errors = []

for idx in code_cells:
    cell = nb.view_cell(idx, show_output=False)
    outputs = cell.get('outputs', [])

    for output in outputs:
        if output.get('output_type') == 'error':
            error_name = output.get('ename', 'Unknown')
            error_value = output.get('evalue', '')
            errors.append({
                'cell': idx,
                'error': error_name,
                'message': error_value
            })

if errors:
    print(f"Found {len(errors)} errors:")
    for err in errors:
        print(f"  Cell {err['cell']}: {err['error']} - {err['message']}")
else:
    print("No errors found")
```

### Example 20: Validate Notebook Structure

```python
def validate_notebook(notebook_path):
    """Comprehensive notebook validation."""
    nb = NotebookController(notebook_path, auto_backup=False)
    issues = []

    # Check 1: Empty cells
    for i in range(nb.get_cell_count()):
        cell = nb.view_cell(i, show_output=False)
        source = ''.join(cell.get('source', []))
        if not source.strip():
            issues.append(f"Cell {i}: Empty cell")

    # Check 2: Execution errors
    for idx in nb.filter_cells('code'):
        cell = nb.view_cell(idx, show_output=False)
        for output in cell.get('outputs', []):
            if output.get('output_type') == 'error':
                issues.append(f"Cell {idx}: {output.get('ename')} error")

    # Check 3: Required imports
    has_pandas = False
    for idx in nb.filter_cells('code'):
        cell = nb.view_cell(idx, show_output=False)
        source = ''.join(cell.get('source', []))
        if 'import pandas' in source:
            has_pandas = True
            break

    if not has_pandas:
        issues.append("Missing pandas import")

    # Report
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Notebook validation passed")
        return True

# Run validation
validate_notebook('analysis.ipynb')
```

## CI/CD Integration

### Example 21: Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Clear outputs from all notebooks before commit
for notebook in notebooks/*.ipynb; do
    echo "Cleaning $notebook..."
    python automation/notebook_controller/notebook_controller.py "$notebook" --clear-outputs
    git add "$notebook"
done
```

### Example 22: GitHub Actions Workflow

```yaml
# .github/workflows/test-notebooks.yml
name: Test Notebooks

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install jupyter nbconvert pandas numpy matplotlib

      - name: Execute notebooks
        run: |
          for notebook in notebooks/*.ipynb; do
            echo "Testing $notebook..."
            python automation/notebook_controller/notebook_controller.py \
              "$notebook" --execute-all
          done

      - name: Validate notebooks
        run: |
          python automation/notebook_controller/examples.py 8
```

### Example 23: Makefile Targets

```makefile
# Makefile

.PHONY: clean-notebooks execute-notebooks validate-notebooks

clean-notebooks:
	@echo "Cleaning all notebooks..."
	@for nb in notebooks/*.ipynb; do \
		python automation/notebook_controller/notebook_controller.py "$$nb" --clear-outputs; \
	done
	@echo "Done!"

execute-notebooks:
	@echo "Executing all notebooks..."
	@for nb in notebooks/*.ipynb; do \
		echo "Executing $$nb..."; \
		python automation/notebook_controller/notebook_controller.py "$$nb" --execute-all; \
	done
	@echo "Done!"

validate-notebooks:
	@echo "Validating notebooks..."
	@python automation/notebook_controller/examples.py 8

test: validate-notebooks execute-notebooks
```

## Advanced Automation

### Example 24: Dynamic Notebook Generation

```python
from automation.notebook_controller.notebook_controller import NotebookController

# Start with template
nb = NotebookController('template.ipynb')

# Clear all cells except first
while nb.get_cell_count() > 1:
    nb.jump_to_cell(1)
    nb.delete_cell()

# Build notebook programmatically
nb.edit_cell("# Automated Analysis Report", cell_type='markdown', index=0)

# Add imports
nb.insert_cell("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
""", cell_type='code', position='after')

# Add data loading
nb.insert_cell("""
# Load data
df = pd.read_csv('data.csv')
print(f"Shape: {df.shape}")
df.head()
""", cell_type='code', position='after')

# Add analysis sections
sections = [
    ("## Data Overview", "markdown"),
    ("df.info()\ndf.describe()", "code"),
    ("## Visualizations", "markdown"),
    ("df.hist(figsize=(12, 8))\nplt.tight_layout()", "code"),
]

for content, cell_type in sections:
    nb.insert_cell(content, cell_type=cell_type, position='after')

# Execute all
nb.execute_all_cells()

# Save
nb.save_as('automated_report.ipynb')
```

### Example 25: Notebook Comparison

```python
def compare_notebooks(nb1_path, nb2_path):
    """Compare two notebooks."""
    nb1 = NotebookController(nb1_path, auto_backup=False)
    nb2 = NotebookController(nb2_path, auto_backup=False)

    print(f"Notebook 1: {nb1.get_cell_count()} cells")
    print(f"Notebook 2: {nb2.get_cell_count()} cells")

    # Compare cell counts by type
    nb1_code = len(nb1.filter_cells('code'))
    nb2_code = len(nb2.filter_cells('code'))

    print(f"\nCode cells: {nb1_code} vs {nb2_code}")
    print(f"Markdown cells: {nb1.get_cell_count() - nb1_code} vs {nb2.get_cell_count() - nb2_code}")

compare_notebooks('v1.ipynb', 'v2.ipynb')
```

### Example 26: Batch Notebook Processing

```python
import os
from pathlib import Path

def process_all_notebooks(directory, operation):
    """Process all notebooks in directory."""
    notebook_files = Path(directory).glob('*.ipynb')

    for nb_path in notebook_files:
        print(f"Processing {nb_path.name}...")
        nb = NotebookController(str(nb_path))

        # Apply operation
        operation(nb)

        # Save
        nb.save()
        print(f"  ✓ Done")

# Clear outputs from all notebooks
def clear_outputs(nb):
    nb.clear_all_outputs()

process_all_notebooks('notebooks/', clear_outputs)

# Execute all notebooks
def execute_all(nb):
    nb.execute_all_cells()

process_all_notebooks('notebooks/', execute_all)
```

### Example 27: Custom Analysis Script

```python
def analyze_imports(notebook_path):
    """Analyze all imports in a notebook."""
    import re

    nb = NotebookController(notebook_path, auto_backup=False)

    imports = set()
    code_cells = nb.filter_cells('code')

    for idx in code_cells:
        cell = nb.view_cell(idx, show_output=False)
        source = ''.join(cell.get('source', []))

        # Find import statements
        for line in source.split('\n'):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                imports.add(line.strip())

    print(f"Found {len(imports)} unique imports:")
    for imp in sorted(imports):
        print(f"  {imp}")

    return imports

# Analyze
imports = analyze_imports('analysis.ipynb')
```

### Example 28: Interactive Notebook Editor

```python
def interactive_editor(notebook_path):
    """Interactive notebook editing session."""
    nb = NotebookController(notebook_path)

    while True:
        print(f"\nCurrent cell: {nb.current_cell_index}/{nb.get_cell_count()-1}")
        print("Commands: view, edit, next, prev, jump, save, exit")

        cmd = input("> ").strip().lower()

        if cmd == 'view':
            nb.view_cell()
        elif cmd == 'edit':
            print("Enter new content (Ctrl+D when done):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            content = '\n'.join(lines)
            nb.edit_cell(content)
        elif cmd == 'next':
            nb.next_cell()
        elif cmd == 'prev':
            nb.prev_cell()
        elif cmd.startswith('jump '):
            idx = int(cmd.split()[1])
            nb.jump_to_cell(idx)
        elif cmd == 'save':
            nb.save()
            print("Saved!")
        elif cmd == 'exit':
            break

# Run interactive editor
interactive_editor('notebook.ipynb')
```

## Running Examples

All examples can be run from the project root:

```bash
# Copy example to a script
cat > my_script.py << 'EOF'
from automation.notebook_controller.notebook_controller import NotebookController

nb = NotebookController('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb')
nb.get_stats()
EOF

# Run it
python my_script.py
```

Or use the built-in examples:

```bash
# Run example 1
python automation/notebook_controller/examples.py 1

# Run all examples
python automation/notebook_controller/examples.py all
```
