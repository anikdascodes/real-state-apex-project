# Automation Scripts - Quick Start Guide

Get started with notebook automation in 5 minutes.

## Installation

```bash
# Ensure Jupyter is installed
pip install jupyter nbconvert

# Or with uv (recommended for this project)
uv pip install jupyter nbconvert
```

## Three Ways to Use

### 1. Command Line (Quick Tasks)

```bash
# Show notebook statistics
python automation/notebook_controller/notebook_controller.py notebook.ipynb --stats

# View cell 5
python automation/notebook_controller/notebook_controller.py notebook.ipynb --view 5

# Search for text
python automation/notebook_controller/notebook_controller.py notebook.ipynb --search "pandas"

# Execute all cells
python automation/notebook_controller/notebook_controller.py notebook.ipynb --execute-all

# Clear all outputs
python automation/notebook_controller/notebook_controller.py notebook.ipynb --clear-outputs

# List all cells
python automation/notebook_controller/notebook_controller.py notebook.ipynb --list
```

### 2. Interactive Mode (Exploration)

```bash
python automation/notebook_controller/notebook_controller.py notebook.ipynb
```

Then use commands:
```
[Cell 0] > list          # List all cells
[Cell 0] > view 5        # View cell 5
[Cell 0] > jump 10       # Jump to cell 10
[Cell 0] > run           # Execute current cell
[Cell 0] > save          # Save changes
[Cell 0] > help          # Show all commands
[Cell 0] > exit          # Quit
```

### 3. Python API (Automation)

```python
from automation.notebook_controller.notebook_controller import NotebookController

# Load notebook
nb = NotebookController('notebook.ipynb')

# Navigate and view
nb.jump_to_cell(5)
nb.view_cell()

# Edit
nb.edit_cell("print('Hello')", index=5)

# Execute
nb.execute_cell(5)

# Save
nb.save()
```

## Common Tasks

### Clean Before Git Commit
```bash
python automation/notebook_controller/notebook_controller.py notebook.ipynb --clear-outputs
```

### Execute Notebook
```bash
python automation/notebook_execution/execute_notebook.py input.ipynb output.ipynb
```

### Search and Replace
```python
from automation.notebook_controller.notebook_controller import NotebookController

nb = NotebookController('notebook.ipynb')
nb.replace_in_all_cells('old_text', 'new_text')
nb.save()
```

### Validate Notebook
```bash
python automation/notebook_controller/examples.py 8
```

## Interactive Commands

| Command | Description |
|---------|-------------|
| `list` | List all cells |
| `view [N]` | View cell |
| `jump N` | Jump to cell N |
| `next` | Next cell |
| `prev` | Previous cell |
| `edit` | Edit current cell |
| `run` | Execute cell |
| `runall` | Execute all |
| `search TEXT` | Find text |
| `undo` | Undo change |
| `save` | Save notebook |
| `help` | Show help |
| `exit` | Quit |

## Examples

```bash
# Run example 1 (Basic Navigation)
python automation/notebook_controller/examples.py 1

# Run all examples
python automation/notebook_controller/examples.py all

# Run demo
bash automation/notebook_controller/demo.sh
```

## Need More Help?

- Full documentation: `automation/README.md`
- API reference: `automation/docs/API_REFERENCE.md`
- Examples: `automation/docs/EXAMPLES.md`
