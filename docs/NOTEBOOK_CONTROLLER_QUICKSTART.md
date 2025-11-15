# Notebook Controller - Quick Start Guide

## What is it?

A powerful automation tool for complete control over Jupyter notebooks (.ipynb files).

## Installation

```bash
# Already included in the project!
# Just ensure Jupyter is installed:
pip install jupyter nbconvert
```

## 3 Ways to Use

### 1. Interactive CLI (Easiest)

```bash
python scripts/notebook_controller.py notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb
```

Then use commands like:
- `list` - See all cells
- `view 5` - View cell 5
- `jump 10` - Go to cell 10
- `run` - Execute current cell
- `help` - Show all commands
- `exit` - Quit

### 2. Command Line (Quick Tasks)

```bash
# View cell 5
python scripts/notebook_controller.py notebook.ipynb --view 5

# List all cells
python scripts/notebook_controller.py notebook.ipynb --list

# Execute all cells
python scripts/notebook_controller.py notebook.ipynb --execute-all

# Search for text
python scripts/notebook_controller.py notebook.ipynb --search "pandas"

# Show stats
python scripts/notebook_controller.py notebook.ipynb --stats

# Clear outputs
python scripts/notebook_controller.py notebook.ipynb --clear-outputs
```

### 3. Python API (Automation Scripts)

```python
from scripts.notebook_controller import NotebookController

# Load notebook
nb = NotebookController('notebook.ipynb')

# Navigate
nb.jump_to_cell(5)
nb.next_cell()
nb.prev_cell()

# View
nb.view_cell()
nb.list_all_cells()
nb.search_cells('pandas')

# Edit
nb.edit_cell("print('Hello')", index=5)
nb.insert_cell("# New cell", cell_type='markdown')
nb.delete_cell(10)

# Execute
nb.execute_cell(5)
nb.execute_all_cells()

# Undo/Redo
nb.undo()
nb.redo()

# Save
nb.save()
```

## Common Tasks

### Task 1: Clean All Outputs

```bash
python scripts/notebook_controller.py notebook.ipynb --clear-outputs
```

### Task 2: Execute Notebook

```bash
python scripts/notebook_controller.py notebook.ipynb --execute-all
```

### Task 3: Find Text in Cells

```bash
python scripts/notebook_controller.py notebook.ipynb --search "import pandas"
```

### Task 4: View Specific Cell

```bash
python scripts/notebook_controller.py notebook.ipynb --view 15
```

### Task 5: Interactive Editing

```bash
# Start interactive mode
python scripts/notebook_controller.py notebook.ipynb

# Then use commands:
[Cell 0] > jump 10
[Cell 10] > view
[Cell 10] > edit
# (Type new content, press Ctrl+D when done)
[Cell 10] > save
[Cell 10] > exit
```

## Examples

See practical examples:
```bash
# Run example 1 (Basic Navigation)
python scripts/notebook_automation_examples.py 1

# Run example 2 (Search and Analyze)
python scripts/notebook_automation_examples.py 2

# Run all examples
python scripts/notebook_automation_examples.py all
```

## Interactive Mode Commands

| Command | Short | Description |
|---------|-------|-------------|
| `next` | `n` | Next cell |
| `prev` | `p` | Previous cell |
| `jump <n>` | `j <n>` | Jump to cell n |
| `first` | | First cell |
| `last` | | Last cell |
| `view [n]` | `v [n]` | View cell |
| `list` | `ls` | List all cells |
| `search <text>` | | Search cells |
| `edit` | `e` | Edit current cell |
| `delete [n]` | `del [n]` | Delete cell |
| `insert [type]` | | Insert cell |
| `run [n]` | `r [n]` | Execute cell |
| `runall` | | Execute all |
| `undo` | `u` | Undo change |
| `redo` | | Redo change |
| `save` | `s` | Save notebook |
| `stats` | | Show statistics |
| `help` | `h` | Show help |
| `exit` | `q` | Quit |

## Safety Features

- **Auto Backup**: Creates timestamped backup before saving
- **Undo/Redo**: 50 levels of undo history
- **No Data Loss**: All changes tracked

## Need Help?

```bash
# Show all options
python scripts/notebook_controller.py --help

# Interactive mode help
python scripts/notebook_controller.py notebook.ipynb
[Cell 0] > help

# Read full guide
cat docs/NOTEBOOK_CONTROLLER_GUIDE.md
```

## Quick Reference Card

### Navigation
```
jump 10     # Go to cell 10
next        # Next cell
prev        # Previous cell
first       # First cell
last        # Last cell
```

### Viewing
```
view        # View current cell
view 5      # View cell 5
list        # List all cells
list -c     # List with content
search text # Find 'text'
```

### Editing
```
edit        # Edit current
delete      # Delete current
insert code # New code cell
dup         # Duplicate current
```

### Execution
```
run         # Execute current
run 5       # Execute cell 5
runall      # Execute all
```

### Management
```
undo        # Undo last
redo        # Redo last
save        # Save file
stats       # Show stats
```

## Pro Tips

1. **Always use interactive mode** when exploring notebooks
2. **Use `--stats`** to quickly understand notebook structure
3. **Use `--search`** to find specific code or text
4. **Clear outputs** before committing to git
5. **Use undo** liberally - it's there to help!

## Full Documentation

- Complete Guide: `docs/NOTEBOOK_CONTROLLER_GUIDE.md`
- Examples: `python scripts/notebook_automation_examples.py`
- Help: `python scripts/notebook_controller.py --help`
