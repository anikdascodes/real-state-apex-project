# Automation Scripts for Jupyter Notebooks

Complete automation toolkit for Jupyter notebook management, execution, and control.

## 📁 Directory Structure

```
automation/
├── README.md                          # This file - Main documentation
├── notebook_controller/               # Notebook control & manipulation
│   ├── notebook_controller.py        # Main controller script (1000+ lines)
│   ├── examples.py                   # 8 practical automation examples
│   └── demo.sh                       # Interactive demo script
├── notebook_execution/                # Notebook execution utilities
│   └── execute_notebook.py           # Execute notebooks with output capture
├── pdf_export/                        # PDF generation from notebooks
│   ├── notebook_to_html_pdf.py       # HTML-based PDF generator
│   ├── notebook_to_pdf.py            # LaTeX-based PDF generator
│   └── README.md                     # PDF export documentation
└── docs/                             # Additional documentation
    ├── QUICK_START.md                # Quick reference guide
    ├── API_REFERENCE.md              # Complete API documentation
    └── EXAMPLES.md                   # Detailed usage examples
```

## 🚀 Quick Start

### Installation

No installation needed! Just ensure you have Jupyter:

```bash
# Install Jupyter (if not already installed)
pip install jupyter nbconvert

# Or using uv (project uses uv)
uv pip install jupyter nbconvert
```

### Basic Usage

```bash
# Interactive mode - explore notebooks interactively
python automation/notebook_controller/notebook_controller.py notebook.ipynb

# Command-line mode - quick operations
python automation/notebook_controller/notebook_controller.py notebook.ipynb --stats

# Execute notebook - run all cells and capture outputs
python automation/notebook_execution/execute_notebook.py notebook.ipynb output.ipynb
```

## 📚 Available Tools

### 1. PDF Export (NEW!)

**Location**: `automation/pdf_export/notebook_to_html_pdf.py`

**Purpose**: Convert Jupyter notebooks to professional PDF documents with all outputs, images, and analysis

**Features**:
- ✅ Extract all markdown, code, and outputs
- ✅ Embed all images (plots, charts, graphs)
- ✅ Professional styling with CSS
- ✅ No LaTeX required (uses weasyprint)
- ✅ Single command execution
- ✅ 1.3 MB PDF from 81-cell notebook in ~10 seconds

**Quick Usage**:

```bash
# Generate PDF report
python automation/pdf_export/notebook_to_html_pdf.py \
    notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb \
    reports/Analysis_Report.pdf

# With our project notebook
python automation/pdf_export/notebook_to_html_pdf.py \
    notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb \
    reports/Ames_Housing_Analysis_Report.pdf
```

**Output Example**:
```
✅ PDF created successfully: reports/Ames_Housing_Analysis_Report.pdf
   Size: 1.30 MB
   Processed: 81 cells (42 code cells)
   Images: 11 plots/charts
```

**See**: `automation/pdf_export/README.md` for complete documentation

### 2. Notebook Controller

**Location**: `automation/notebook_controller/notebook_controller.py`

**Purpose**: Complete control over Jupyter notebooks - view, edit, execute, navigate cells

**Features**:
- ✅ View, edit, insert, delete cells
- ✅ Navigate (jump, next, prev, first, last)
- ✅ Execute cells with output capture
- ✅ Undo/Redo with 50-level history
- ✅ Search and replace across cells
- ✅ Batch operations (merge, filter, replace)
- ✅ Auto-backup before modifications
- ✅ Interactive CLI mode
- ✅ Python API for automation

**Quick Examples**:

```bash
# Show statistics
python automation/notebook_controller/notebook_controller.py notebook.ipynb --stats

# View specific cell
python automation/notebook_controller/notebook_controller.py notebook.ipynb --view 5

# Search for text
python automation/notebook_controller/notebook_controller.py notebook.ipynb --search "pandas"

# Execute all cells
python automation/notebook_controller/notebook_controller.py notebook.ipynb --execute-all

# Clear all outputs
python automation/notebook_controller/notebook_controller.py notebook.ipynb --clear-outputs

# List all cells
python automation/notebook_controller/notebook_controller.py notebook.ipynb --list

# Interactive mode
python automation/notebook_controller/notebook_controller.py notebook.ipynb
```

**Interactive Mode Commands**:

```
[Cell 0] > list          # List all cells
[Cell 0] > view 5        # View cell 5
[Cell 0] > jump 10       # Jump to cell 10
[Cell 0] > next          # Next cell
[Cell 0] > prev          # Previous cell
[Cell 0] > edit          # Edit current cell
[Cell 0] > run           # Execute current cell
[Cell 0] > runall        # Execute all cells
[Cell 0] > search text   # Search for 'text'
[Cell 0] > undo          # Undo last change
[Cell 0] > save          # Save notebook
[Cell 0] > stats         # Show statistics
[Cell 0] > help          # Show all commands
[Cell 0] > exit          # Exit
```

**Python API**:

```python
from automation.notebook_controller.notebook_controller import NotebookController

# Initialize
nb = NotebookController('notebook.ipynb')

# Navigate
nb.jump_to_cell(5)
nb.next_cell()
nb.view_cell()

# Edit
nb.edit_cell("print('Hello')", index=5)
nb.insert_cell("# Comment", cell_type='markdown')
nb.delete_cell(10)

# Execute
nb.execute_cell(5)
nb.execute_all_cells()

# Batch operations
nb.search_cells('pandas')
nb.replace_in_all_cells('old', 'new')
nb.clear_all_outputs()

# History
nb.undo()
nb.redo()

# Save
nb.save()
```

### 3. Notebook Execution

**Location**: `automation/notebook_execution/execute_notebook.py`

**Purpose**: Execute notebooks and capture all outputs

**Features**:
- ✅ Execute all cells in sequence
- ✅ Capture outputs, visualizations, errors
- ✅ Configurable timeout
- ✅ Progress reporting
- ✅ Error handling

**Usage**:

```bash
# Basic execution
python automation/notebook_execution/execute_notebook.py input.ipynb output.ipynb

# With timeout (default 600 seconds)
python automation/notebook_execution/execute_notebook.py input.ipynb output.ipynb --timeout 300
```

**Python API**:

```python
from automation.notebook_execution.execute_notebook import execute_notebook_cells

# Execute notebook
execute_notebook_cells('input.ipynb', 'output.ipynb')

# With custom timeout
execute_notebook_cells('input.ipynb', 'output.ipynb', timeout=300)
```

### 4. Automation Examples

**Location**: `automation/notebook_controller/examples.py`

**Purpose**: 8 practical examples demonstrating automation capabilities

**Available Examples**:

1. **Basic Navigation** - Navigate and view cells
2. **Search and Analyze** - Find patterns, get statistics
3. **Cell Manipulation** - Edit, insert, delete cells
4. **Undo/Redo** - History management
5. **Batch Operations** - Filter, merge, bulk operations
6. **Output Management** - Clear and manage outputs
7. **Export/Import** - Extract cells to files
8. **Validation** - Check notebook structure and errors

**Run Examples**:

```bash
# Run specific example
python automation/notebook_controller/examples.py 1

# Run all examples interactively
python automation/notebook_controller/examples.py all

# List available examples
python automation/notebook_controller/examples.py
```

### 5. Interactive Demo

**Location**: `automation/notebook_controller/demo.sh`

**Purpose**: Interactive walkthrough of all features

**Usage**:

```bash
bash automation/notebook_controller/demo.sh
```

## 🎯 Common Use Cases

### Use Case 1: Clean Notebook Before Git Commit

Remove all outputs and execution counts:

```bash
python automation/notebook_controller/notebook_controller.py notebook.ipynb --clear-outputs
```

Or with Python API:

```python
from automation.notebook_controller.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb')
nb.clear_all_outputs()
nb.save()
```

### Use Case 2: Execute Notebook Programmatically

Execute all cells and save with outputs:

```bash
python automation/notebook_controller/notebook_controller.py notebook.ipynb --execute-all
```

Or:

```bash
python automation/notebook_execution/execute_notebook.py notebook.ipynb notebook_executed.ipynb
```

### Use Case 3: Search and Replace Across Notebook

Find and replace text in all cells:

```python
from automation.notebook_controller.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb')

# Search first
nb.search_cells('old_function_name')

# Replace
nb.replace_in_all_cells('old_function_name', 'new_function_name')

# Save
nb.save()
```

### Use Case 4: Validate Notebook Structure

Check for errors and empty cells:

```python
from automation.notebook_controller.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb', auto_backup=False)

issues = []

# Check for empty cells
for i in range(nb.get_cell_count()):
    cell = nb.view_cell(i, show_output=False)
    source = ''.join(cell.get('source', []))
    if not source.strip():
        issues.append(f"Cell {i}: Empty cell")

# Check for execution errors
code_cells = nb.filter_cells('code')
for i in code_cells:
    cell = nb.view_cell(i, show_output=False)
    outputs = cell.get('outputs', [])
    for output in outputs:
        if output.get('output_type') == 'error':
            issues.append(f"Cell {i}: Error - {output.get('ename')}")

if issues:
    print(f"Found {len(issues)} issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Notebook validation passed!")
```

### Use Case 5: Extract Code from Specific Cells

Export cells to Python files:

```python
from automation.notebook_controller.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb')

# Export cell 10 to file
nb.export_cell(index=10, output_file='extracted_code.py')

# Export all code cells
code_cells = nb.filter_cells('code')
for i in code_cells:
    nb.export_cell(index=i, output_file=f'cell_{i}.py')
```

### Use Case 6: Merge Multiple Cells

Combine cells into one:

```python
from automation.notebook_controller.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb')

# Merge cells 5 through 10
nb.merge_cells(start_index=5, end_index=10, separator='\n\n')

nb.save()
```

### Use Case 7: Batch Process Multiple Notebooks

```bash
#!/bin/bash
# Clear outputs from all notebooks

for notebook in notebooks/*.ipynb; do
    echo "Processing $notebook..."
    python automation/notebook_controller/notebook_controller.py "$notebook" --clear-outputs
done

echo "Done!"
```

### Use Case 8: CI/CD Integration

Execute notebooks in CI pipeline:

```yaml
# .github/workflows/test-notebooks.yml
name: Test Notebooks

on: [push]

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
          python automation/notebook_execution/execute_notebook.py \
            notebooks/analysis.ipynb \
            notebooks/analysis_executed.ipynb

      - name: Validate execution
        run: |
          python automation/notebook_controller/examples.py 8
```

## 📖 Detailed Documentation

### Command Reference

#### Notebook Controller Commands

| Command | Short | Description | Example |
|---------|-------|-------------|---------|
| `--stats` | | Show notebook statistics | `--stats` |
| `--view N` | `-v N` | View cell N | `--view 5` |
| `--list` | `-l` | List all cells | `--list` |
| `--search TEXT` | `-s TEXT` | Search for text | `--search "pandas"` |
| `--execute N` | `-e N` | Execute cell N | `--execute 5` |
| `--execute-all` | | Execute all cells | `--execute-all` |
| `--clear-outputs` | `-c` | Clear all outputs | `--clear-outputs` |
| `--interactive` | `-i` | Start interactive mode | `--interactive` |
| `--no-backup` | | Disable auto-backup | `--no-backup` |

#### Interactive Mode Commands

| Command | Short | Description |
|---------|-------|-------------|
| `next` | `n` | Move to next cell |
| `prev` | `p` | Move to previous cell |
| `jump N` | `j N` | Jump to cell N |
| `first` | | Jump to first cell |
| `last` | | Jump to last cell |
| `view [N]` | `v [N]` | View cell content |
| `list` | `ls` | List all cells |
| `search TEXT` | | Search for text |
| `edit` | `e` | Edit current cell |
| `clear [N]` | | Clear cell content |
| `delete [N]` | `del [N]` | Delete cell |
| `insert [type]` | | Insert cell (code/markdown) |
| `duplicate` | `dup` | Duplicate current cell |
| `run [N]` | `r [N]` | Execute cell |
| `runall` | | Execute all cells |
| `clearoutputs [all]` | | Clear outputs |
| `undo` | `u` | Undo last change |
| `redo` | | Redo last undo |
| `history` | `hist` | Show history |
| `save` | `s` | Save notebook |
| `saveas PATH` | | Save as new file |
| `stats` | | Show statistics |
| `help` | `h` | Show help |
| `exit` | `q` | Exit |

### Python API Reference

#### NotebookController Class

**Initialization**:
```python
NotebookController(notebook_path: str, auto_backup: bool = True)
```

**Navigation Methods**:
- `jump_to_cell(index: int) -> bool`
- `next_cell() -> bool`
- `prev_cell() -> bool`
- `first_cell()`
- `last_cell()`

**Viewing Methods**:
- `view_cell(index: int = None, show_output: bool = True) -> Dict`
- `list_all_cells(show_content: bool = False)`
- `search_cells(pattern: str, regex: bool = False, cell_type: str = None)`
- `get_cell_count() -> int`
- `get_stats()`

**Editing Methods**:
- `edit_cell(content: str, index: int = None, cell_type: str = None)`
- `insert_cell(content: str, cell_type: str = 'code', index: int = None, position: str = 'after')`
- `delete_cell(index: int = None) -> bool`
- `duplicate_cell(index: int = None) -> bool`
- `clear_cell(index: int = None) -> bool`
- `append_to_cell(content: str, index: int = None)`

**Execution Methods**:
- `execute_cell(index: int = None, timeout: int = 60) -> Tuple[bool, str]`
- `execute_all_cells(start_index: int = 0, end_index: int = None)`
- `clear_outputs(index: int = None) -> bool`
- `clear_all_outputs()`

**History Methods**:
- `undo() -> bool`
- `redo() -> bool`
- `show_history()`

**Batch Methods**:
- `filter_cells(cell_type: str) -> List[int]`
- `replace_in_all_cells(old: str, new: str, cell_type: str = None)`
- `merge_cells(start_index: int, end_index: int, separator: str = '\n\n') -> bool`

**Save Methods**:
- `save()`
- `save_as(path: str)`
- `export_cell(index: int = None, output_file: str = None)`
- `import_from_file(file_path: str, cell_type: str = 'code', position: str = 'after')`

## 🛠️ Advanced Usage

### Custom Automation Scripts

Create your own automation scripts using the API:

```python
#!/usr/bin/env python3
"""Custom notebook automation script"""

from automation.notebook_controller.notebook_controller import NotebookController

def clean_and_execute(notebook_path, output_path):
    """Clean outputs, execute, and save."""
    # Load notebook
    nb = NotebookController(notebook_path)

    # Clear all outputs
    print("Clearing outputs...")
    nb.clear_all_outputs()

    # Execute all cells
    print("Executing cells...")
    nb.execute_all_cells()

    # Save to new file
    print(f"Saving to {output_path}...")
    nb.save_as(output_path)

    print("Done!")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: script.py input.ipynb output.ipynb")
        sys.exit(1)

    clean_and_execute(sys.argv[1], sys.argv[2])
```

### Makefile Integration

```makefile
.PHONY: clean-notebooks execute-notebooks validate-notebooks

# Clean all notebook outputs
clean-notebooks:
	@for nb in notebooks/*.ipynb; do \
		echo "Cleaning $$nb..."; \
		python automation/notebook_controller/notebook_controller.py "$$nb" --clear-outputs; \
	done

# Execute all notebooks
execute-notebooks:
	@for nb in notebooks/*.ipynb; do \
		echo "Executing $$nb..."; \
		python automation/notebook_controller/notebook_controller.py "$$nb" --execute-all; \
	done

# Validate notebooks
validate-notebooks:
	@python automation/notebook_controller/examples.py 8
```

## 🔧 Troubleshooting

### Issue: Import Error

**Problem**: `ModuleNotFoundError: No module named 'automation'`

**Solution**: Run from project root or update Python path:
```bash
# From project root
python automation/notebook_controller/notebook_controller.py notebook.ipynb

# Or add to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/path/to/project
```

### Issue: Execution Timeout

**Problem**: Cell execution times out

**Solution**: Increase timeout:
```bash
# Command line
python automation/notebook_controller/notebook_controller.py notebook.ipynb --execute-all

# Python API
nb.execute_cell(index=10, timeout=300)  # 5 minutes
```

### Issue: Backup Files

**Problem**: Too many backup files created

**Solution**: Disable auto-backup:
```python
nb = NotebookController('notebook.ipynb', auto_backup=False)

# Or manually backup when needed
nb._create_backup()
```

### Issue: Large Notebook Performance

**Problem**: Slow operations on large notebooks

**Solution**:
- Disable auto-backup for large files
- Clear outputs before operations
- Use specific cell operations instead of viewing all

## 📊 Performance Tips

1. **Disable auto-backup** for large notebooks:
   ```python
   nb = NotebookController('large.ipynb', auto_backup=False)
   ```

2. **Clear outputs** before processing:
   ```python
   nb.clear_all_outputs()
   ```

3. **Use batch operations** instead of loops:
   ```python
   # Good
   nb.replace_in_all_cells('old', 'new')

   # Avoid
   for i in range(nb.get_cell_count()):
       nb.edit_cell(...)  # Creates undo state each time
   ```

4. **Limit history** for long-running scripts:
   ```python
   nb.max_history = 10  # Default is 50
   ```

## 🧪 Testing

Run the test suite:

```bash
# Test basic functionality
python automation/notebook_controller/notebook_controller.py \
    notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb --stats

# Run all examples
python automation/notebook_controller/examples.py all

# Run demo
bash automation/notebook_controller/demo.sh
```

## 📦 Project Context

These automation scripts are part of the **Ames Housing Price Prediction** project, created to manage and automate Jupyter notebook workflows for machine learning analysis.

**Project**: Advanced Apex Project - Real Estate Price Modeling
**Institution**: BITS Pilani
**Dataset**: Ames Housing Dataset (2,930 properties, 82 features)

## 📄 License

Part of the Ames Housing Price Prediction project.

## 🤝 Contributing

To add new automation scripts:

1. Create script in appropriate subdirectory
2. Add documentation to this README
3. Add examples to `examples.py`
4. Test thoroughly
5. Update API reference

## 📞 Support

For issues or questions:
- Check documentation in `automation/docs/`
- Run interactive demo: `bash automation/notebook_controller/demo.sh`
- View examples: `python automation/notebook_controller/examples.py`

## 🎓 Additional Resources

- **Quick Start**: `automation/docs/QUICK_START.md`
- **API Reference**: `automation/docs/API_REFERENCE.md`
- **Examples**: `automation/docs/EXAMPLES.md`
- **Original Docs**: `docs/NOTEBOOK_CONTROLLER_GUIDE.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-11-15
**Author**: Automation Engineering Team
