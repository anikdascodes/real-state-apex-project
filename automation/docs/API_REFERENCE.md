# Automation Scripts - API Reference

Complete API documentation for all automation modules.

## NotebookController Class

### Import

```python
from automation.notebook_controller.notebook_controller import NotebookController
```

### Initialization

```python
NotebookController(notebook_path: str, auto_backup: bool = True)
```

**Parameters**:
- `notebook_path` (str): Path to .ipynb file
- `auto_backup` (bool): Create backup before modifications (default: True)

**Example**:
```python
nb = NotebookController('analysis.ipynb')
nb_no_backup = NotebookController('analysis.ipynb', auto_backup=False)
```

## Navigation Methods

### jump_to_cell(index: int) -> bool

Jump to a specific cell by index.

**Parameters**:
- `index` (int): Cell index (0-based, negative for reverse indexing)

**Returns**: bool - True if successful

**Example**:
```python
nb.jump_to_cell(5)    # Jump to cell 5
nb.jump_to_cell(-1)   # Jump to last cell
nb.jump_to_cell(-5)   # Jump to 5th cell from end
```

### next_cell() -> bool

Move to the next cell.

**Returns**: bool - True if successful

**Example**:
```python
nb.next_cell()
```

### prev_cell() -> bool

Move to the previous cell.

**Returns**: bool - True if successful

**Example**:
```python
nb.prev_cell()
```

### first_cell()

Jump to the first cell.

**Example**:
```python
nb.first_cell()
```

### last_cell()

Jump to the last cell.

**Example**:
```python
nb.last_cell()
```

## Viewing Methods

### view_cell(index: Optional[int] = None, show_output: bool = True) -> Dict

View a cell's content.

**Parameters**:
- `index` (int, optional): Cell index (uses current if None)
- `show_output` (bool): Print cell content (default: True)

**Returns**: Dict - Cell dictionary

**Example**:
```python
# View current cell
cell = nb.view_cell()

# View cell 10 without printing
cell = nb.view_cell(index=10, show_output=False)

# Access cell data
source = ''.join(cell.get('source', []))
cell_type = cell['cell_type']
outputs = cell.get('outputs', [])
```

### list_all_cells(show_content: bool = False)

List all cells in the notebook.

**Parameters**:
- `show_content` (bool): Show first 100 chars of each cell (default: False)

**Example**:
```python
# List with summary
nb.list_all_cells()

# List with content preview
nb.list_all_cells(show_content=True)
```

### search_cells(pattern: str, regex: bool = False, cell_type: Optional[str] = None)

Search for pattern in cells.

**Parameters**:
- `pattern` (str): Search pattern
- `regex` (bool): Use regex matching (default: False)
- `cell_type` (str, optional): Filter by 'code' or 'markdown'

**Returns**: List of (index, source) tuples

**Example**:
```python
# Simple search
matches = nb.search_cells('import pandas')

# Regex search
matches = nb.search_cells(r'def \w+\(', regex=True)

# Search only code cells
matches = nb.search_cells('import', cell_type='code')
```

### get_cell_count() -> int

Get total number of cells.

**Returns**: int - Total cells

**Example**:
```python
total = nb.get_cell_count()
print(f"Notebook has {total} cells")
```

### get_stats()

Show notebook statistics.

**Example**:
```python
nb.get_stats()
```

## Editing Methods

### edit_cell(content: str, index: Optional[int] = None, cell_type: Optional[str] = None)

Edit a cell's content.

**Parameters**:
- `content` (str): New content
- `index` (int, optional): Cell index (uses current if None)
- `cell_type` (str, optional): Change to 'code' or 'markdown'

**Example**:
```python
# Edit current cell
nb.edit_cell("print('Hello World')")

# Edit cell 5
nb.edit_cell("print('Hello')", index=5)

# Edit and change type
nb.edit_cell("# Header", index=5, cell_type='markdown')
```

### insert_cell(content: str, cell_type: str = 'code', index: Optional[int] = None, position: str = 'after')

Insert a new cell.

**Parameters**:
- `content` (str): Cell content
- `cell_type` (str): 'code' or 'markdown' (default: 'code')
- `index` (int, optional): Position reference (uses current if None)
- `position` (str): 'before', 'after', or 'replace' (default: 'after')

**Example**:
```python
# Insert code cell after current
nb.insert_cell("print('test')")

# Insert markdown before cell 5
nb.insert_cell("# Title", cell_type='markdown', index=5, position='before')

# Replace cell 10
nb.insert_cell("new content", index=10, position='replace')
```

### delete_cell(index: Optional[int] = None) -> bool

Delete a cell.

**Parameters**:
- `index` (int, optional): Cell index (uses current if None)

**Returns**: bool - True if successful

**Example**:
```python
# Delete current cell
nb.delete_cell()

# Delete cell 10
nb.delete_cell(10)
```

### duplicate_cell(index: Optional[int] = None) -> bool

Duplicate a cell.

**Parameters**:
- `index` (int, optional): Cell index (uses current if None)

**Returns**: bool - True if successful

**Example**:
```python
# Duplicate current cell
nb.duplicate_cell()

# Duplicate cell 5
nb.duplicate_cell(5)
```

### clear_cell(index: Optional[int] = None) -> bool

Clear a cell's content.

**Parameters**:
- `index` (int, optional): Cell index (uses current if None)

**Returns**: bool - True if successful

**Example**:
```python
nb.clear_cell()       # Clear current
nb.clear_cell(10)     # Clear cell 10
```

### append_to_cell(content: str, index: Optional[int] = None)

Append content to a cell.

**Parameters**:
- `content` (str): Content to append
- `index` (int, optional): Cell index (uses current if None)

**Example**:
```python
nb.append_to_cell("\nprint('additional code')")
```

## Execution Methods

### execute_cell(index: Optional[int] = None, timeout: int = 60) -> Tuple[bool, str]

Execute a code cell and capture output.

**Parameters**:
- `index` (int, optional): Cell index (uses current if None)
- `timeout` (int): Execution timeout in seconds (default: 60)

**Returns**: Tuple[bool, str] - (success, message)

**Example**:
```python
# Execute current cell
success, msg = nb.execute_cell()

# Execute cell 5 with 5-minute timeout
success, msg = nb.execute_cell(index=5, timeout=300)

if not success:
    print(f"Execution failed: {msg}")
```

### execute_all_cells(start_index: int = 0, end_index: Optional[int] = None)

Execute all cells in range.

**Parameters**:
- `start_index` (int): Start from this cell (default: 0)
- `end_index` (int, optional): End at this cell (inclusive, None = last)

**Example**:
```python
# Execute all cells
nb.execute_all_cells()

# Execute cells 0-20
nb.execute_all_cells(start_index=0, end_index=20)

# Execute from cell 10 to end
nb.execute_all_cells(start_index=10)
```

### clear_outputs(index: Optional[int] = None) -> bool

Clear outputs from a code cell.

**Parameters**:
- `index` (int, optional): Cell index (uses current if None)

**Returns**: bool - True if successful

**Example**:
```python
nb.clear_outputs()      # Clear current cell
nb.clear_outputs(10)    # Clear cell 10
```

### clear_all_outputs()

Clear all outputs from all code cells.

**Example**:
```python
nb.clear_all_outputs()
```

## History Methods

### undo() -> bool

Undo the last change.

**Returns**: bool - True if successful

**Example**:
```python
nb.edit_cell("new content")
nb.undo()  # Restore previous content
```

### redo() -> bool

Redo the last undone change.

**Returns**: bool - True if successful

**Example**:
```python
nb.undo()
nb.redo()  # Reapply change
```

### show_history()

Show undo/redo history.

**Example**:
```python
nb.show_history()
```

## Batch Methods

### filter_cells(cell_type: str) -> List[int]

Get indices of cells by type.

**Parameters**:
- `cell_type` (str): 'code' or 'markdown'

**Returns**: List[int] - Cell indices

**Example**:
```python
# Get all code cells
code_cells = nb.filter_cells('code')

# Get all markdown cells
markdown_cells = nb.filter_cells('markdown')

# Process all code cells
for i in code_cells:
    cell = nb.view_cell(i, show_output=False)
    # ... process cell
```

### replace_in_all_cells(old: str, new: str, cell_type: Optional[str] = None)

Replace text in all cells.

**Parameters**:
- `old` (str): Text to find
- `new` (str): Replacement text
- `cell_type` (str, optional): Filter by 'code' or 'markdown'

**Example**:
```python
# Replace in all cells
nb.replace_in_all_cells('old_name', 'new_name')

# Replace only in code cells
nb.replace_in_all_cells('import old', 'import new', cell_type='code')
```

### merge_cells(start_index: int, end_index: int, separator: str = '\n\n') -> bool

Merge multiple cells into one.

**Parameters**:
- `start_index` (int): First cell to merge
- `end_index` (int): Last cell to merge (inclusive)
- `separator` (str): Separator between cells (default: '\n\n')

**Returns**: bool - True if successful

**Example**:
```python
# Merge cells 5-10
nb.merge_cells(5, 10)

# Merge with custom separator
nb.merge_cells(5, 10, separator='\n\n---\n\n')
```

## Save Methods

### save()

Save notebook to original file.

**Example**:
```python
nb.edit_cell("new content")
nb.save()
```

### save_as(path: str)

Save notebook to a different file.

**Parameters**:
- `path` (str): New file path

**Example**:
```python
nb.save_as('analysis_modified.ipynb')
```

### export_cell(index: Optional[int] = None, output_file: Optional[str] = None)

Export cell content to a file.

**Parameters**:
- `index` (int, optional): Cell index (uses current if None)
- `output_file` (str, optional): Output file path

**Returns**: str - Cell content if output_file is None

**Example**:
```python
# Export cell 10 to file
nb.export_cell(index=10, output_file='cell_10.py')

# Get cell content
content = nb.export_cell(index=10)
```

### import_from_file(file_path: str, cell_type: str = 'code', position: str = 'after')

Import content from file as a new cell.

**Parameters**:
- `file_path` (str): File to import
- `cell_type` (str): 'code' or 'markdown' (default: 'code')
- `position` (str): 'before' or 'after' (default: 'after')

**Example**:
```python
nb.import_from_file('script.py', cell_type='code', position='after')
```

## Notebook Execution Module

### Import

```python
from automation.notebook_execution.execute_notebook import execute_notebook_cells
```

### execute_notebook_cells(notebook_path: str, output_path: str, timeout: int = 600)

Execute a notebook and save with outputs.

**Parameters**:
- `notebook_path` (str): Input notebook path
- `output_path` (str): Output notebook path
- `timeout` (int): Timeout in seconds (default: 600)

**Example**:
```python
from automation.notebook_execution.execute_notebook import execute_notebook_cells

# Execute notebook
execute_notebook_cells('input.ipynb', 'output.ipynb')

# With custom timeout
execute_notebook_cells('input.ipynb', 'output.ipynb', timeout=300)
```

## Error Handling

All methods handle errors gracefully and print error messages:

```python
try:
    nb = NotebookController('notebook.ipynb')
    nb.execute_cell(5)
except FileNotFoundError:
    print("Notebook not found")
except Exception as e:
    print(f"Error: {e}")
```

## Type Hints

The module uses type hints for better IDE support:

```python
from typing import Dict, List, Optional, Tuple

def view_cell(self, index: Optional[int] = None, show_output: bool = True) -> Dict:
    ...

def execute_cell(self, index: Optional[int] = None, timeout: int = 60) -> Tuple[bool, str]:
    ...
```

## Constants

```python
# Default values
MAX_HISTORY = 50        # Maximum undo states
DEFAULT_TIMEOUT = 60    # Cell execution timeout (seconds)
```

## Attributes

```python
nb = NotebookController('notebook.ipynb')

# Public attributes
nb.notebook_path        # Path to notebook
nb.notebook            # Notebook dictionary
nb.current_cell_index  # Current cell position
nb.auto_backup         # Auto-backup enabled

# Modify settings
nb.max_history = 100   # Change history limit
```
