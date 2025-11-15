# Notebook Controller - Complete Usage Guide

## Overview

The Notebook Controller is a professional-grade automation tool for complete control over Jupyter notebooks (.ipynb files). It provides programmatic and interactive interfaces for viewing, editing, executing, and managing notebook cells.

## Features

### Core Capabilities
- ✅ **Full Cell Control**: View, edit, insert, delete, duplicate cells
- ✅ **Cell Navigation**: Jump to any cell, move forward/backward
- ✅ **Cell Execution**: Execute individual cells or entire notebook
- ✅ **Undo/Redo**: Full history with 50-state rollback
- ✅ **Search & Replace**: Pattern matching across cells
- ✅ **Batch Operations**: Merge cells, clear outputs, bulk replace
- ✅ **Auto Backup**: Timestamped backups before modifications
- ✅ **CLI Mode**: Interactive command-line interface
- ✅ **API Mode**: Programmatic Python API

## Installation

```bash
# No installation needed - just ensure you have Jupyter
pip install jupyter nbconvert

# Make script executable
chmod +x scripts/notebook_controller.py
```

## Quick Start

### 1. Interactive Mode (Recommended for Exploration)

```bash
python scripts/notebook_controller.py notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb
```

This starts an interactive CLI where you can type commands:

```
[Cell 0] > help          # Show all commands
[Cell 0] > list          # List all cells
[Cell 0] > view 5        # View cell 5
[Cell 0] > jump 10       # Jump to cell 10
[Cell 0] > run           # Execute current cell
[Cell 0] > save          # Save changes
[Cell 0] > exit          # Exit
```

### 2. Command-Line Mode (For Automation)

```bash
# View specific cell
python scripts/notebook_controller.py notebook.ipynb --view 5

# List all cells with content
python scripts/notebook_controller.py notebook.ipynb --list

# Execute all cells
python scripts/notebook_controller.py notebook.ipynb --execute-all

# Clear all outputs
python scripts/notebook_controller.py notebook.ipynb --clear-outputs

# Search for pattern
python scripts/notebook_controller.py notebook.ipynb --search "import pandas"

# Show statistics
python scripts/notebook_controller.py notebook.ipynb --stats
```

### 3. Python API Mode (For Scripts)

```python
from scripts.notebook_controller import NotebookController

# Initialize controller
nb = NotebookController('notebook.ipynb')

# Navigate and view
nb.jump_to_cell(5)
nb.view_cell()
nb.next_cell()

# Edit cells
nb.edit_cell("print('Hello World')", index=5)
nb.insert_cell("# New markdown cell", cell_type='markdown', position='after')

# Execute cells
nb.execute_cell(5)
nb.execute_all_cells(start_index=0, end_index=10)

# Undo/redo
nb.undo()
nb.redo()

# Save
nb.save()
```

## Detailed Command Reference

### Navigation Commands

#### `next` or `n`
Move to the next cell
```
[Cell 5] > next
➡️  Moved to cell 6
```

#### `prev` or `p`
Move to the previous cell
```
[Cell 5] > prev
⬅️  Moved to cell 4
```

#### `jump <index>` or `j <index>`
Jump to a specific cell by index
```
[Cell 0] > jump 15
📍 Jumped to cell 15
```

Supports negative indexing:
```
[Cell 0] > jump -1    # Jump to last cell
[Cell 0] > jump -5    # Jump to 5th cell from end
```

#### `first`
Jump to the first cell
```
[Cell 10] > first
⏮️  Moved to first cell
```

#### `last`
Jump to the last cell
```
[Cell 0] > last
⏭️  Moved to last cell
```

### Viewing Commands

#### `view [index]` or `v [index]`
View cell content with outputs
```
[Cell 5] > view
======================================================================
Cell 5 | Type: CODE
======================================================================
import pandas as pd
df = pd.read_csv('data.csv')
df.head()

----------------------------------------------------------------------
OUTPUTS:
----------------------------------------------------------------------
[Result 0]:
   col1  col2  col3
0     1     2     3
1     4     5     6
======================================================================

[Cell 5] > view 10    # View cell 10 specifically
```

#### `list` or `ls`
List all cells with summary
```
[Cell 0] > list
📓 Notebook: example.ipynb
Total cells: 20

   Cell   0 | code     | 5 lines
👉 Cell   1 | markdown | 2 lines
   Cell   2 | code     | 15 lines
   ...
```

With content preview:
```
[Cell 0] > list --content
[Cell 0] > ls -c

   Cell   0 | code     | import pandas as pd import numpy as np...
👉 Cell   1 | markdown | # Introduction This notebook demonstrates...
   Cell   2 | code     | df = pd.read_csv('data.csv') print(df.shape)...
```

#### `search <pattern>`
Search for text pattern in all cells
```
[Cell 0] > search import pandas

🔍 Searching for: 'import pandas'

✅ Found 3 matches

Cell 0 (code):
  Line 1: import pandas as pd

Cell 5 (code):
  Line 1: import pandas as pd
  Line 2: import numpy as np

Cell 15 (markdown):
  Line 3: We use `import pandas` to load the library
```

### Editing Commands

#### `edit` or `e`
Edit the current cell
```
[Cell 5] > edit
Enter new content (Ctrl+D or Ctrl+Z to finish):
print('Hello World')
print('Updated code')
^D
✏️  Edited cell 5
```

#### `clear [index]`
Clear cell content
```
[Cell 5] > clear          # Clear current cell
[Cell 5] > clear 10       # Clear cell 10
```

#### `delete [index]` or `del [index]`
Delete a cell
```
[Cell 5] > delete         # Delete current cell
🗑️  Deleted cell 5 (code)

[Cell 0] > delete 10      # Delete cell 10
🗑️  Deleted cell 10 (markdown)
```

#### `insert [type]`
Insert a new cell
```
[Cell 5] > insert code
Enter content for new code cell (Ctrl+D to finish):
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
^D
➕ Inserted code cell at position 6

[Cell 5] > insert markdown
Enter content for new markdown cell (Ctrl+D to finish):
# New Section
This is a new markdown cell
^D
➕ Inserted markdown cell at position 6
```

#### `duplicate` or `dup`
Duplicate the current cell
```
[Cell 5] > duplicate
➕ Inserted code cell at position 6
```

### Execution Commands

#### `run [index]` or `r [index]`
Execute a code cell
```
[Cell 5] > run
▶️  Executing cell 5...
✅ Cell 5 executed successfully

Outputs:
[Result 0]:
   col1  col2
0     1     2
1     3     4
```

Execute specific cell:
```
[Cell 0] > run 15
▶️  Executing cell 15...
✅ Cell 15 executed successfully
```

#### `runall`
Execute all cells in sequence
```
[Cell 0] > runall

▶️  Executing cells 0 to 80...
▶️  Executing cell 0...
✅ Cell 0 executed successfully
▶️  Executing cell 1...
✅ Cell 1 executed successfully
...

======================================================================
Execution Summary:
  ✅ Successful: 75
  ❌ Failed: 0
======================================================================
```

#### `clearoutputs [all]`
Clear cell outputs
```
[Cell 5] > clearoutputs        # Clear current cell output
🧹 Cleared outputs from cell 5

[Cell 0] > clearoutputs all    # Clear all outputs
🧹 Cleared outputs from 45 code cells
```

### Undo/Redo Commands

#### `undo` or `u`
Undo the last change
```
[Cell 5] > delete
🗑️  Deleted cell 5 (code)

[Cell 5] > undo
↶  Undo successful (position 5/6)
```

#### `redo`
Redo the last undone change
```
[Cell 5] > undo
↶  Undo successful (position 4/6)

[Cell 5] > redo
↷  Redo successful (position 5/6)
```

#### `history` or `hist`
Show undo/redo history
```
[Cell 5] > history

📜 History (6 states):
   Current position: 5

   1. 10:15:23 - 80 cells
   2. 10:16:45 - 81 cells
   3. 10:17:12 - 81 cells
   4. 10:18:30 - 80 cells
👉 5. 10:19:05 - 81 cells
   6. 10:20:15 - 81 cells
```

### Save Commands

#### `save` or `s`
Save notebook to original file
```
[Cell 5] > save
📦 Backup created: notebook_backup_20250115_101923.ipynb
💾 Saved notebook: notebook.ipynb
```

#### `saveas <path>`
Save notebook to a new file
```
[Cell 5] > saveas notebooks/notebook_modified.ipynb
💾 Saved notebook: notebook_modified.ipynb
```

### Info Commands

#### `stats`
Show notebook statistics
```
[Cell 5] > stats

📊 Notebook Statistics
======================================================================
File: Ames_Housing_Price_Prediction_EXECUTED.ipynb
Total cells: 81
  - Code cells: 58
  - Markdown cells: 23
Total lines: 1547
Current cell: 5
History states: 12
======================================================================
```

#### `help` or `h`
Show help message
```
[Cell 0] > help
[Shows complete command reference]
```

#### `exit`, `quit`, or `q`
Exit interactive mode
```
[Cell 5] > exit
👋 Goodbye!
```

## Python API Examples

### Example 1: Batch Cell Editing

```python
from scripts.notebook_controller import NotebookController

# Load notebook
nb = NotebookController('analysis.ipynb')

# Find all cells with old import
nb.search_cells('from sklearn.model_selection import train_test_split')

# Replace across all cells
nb.replace_in_all_cells(
    'from sklearn.model_selection import train_test_split',
    'from sklearn.model_selection import train_test_split, cross_val_score'
)

# Save changes
nb.save()
```

### Example 2: Automated Cell Execution

```python
from scripts.notebook_controller import NotebookController

# Load notebook
nb = NotebookController('pipeline.ipynb')

# Clear all previous outputs
nb.clear_all_outputs()

# Execute cells 0-20 (data loading and preprocessing)
nb.execute_all_cells(start_index=0, end_index=20)

# Check specific cell output
nb.jump_to_cell(15)
cell = nb.view_cell(show_output=False)
outputs = cell.get('outputs', [])

# Continue execution if successful
if outputs and outputs[0].get('output_type') != 'error':
    nb.execute_all_cells(start_index=21, end_index=50)

# Save executed notebook
nb.save_as('pipeline_executed.ipynb')
```

### Example 3: Notebook Validation

```python
from scripts.notebook_controller import NotebookController

def validate_notebook(notebook_path):
    """Validate notebook structure and content."""
    nb = NotebookController(notebook_path, auto_backup=False)

    issues = []

    # Check for empty cells
    for i in range(nb.get_cell_count()):
        cell = nb.view_cell(i, show_output=False)
        source = ''.join(cell.get('source', []))

        if not source.strip():
            issues.append(f"Cell {i}: Empty cell")

    # Check for cells with errors
    code_cells = nb.filter_cells('code')
    for i in code_cells:
        cell = nb.view_cell(i, show_output=False)
        outputs = cell.get('outputs', [])

        for output in outputs:
            if output.get('output_type') == 'error':
                error = output.get('ename', 'Unknown')
                issues.append(f"Cell {i}: Error - {error}")

    # Report
    if issues:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("✅ Notebook validation passed")

    return len(issues) == 0

# Run validation
validate_notebook('analysis.ipynb')
```

### Example 4: Dynamic Notebook Generation

```python
from scripts.notebook_controller import NotebookController

# Create from existing template
nb = NotebookController('template.ipynb')

# Clear all cells
while nb.get_cell_count() > 1:
    nb.delete_cell(0)

# Build new notebook programmatically
nb.edit_cell("# Machine Learning Pipeline", cell_type='markdown', index=0)

# Add imports
nb.insert_cell("""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
""", cell_type='code', position='after')

# Add data loading
nb.insert_cell("""
# Load data
df = pd.read_csv('data/housing.csv')
print(f"Dataset shape: {df.shape}")
df.head()
""", cell_type='code', position='after')

# Add more cells...
nb.insert_cell("## Data Preprocessing", cell_type='markdown', position='after')

# Execute to generate outputs
nb.execute_all_cells()

# Save
nb.save_as('generated_pipeline.ipynb')
```

### Example 5: Cell Content Analysis

```python
from scripts.notebook_controller import NotebookController
import re

def analyze_imports(notebook_path):
    """Analyze all imports in a notebook."""
    nb = NotebookController(notebook_path, auto_backup=False)

    imports = set()
    code_cells = nb.filter_cells('code')

    for i in code_cells:
        cell = nb.view_cell(i, show_output=False)
        source = ''.join(cell.get('source', []))

        # Find import statements
        import_pattern = r'^(?:from\s+(\S+)\s+)?import\s+(.+)$'
        for line in source.split('\n'):
            match = re.match(import_pattern, line.strip())
            if match:
                imports.add(line.strip())

    print(f"📦 Found {len(imports)} unique imports:")
    for imp in sorted(imports):
        print(f"   {imp}")

    return imports

# Analyze imports
imports = analyze_imports('analysis.ipynb')
```

## Advanced Usage

### Working with Cell Metadata

```python
# Access cell metadata
cell = nb.view_cell(5, show_output=False)
metadata = cell.get('metadata', {})

# Modify cell (preserves metadata)
nb.edit_cell("new content", index=5)
```

### Batch Operations

```python
# Merge multiple cells
nb.merge_cells(start_index=5, end_index=8, separator='\n\n')

# Filter and process
markdown_cells = nb.filter_cells('markdown')
for idx in markdown_cells:
    cell = nb.view_cell(idx, show_output=False)
    source = ''.join(cell.get('source', []))
    if '##' in source:
        print(f"Section header at cell {idx}")
```

### Export and Import

```python
# Export cell to file
nb.export_cell(index=10, output_file='cell_10.py')

# Import from file
nb.import_from_file('snippet.py', cell_type='code', position='after')
```

## Tips and Best Practices

### 1. Always Use Auto-Backup
```python
# Auto-backup is enabled by default
nb = NotebookController('important.ipynb', auto_backup=True)
```

### 2. Check Cell Count Before Operations
```python
if nb.get_cell_count() > 10:
    nb.delete_cell(10)
```

### 3. Use Undo for Safety
```python
# Try an operation
nb.delete_cell(5)

# If not what you wanted
nb.undo()
```

### 4. Save Incrementally
```python
# Make changes
nb.edit_cell("new content", index=5)
nb.save()

# More changes
nb.edit_cell("more content", index=6)
nb.save()
```

### 5. Test Execution with Single Cell
```python
# Test one cell first
success, msg = nb.execute_cell(0)

if success:
    # Execute all
    nb.execute_all_cells()
```

## Troubleshooting

### Issue: Execution Timeout
```python
# Increase timeout (default is 60 seconds)
nb.execute_cell(index=10, timeout=300)  # 5 minutes
```

### Issue: Large Notebook Performance
```python
# Disable auto-backup for large notebooks
nb = NotebookController('huge.ipynb', auto_backup=False)

# Manual backup when needed
nb._create_backup()
```

### Issue: Cell Navigation Lost
```python
# Check current position
print(f"Current cell: {nb.current_cell_index}")

# Reset to first cell
nb.first_cell()
```

## Integration Examples

### With Git Workflow
```python
import subprocess
from scripts.notebook_controller import NotebookController

# Clear outputs before commit
nb = NotebookController('analysis.ipynb')
nb.clear_all_outputs()
nb.save()

# Git operations
subprocess.run(['git', 'add', 'analysis.ipynb'])
subprocess.run(['git', 'commit', '-m', 'Update analysis notebook'])
```

### With Testing Framework
```python
import pytest
from scripts.notebook_controller import NotebookController

def test_notebook_executes():
    """Test that notebook executes without errors."""
    nb = NotebookController('analysis.ipynb')
    nb.clear_all_outputs()

    # Execute all cells
    nb.execute_all_cells()

    # Check for errors
    code_cells = nb.filter_cells('code')
    for i in code_cells:
        cell = nb.view_cell(i, show_output=False)
        outputs = cell.get('outputs', [])

        for output in outputs:
            assert output.get('output_type') != 'error', \
                f"Cell {i} has error: {output.get('ename')}"
```

## Command-Line Automation

### Bash Script Example
```bash
#!/bin/bash

# Clear outputs from all notebooks
for notebook in notebooks/*.ipynb; do
    echo "Processing $notebook..."
    python scripts/notebook_controller.py "$notebook" --clear-outputs
done

echo "All notebooks cleaned!"
```

### Makefile Example
```makefile
.PHONY: clean-notebooks execute-notebooks

clean-notebooks:
	@for nb in notebooks/*.ipynb; do \
		python scripts/notebook_controller.py "$$nb" --clear-outputs; \
	done

execute-notebooks:
	@for nb in notebooks/*.ipynb; do \
		python scripts/notebook_controller.py "$$nb" --execute-all; \
	done
```

## API Reference Summary

### NotebookController Class

#### Initialization
- `__init__(notebook_path, auto_backup=True)`

#### Navigation
- `jump_to_cell(index)` - Jump to cell
- `next_cell()` - Move to next
- `prev_cell()` - Move to previous
- `first_cell()` - Jump to first
- `last_cell()` - Jump to last

#### Viewing
- `view_cell(index, show_output)` - View cell
- `list_all_cells(show_content)` - List all
- `search_cells(pattern, regex, cell_type)` - Search

#### Editing
- `edit_cell(content, index, cell_type)` - Edit cell
- `clear_cell(index)` - Clear content
- `delete_cell(index)` - Delete cell
- `insert_cell(content, cell_type, index, position)` - Insert
- `duplicate_cell(index)` - Duplicate

#### Execution
- `execute_cell(index, timeout)` - Execute one
- `execute_all_cells(start_index, end_index)` - Execute range
- `clear_outputs(index)` - Clear output
- `clear_all_outputs()` - Clear all outputs

#### History
- `undo()` - Undo change
- `redo()` - Redo change
- `show_history()` - Show history

#### Batch Operations
- `filter_cells(cell_type)` - Get indices by type
- `replace_in_all_cells(old, new, cell_type)` - Bulk replace
- `merge_cells(start, end, separator)` - Merge cells

#### Save
- `save()` - Save to original
- `save_as(path)` - Save to new file
- `_create_backup()` - Manual backup

#### Info
- `get_cell_count()` - Get total cells
- `get_stats()` - Show statistics

## License

This tool is part of the Ames Housing Price Prediction project.
