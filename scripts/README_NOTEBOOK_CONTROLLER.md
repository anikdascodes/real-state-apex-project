# Notebook Controller

Professional Jupyter Notebook Automation Tool

## Features

✅ **Complete Control** - View, edit, execute, navigate any notebook
✅ **Interactive CLI** - User-friendly command-line interface
✅ **Python API** - Programmatic automation capabilities
✅ **Undo/Redo** - 50-level history with rollback
✅ **Safe Operations** - Auto-backup before modifications
✅ **Batch Processing** - Search, replace, merge, filter cells
✅ **Cell Execution** - Run individual cells or entire notebooks
✅ **Zero Dependencies** - Only requires Jupyter (already installed)

## Quick Start

### Interactive Mode
```bash
python scripts/notebook_controller.py notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb
```

### Command Line
```bash
# View statistics
python scripts/notebook_controller.py notebook.ipynb --stats

# Search for text
python scripts/notebook_controller.py notebook.ipynb --search "pandas"

# Execute all cells
python scripts/notebook_controller.py notebook.ipynb --execute-all

# Clear outputs
python scripts/notebook_controller.py notebook.ipynb --clear-outputs
```

### Python API
```python
from scripts.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb')
nb.jump_to_cell(5)
nb.view_cell()
nb.execute_cell()
nb.save()
```

## Documentation

- **Quick Start**: `docs/NOTEBOOK_CONTROLLER_QUICKSTART.md`
- **Complete Guide**: `docs/NOTEBOOK_CONTROLLER_GUIDE.md`
- **Examples**: `python scripts/notebook_automation_examples.py`

## Common Use Cases

### 1. Clean Notebook for Git
```bash
python scripts/notebook_controller.py notebook.ipynb --clear-outputs
```

### 2. Execute and Save
```bash
python scripts/notebook_controller.py notebook.ipynb --execute-all
```

### 3. Find and Replace
```python
from scripts.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb')
nb.replace_in_all_cells('old_text', 'new_text')
nb.save()
```

### 4. Validate Notebook
```python
from scripts.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb', auto_backup=False)

# Check for errors
for i in nb.filter_cells('code'):
    cell = nb.view_cell(i, show_output=False)
    outputs = cell.get('outputs', [])
    for output in outputs:
        if output.get('output_type') == 'error':
            print(f"Error in cell {i}")
```

### 5. Extract Code
```python
from scripts.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb')
nb.export_cell(index=10, output_file='extracted.py')
```

## Architecture

```
NotebookController
├── Core Operations
│   ├── _load_notebook()
│   ├── _save_notebook()
│   └── _create_backup()
├── Navigation
│   ├── jump_to_cell()
│   ├── next_cell()
│   └── prev_cell()
├── Viewing
│   ├── view_cell()
│   ├── list_all_cells()
│   └── search_cells()
├── Editing
│   ├── edit_cell()
│   ├── insert_cell()
│   └── delete_cell()
├── Execution
│   ├── execute_cell()
│   └── execute_all_cells()
├── History
│   ├── undo()
│   ├── redo()
│   └── show_history()
└── Batch Operations
    ├── filter_cells()
    ├── replace_in_all_cells()
    └── merge_cells()
```

## API Reference

### Core Methods

| Method | Description |
|--------|-------------|
| `NotebookController(path, auto_backup=True)` | Initialize controller |
| `save()` | Save to original file |
| `save_as(path)` | Save to new file |

### Navigation Methods

| Method | Description |
|--------|-------------|
| `jump_to_cell(index)` | Jump to specific cell |
| `next_cell()` | Move to next cell |
| `prev_cell()` | Move to previous cell |
| `first_cell()` | Jump to first cell |
| `last_cell()` | Jump to last cell |

### Viewing Methods

| Method | Description |
|--------|-------------|
| `view_cell(index, show_output=True)` | View cell content |
| `list_all_cells(show_content=False)` | List all cells |
| `search_cells(pattern, regex=False, cell_type=None)` | Search cells |
| `get_cell_count()` | Get total cells |
| `get_stats()` | Show statistics |

### Editing Methods

| Method | Description |
|--------|-------------|
| `edit_cell(content, index, cell_type)` | Edit cell |
| `insert_cell(content, cell_type, index, position)` | Insert cell |
| `delete_cell(index)` | Delete cell |
| `duplicate_cell(index)` | Duplicate cell |
| `clear_cell(index)` | Clear content |

### Execution Methods

| Method | Description |
|--------|-------------|
| `execute_cell(index, timeout=60)` | Execute cell |
| `execute_all_cells(start, end)` | Execute range |
| `clear_outputs(index)` | Clear output |
| `clear_all_outputs()` | Clear all outputs |

### History Methods

| Method | Description |
|--------|-------------|
| `undo()` | Undo last change |
| `redo()` | Redo last undo |
| `show_history()` | Show history |

### Batch Methods

| Method | Description |
|--------|-------------|
| `filter_cells(cell_type)` | Get cells by type |
| `replace_in_all_cells(old, new, cell_type)` | Replace text |
| `merge_cells(start, end, separator)` | Merge cells |

## Examples

Run practical examples:
```bash
python scripts/notebook_automation_examples.py <1-8|all>
```

1. Basic Navigation and Viewing
2. Search and Analyze
3. Cell Manipulation
4. Undo/Redo Functionality
5. Batch Operations
6. Output Management
7. Export and Import
8. Notebook Validation

## Testing

```bash
# Test basic functionality
python scripts/notebook_controller.py notebook.ipynb --stats

# Test viewing
python scripts/notebook_controller.py notebook.ipynb --view 0

# Test search
python scripts/notebook_controller.py notebook.ipynb --search "import"

# Test examples
python scripts/notebook_automation_examples.py 1
```

## Requirements

- Python 3.7+
- Jupyter (`pip install jupyter nbconvert`)
- No other dependencies!

## License

Part of the Ames Housing Price Prediction project.

## Author

Automation Engineering Team

## Version

1.0.0 - Initial Release

---

For complete documentation, see `docs/NOTEBOOK_CONTROLLER_GUIDE.md`
