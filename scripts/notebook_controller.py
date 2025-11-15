#!/usr/bin/env python3
"""
Notebook Controller - Professional Jupyter Notebook Automation Tool
=====================================================================

A comprehensive automation script for complete control over Jupyter notebooks.

Features:
- View, edit, delete cells (code/markdown)
- Execute cells and capture outputs
- Navigate between cells (jump, next, prev)
- Undo/redo functionality with full history
- Batch operations
- Cell insertion at any position
- Export and backup capabilities
- Interactive CLI mode

Author: Automation Engineering Team
Version: 1.0.0
"""

import json
import copy
import subprocess
import sys
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re


class NotebookController:
    """
    Main controller class for Jupyter notebook automation.

    Provides full control over notebook files including viewing, editing,
    executing, and managing cells with undo/redo capabilities.
    """

    def __init__(self, notebook_path: str, auto_backup: bool = True):
        """
        Initialize the notebook controller.

        Args:
            notebook_path: Path to the .ipynb file
            auto_backup: Automatically create backup before modifications
        """
        self.notebook_path = Path(notebook_path)
        self.auto_backup = auto_backup
        self.notebook = None
        self.current_cell_index = 0
        self.history = []  # For undo/redo
        self.history_position = -1
        self.max_history = 50

        if not self.notebook_path.exists():
            raise FileNotFoundError(f"Notebook not found: {notebook_path}")

        self._load_notebook()
        self._save_state()  # Initial state for undo

    # ==================== CORE OPERATIONS ====================

    def _load_notebook(self):
        """Load the notebook from file."""
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
        print(f"✅ Loaded notebook: {self.notebook_path.name}")
        print(f"   Cells: {len(self.notebook['cells'])}")

    def _save_notebook(self, path: Optional[Path] = None):
        """Save the notebook to file."""
        save_path = path or self.notebook_path

        if self.auto_backup and path is None:
            self._create_backup()

        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.notebook, f, indent=1, ensure_ascii=False)

        print(f"💾 Saved notebook: {save_path.name}")

    def _create_backup(self):
        """Create a timestamped backup of the notebook."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"{self.notebook_path.stem}_backup_{timestamp}.ipynb"
        backup_path = self.notebook_path.parent / backup_name

        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(self.notebook, f, indent=1, ensure_ascii=False)

        print(f"📦 Backup created: {backup_name}")

    def _save_state(self):
        """Save current state for undo functionality."""
        # Remove any states after current position
        self.history = self.history[:self.history_position + 1]

        # Add current state
        state = copy.deepcopy(self.notebook)
        self.history.append({
            'notebook': state,
            'cell_index': self.current_cell_index,
            'timestamp': datetime.now()
        })

        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_position += 1

    # ==================== CELL NAVIGATION ====================

    def get_cell_count(self) -> int:
        """Get total number of cells."""
        return len(self.notebook['cells'])

    def jump_to_cell(self, index: int) -> bool:
        """
        Jump to a specific cell by index.

        Args:
            index: Cell index (0-based or negative for reverse indexing)

        Returns:
            True if successful, False otherwise
        """
        cell_count = self.get_cell_count()

        # Handle negative indexing
        if index < 0:
            index = cell_count + index

        if 0 <= index < cell_count:
            self.current_cell_index = index
            print(f"📍 Jumped to cell {index}")
            return True
        else:
            print(f"❌ Invalid cell index: {index} (total cells: {cell_count})")
            return False

    def next_cell(self) -> bool:
        """Move to next cell."""
        if self.current_cell_index < self.get_cell_count() - 1:
            self.current_cell_index += 1
            print(f"➡️  Moved to cell {self.current_cell_index}")
            return True
        else:
            print("❌ Already at last cell")
            return False

    def prev_cell(self) -> bool:
        """Move to previous cell."""
        if self.current_cell_index > 0:
            self.current_cell_index -= 1
            print(f"⬅️  Moved to cell {self.current_cell_index}")
            return True
        else:
            print("❌ Already at first cell")
            return False

    def first_cell(self):
        """Jump to first cell."""
        self.current_cell_index = 0
        print("⏮️  Moved to first cell")

    def last_cell(self):
        """Jump to last cell."""
        self.current_cell_index = self.get_cell_count() - 1
        print("⏭️  Moved to last cell")

    # ==================== CELL VIEWING ====================

    def view_cell(self, index: Optional[int] = None, show_output: bool = True) -> Dict:
        """
        View a cell's content.

        Args:
            index: Cell index (uses current if None)
            show_output: Print the cell content

        Returns:
            Cell dictionary
        """
        if index is None:
            index = self.current_cell_index

        if not (0 <= index < self.get_cell_count()):
            print(f"❌ Invalid cell index: {index}")
            return {}

        cell = self.notebook['cells'][index]

        if show_output:
            self._print_cell(cell, index)

        return cell

    def _print_cell(self, cell: Dict, index: int):
        """Pretty print a cell."""
        cell_type = cell['cell_type']
        source = ''.join(cell.get('source', []))

        print(f"\n{'='*70}")
        print(f"Cell {index} | Type: {cell_type.upper()}")
        print(f"{'='*70}")
        print(source)

        # Show outputs for code cells
        if cell_type == 'code' and 'outputs' in cell:
            outputs = cell['outputs']
            if outputs:
                print(f"\n{'-'*70}")
                print("OUTPUTS:")
                print(f"{'-'*70}")
                for i, output in enumerate(outputs):
                    self._print_output(output, i)

        print(f"{'='*70}\n")

    def _print_output(self, output: Dict, index: int):
        """Print a cell output."""
        output_type = output.get('output_type', 'unknown')

        if output_type == 'stream':
            text = ''.join(output.get('text', []))
            print(f"[Stream {index}]:\n{text}")

        elif output_type == 'execute_result' or output_type == 'display_data':
            data = output.get('data', {})
            if 'text/plain' in data:
                text = ''.join(data['text/plain'])
                print(f"[Result {index}]:\n{text}")
            if 'image/png' in data:
                print(f"[Image {index}]: <PNG image data>")

        elif output_type == 'error':
            ename = output.get('ename', 'Error')
            evalue = output.get('evalue', '')
            print(f"[Error {index}]: {ename}: {evalue}")

    def list_all_cells(self, show_content: bool = False):
        """
        List all cells in the notebook.

        Args:
            show_content: Show first 100 chars of each cell
        """
        print(f"\n📓 Notebook: {self.notebook_path.name}")
        print(f"Total cells: {self.get_cell_count()}\n")

        for i, cell in enumerate(self.notebook['cells']):
            cell_type = cell['cell_type']
            source = ''.join(cell.get('source', []))

            marker = "👉" if i == self.current_cell_index else "  "
            print(f"{marker} Cell {i:3d} | {cell_type:8s} |", end="")

            if show_content:
                preview = source[:100].replace('\n', ' ')
                if len(source) > 100:
                    preview += "..."
                print(f" {preview}")
            else:
                lines = len(source.split('\n'))
                print(f" {lines} lines")

    def search_cells(self, pattern: str, regex: bool = False, cell_type: Optional[str] = None):
        """
        Search for pattern in cells.

        Args:
            pattern: Search pattern
            regex: Use regex matching
            cell_type: Filter by cell type ('code' or 'markdown')
        """
        print(f"\n🔍 Searching for: '{pattern}'")
        if cell_type:
            print(f"   Filter: {cell_type} cells only")

        matches = []
        for i, cell in enumerate(self.notebook['cells']):
            if cell_type and cell['cell_type'] != cell_type:
                continue

            source = ''.join(cell.get('source', []))

            if regex:
                if re.search(pattern, source, re.IGNORECASE):
                    matches.append((i, source))
            else:
                if pattern.lower() in source.lower():
                    matches.append((i, source))

        print(f"\n✅ Found {len(matches)} matches\n")

        for i, source in matches:
            cell_type = self.notebook['cells'][i]['cell_type']
            lines = source.split('\n')

            # Find matching lines
            matching_lines = []
            for line_num, line in enumerate(lines, 1):
                if regex:
                    if re.search(pattern, line, re.IGNORECASE):
                        matching_lines.append((line_num, line))
                else:
                    if pattern.lower() in line.lower():
                        matching_lines.append((line_num, line))

            print(f"Cell {i} ({cell_type}):")
            for line_num, line in matching_lines:
                print(f"  Line {line_num}: {line.strip()}")
            print()

        return matches

    # ==================== CELL EDITING ====================

    def edit_cell(self, content: str, index: Optional[int] = None, cell_type: Optional[str] = None):
        """
        Edit a cell's content.

        Args:
            content: New content (string or list of strings)
            index: Cell index (uses current if None)
            cell_type: Change cell type ('code' or 'markdown')
        """
        if index is None:
            index = self.current_cell_index

        if not (0 <= index < self.get_cell_count()):
            print(f"❌ Invalid cell index: {index}")
            return False

        self._save_state()

        cell = self.notebook['cells'][index]

        # Update content
        if isinstance(content, str):
            cell['source'] = content.split('\n')
            # Keep newlines except for last line
            cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
        else:
            cell['source'] = content

        # Update cell type if specified
        if cell_type:
            if cell_type not in ['code', 'markdown']:
                print(f"❌ Invalid cell type: {cell_type}")
                return False

            old_type = cell['cell_type']
            cell['cell_type'] = cell_type

            # Update metadata based on type
            if cell_type == 'code':
                if 'execution_count' not in cell:
                    cell['execution_count'] = None
                if 'outputs' not in cell:
                    cell['outputs'] = []
            else:
                # Remove code-specific fields from markdown
                cell.pop('execution_count', None)
                cell.pop('outputs', None)

            print(f"✏️  Changed cell {index} type: {old_type} → {cell_type}")

        print(f"✏️  Edited cell {index}")
        return True

    def append_to_cell(self, content: str, index: Optional[int] = None):
        """Append content to a cell."""
        if index is None:
            index = self.current_cell_index

        cell = self.notebook['cells'][index]
        current_source = ''.join(cell.get('source', []))
        new_source = current_source + '\n' + content

        return self.edit_cell(new_source, index)

    def clear_cell(self, index: Optional[int] = None):
        """Clear a cell's content."""
        if index is None:
            index = self.current_cell_index

        return self.edit_cell("", index)

    def clear_outputs(self, index: Optional[int] = None):
        """Clear outputs from a code cell."""
        if index is None:
            index = self.current_cell_index

        if not (0 <= index < self.get_cell_count()):
            print(f"❌ Invalid cell index: {index}")
            return False

        cell = self.notebook['cells'][index]

        if cell['cell_type'] != 'code':
            print(f"❌ Cell {index} is not a code cell")
            return False

        self._save_state()

        cell['outputs'] = []
        cell['execution_count'] = None

        print(f"🧹 Cleared outputs from cell {index}")
        return True

    def clear_all_outputs(self):
        """Clear all outputs from all code cells."""
        self._save_state()

        count = 0
        for cell in self.notebook['cells']:
            if cell['cell_type'] == 'code':
                cell['outputs'] = []
                cell['execution_count'] = None
                count += 1

        print(f"🧹 Cleared outputs from {count} code cells")

    # ==================== CELL INSERTION/DELETION ====================

    def insert_cell(self, content: str, cell_type: str = 'code',
                   index: Optional[int] = None, position: str = 'after'):
        """
        Insert a new cell.

        Args:
            content: Cell content
            cell_type: 'code' or 'markdown'
            index: Position reference (uses current if None)
            position: 'before', 'after', or 'replace'
        """
        if index is None:
            index = self.current_cell_index

        if cell_type not in ['code', 'markdown']:
            print(f"❌ Invalid cell type: {cell_type}")
            return False

        self._save_state()

        # Create new cell
        new_cell = {
            'cell_type': cell_type,
            'metadata': {},
            'source': content.split('\n') if isinstance(content, str) else content
        }

        # Add newlines to source lines
        if new_cell['source']:
            new_cell['source'] = [line + '\n' for line in new_cell['source'][:-1]] + [new_cell['source'][-1]]

        if cell_type == 'code':
            new_cell['execution_count'] = None
            new_cell['outputs'] = []

        # Insert at position
        if position == 'before':
            insert_index = index
        elif position == 'after':
            insert_index = index + 1
        elif position == 'replace':
            self.notebook['cells'][index] = new_cell
            print(f"✏️  Replaced cell {index} ({cell_type})")
            return True
        else:
            print(f"❌ Invalid position: {position}")
            return False

        self.notebook['cells'].insert(insert_index, new_cell)
        print(f"➕ Inserted {cell_type} cell at position {insert_index}")

        # Update current position
        if position == 'before' or position == 'replace':
            self.current_cell_index = insert_index
        else:
            self.current_cell_index = insert_index

        return True

    def delete_cell(self, index: Optional[int] = None):
        """Delete a cell."""
        if index is None:
            index = self.current_cell_index

        if not (0 <= index < self.get_cell_count()):
            print(f"❌ Invalid cell index: {index}")
            return False

        if self.get_cell_count() == 1:
            print("❌ Cannot delete the only cell in the notebook")
            return False

        self._save_state()

        deleted_cell = self.notebook['cells'].pop(index)
        print(f"🗑️  Deleted cell {index} ({deleted_cell['cell_type']})")

        # Adjust current position
        if self.current_cell_index >= self.get_cell_count():
            self.current_cell_index = self.get_cell_count() - 1

        return True

    def duplicate_cell(self, index: Optional[int] = None):
        """Duplicate a cell."""
        if index is None:
            index = self.current_cell_index

        cell = self.view_cell(index, show_output=False)
        if not cell:
            return False

        source = ''.join(cell.get('source', []))
        self.insert_cell(source, cell['cell_type'], index, 'after')

        return True

    # ==================== CELL EXECUTION ====================

    def execute_cell(self, index: Optional[int] = None, timeout: int = 60) -> Tuple[bool, str]:
        """
        Execute a code cell and capture output.

        Args:
            index: Cell index (uses current if None)
            timeout: Execution timeout in seconds

        Returns:
            (success, output_message)
        """
        if index is None:
            index = self.current_cell_index

        if not (0 <= index < self.get_cell_count()):
            return False, f"Invalid cell index: {index}"

        cell = self.notebook['cells'][index]

        if cell['cell_type'] != 'code':
            return False, f"Cell {index} is not a code cell"

        source = ''.join(cell.get('source', []))

        print(f"▶️  Executing cell {index}...")

        # Create temporary notebook with single cell
        temp_nb = {
            'cells': [copy.deepcopy(cell)],
            'metadata': self.notebook.get('metadata', {}),
            'nbformat': self.notebook.get('nbformat', 4),
            'nbformat_minor': self.notebook.get('nbformat_minor', 0)
        }

        # Execute using jupyter nbconvert
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as f:
            temp_path = f.name
            json.dump(temp_nb, f)

        try:
            result = subprocess.run(
                ['jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                 '--ExecutePreprocessor.timeout=' + str(timeout),
                 '--output', temp_path, temp_path],
                capture_output=True,
                text=True,
                timeout=timeout + 10
            )

            if result.returncode == 0:
                # Read executed notebook
                with open(temp_path, 'r') as f:
                    executed_nb = json.load(f)

                # Update cell with outputs
                self._save_state()
                executed_cell = executed_nb['cells'][0]
                self.notebook['cells'][index]['outputs'] = executed_cell.get('outputs', [])
                self.notebook['cells'][index]['execution_count'] = executed_cell.get('execution_count')

                print(f"✅ Cell {index} executed successfully")

                # Show outputs
                if executed_cell.get('outputs'):
                    print("\nOutputs:")
                    for i, output in enumerate(executed_cell['outputs']):
                        self._print_output(output, i)

                return True, "Execution successful"
            else:
                error_msg = result.stderr
                print(f"❌ Execution failed:\n{error_msg}")
                return False, error_msg

        except subprocess.TimeoutExpired:
            print(f"❌ Execution timed out after {timeout} seconds")
            return False, "Timeout"

        except Exception as e:
            print(f"❌ Execution error: {str(e)}")
            return False, str(e)

        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def execute_all_cells(self, start_index: int = 0, end_index: Optional[int] = None):
        """
        Execute all cells in range.

        Args:
            start_index: Start from this cell
            end_index: End at this cell (inclusive, None = end)
        """
        if end_index is None:
            end_index = self.get_cell_count() - 1

        print(f"\n▶️  Executing cells {start_index} to {end_index}...")

        success_count = 0
        fail_count = 0

        for i in range(start_index, end_index + 1):
            cell = self.notebook['cells'][i]

            if cell['cell_type'] == 'code':
                success, msg = self.execute_cell(i)
                if success:
                    success_count += 1
                else:
                    fail_count += 1
                    print(f"\n⚠️  Failed at cell {i}, stopping execution")
                    break

        print(f"\n{'='*70}")
        print(f"Execution Summary:")
        print(f"  ✅ Successful: {success_count}")
        print(f"  ❌ Failed: {fail_count}")
        print(f"{'='*70}\n")

    # ==================== UNDO/REDO ====================

    def undo(self):
        """Undo last change."""
        if self.history_position <= 0:
            print("❌ Nothing to undo")
            return False

        self.history_position -= 1
        state = self.history[self.history_position]

        self.notebook = copy.deepcopy(state['notebook'])
        self.current_cell_index = state['cell_index']

        print(f"↶  Undo successful (position {self.history_position + 1}/{len(self.history)})")
        return True

    def redo(self):
        """Redo last undone change."""
        if self.history_position >= len(self.history) - 1:
            print("❌ Nothing to redo")
            return False

        self.history_position += 1
        state = self.history[self.history_position]

        self.notebook = copy.deepcopy(state['notebook'])
        self.current_cell_index = state['cell_index']

        print(f"↷  Redo successful (position {self.history_position + 1}/{len(self.history)})")
        return True

    def show_history(self):
        """Show undo/redo history."""
        print(f"\n📜 History ({len(self.history)} states):")
        print(f"   Current position: {self.history_position + 1}\n")

        for i, state in enumerate(self.history):
            marker = "👉" if i == self.history_position else "  "
            timestamp = state['timestamp'].strftime('%H:%M:%S')
            cell_count = len(state['notebook']['cells'])
            print(f"{marker} {i+1}. {timestamp} - {cell_count} cells")

    # ==================== BATCH OPERATIONS ====================

    def filter_cells(self, cell_type: str) -> List[int]:
        """Get indices of cells by type."""
        indices = []
        for i, cell in enumerate(self.notebook['cells']):
            if cell['cell_type'] == cell_type:
                indices.append(i)
        return indices

    def replace_in_all_cells(self, old: str, new: str, cell_type: Optional[str] = None):
        """Replace text in all cells."""
        self._save_state()

        count = 0
        for i, cell in enumerate(self.notebook['cells']):
            if cell_type and cell['cell_type'] != cell_type:
                continue

            source = ''.join(cell.get('source', []))
            if old in source:
                new_source = source.replace(old, new)
                cell['source'] = new_source.split('\n')
                # Add newlines
                cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
                count += 1

        print(f"🔄 Replaced '{old}' with '{new}' in {count} cells")

    def merge_cells(self, start_index: int, end_index: int, separator: str = '\n\n'):
        """Merge multiple cells into one."""
        if not (0 <= start_index < end_index < self.get_cell_count()):
            print("❌ Invalid range")
            return False

        self._save_state()

        # Get all cell contents
        merged_content = []
        cell_type = self.notebook['cells'][start_index]['cell_type']

        for i in range(start_index, end_index + 1):
            cell = self.notebook['cells'][i]
            source = ''.join(cell.get('source', []))
            merged_content.append(source)

        # Create merged cell
        merged_text = separator.join(merged_content)

        # Delete cells from end to start (to maintain indices)
        for i in range(end_index, start_index, -1):
            self.notebook['cells'].pop(i)

        # Update first cell
        self.edit_cell(merged_text, start_index, cell_type)

        print(f"🔗 Merged cells {start_index}-{end_index}")
        return True

    # ==================== EXPORT/IMPORT ====================

    def save(self):
        """Save notebook to original file."""
        self._save_notebook()

    def save_as(self, path: str):
        """Save notebook to a different file."""
        self._save_notebook(Path(path))

    def export_cell(self, index: Optional[int] = None, output_file: Optional[str] = None):
        """Export cell content to a file."""
        if index is None:
            index = self.current_cell_index

        cell = self.view_cell(index, show_output=False)
        if not cell:
            return False

        source = ''.join(cell.get('source', []))

        if output_file:
            with open(output_file, 'w') as f:
                f.write(source)
            print(f"📤 Exported cell {index} to {output_file}")
        else:
            return source

    def import_from_file(self, file_path: str, cell_type: str = 'code',
                        position: str = 'after'):
        """Import content from file as a new cell."""
        with open(file_path, 'r') as f:
            content = f.read()

        self.insert_cell(content, cell_type, position=position)
        print(f"📥 Imported {file_path} as new {cell_type} cell")

    # ==================== STATISTICS & INFO ====================

    def get_stats(self):
        """Get notebook statistics."""
        code_cells = len([c for c in self.notebook['cells'] if c['cell_type'] == 'code'])
        markdown_cells = len([c for c in self.notebook['cells'] if c['cell_type'] == 'markdown'])

        total_lines = 0
        for cell in self.notebook['cells']:
            source = ''.join(cell.get('source', []))
            total_lines += len(source.split('\n'))

        print(f"\n📊 Notebook Statistics")
        print(f"{'='*70}")
        print(f"File: {self.notebook_path.name}")
        print(f"Total cells: {self.get_cell_count()}")
        print(f"  - Code cells: {code_cells}")
        print(f"  - Markdown cells: {markdown_cells}")
        print(f"Total lines: {total_lines}")
        print(f"Current cell: {self.current_cell_index}")
        print(f"History states: {len(self.history)}")
        print(f"{'='*70}\n")


# ==================== CLI INTERFACE ====================

class NotebookCLI:
    """Interactive CLI for notebook controller."""

    def __init__(self, controller: NotebookController):
        self.controller = controller
        self.running = True

    def run(self):
        """Start interactive CLI."""
        print("\n" + "="*70)
        print("📓 NOTEBOOK CONTROLLER - Interactive Mode")
        print("="*70)
        print("Type 'help' for available commands, 'exit' to quit\n")

        while self.running:
            try:
                cmd = input(f"[Cell {self.controller.current_cell_index}] > ").strip()

                if not cmd:
                    continue

                self.execute_command(cmd)

            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit")
            except EOFError:
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        print("\n👋 Goodbye!\n")

    def execute_command(self, cmd: str):
        """Execute a CLI command."""
        parts = cmd.split()
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        # Navigation commands
        if command == 'next' or command == 'n':
            self.controller.next_cell()

        elif command == 'prev' or command == 'p':
            self.controller.prev_cell()

        elif command == 'jump' or command == 'j':
            if args:
                self.controller.jump_to_cell(int(args[0]))
            else:
                print("Usage: jump <index>")

        elif command == 'first':
            self.controller.first_cell()

        elif command == 'last':
            self.controller.last_cell()

        # Viewing commands
        elif command == 'view' or command == 'v':
            index = int(args[0]) if args else None
            self.controller.view_cell(index)

        elif command == 'list' or command == 'ls':
            show_content = '--content' in args or '-c' in args
            self.controller.list_all_cells(show_content)

        elif command == 'search':
            if args:
                pattern = ' '.join(args)
                self.controller.search_cells(pattern)
            else:
                print("Usage: search <pattern>")

        # Editing commands
        elif command == 'edit' or command == 'e':
            print("Enter new content (Ctrl+D or Ctrl+Z to finish):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass

            content = '\n'.join(lines)
            self.controller.edit_cell(content)

        elif command == 'clear':
            index = int(args[0]) if args else None
            self.controller.clear_cell(index)

        elif command == 'delete' or command == 'del':
            index = int(args[0]) if args else None
            self.controller.delete_cell(index)

        elif command == 'insert':
            if args:
                cell_type = args[0] if args[0] in ['code', 'markdown'] else 'code'
                print(f"Enter content for new {cell_type} cell (Ctrl+D to finish):")
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass

                content = '\n'.join(lines)
                self.controller.insert_cell(content, cell_type)
            else:
                print("Usage: insert [code|markdown]")

        elif command == 'duplicate' or command == 'dup':
            self.controller.duplicate_cell()

        # Execution commands
        elif command == 'run' or command == 'r':
            index = int(args[0]) if args else None
            self.controller.execute_cell(index)

        elif command == 'runall':
            self.controller.execute_all_cells()

        elif command == 'clearoutputs':
            if args and args[0] == 'all':
                self.controller.clear_all_outputs()
            else:
                self.controller.clear_outputs()

        # Undo/Redo
        elif command == 'undo' or command == 'u':
            self.controller.undo()

        elif command == 'redo':
            self.controller.redo()

        elif command == 'history' or command == 'hist':
            self.controller.show_history()

        # Save commands
        elif command == 'save' or command == 's':
            self.controller.save()

        elif command == 'saveas':
            if args:
                self.controller.save_as(args[0])
            else:
                print("Usage: saveas <path>")

        # Info commands
        elif command == 'stats':
            self.controller.get_stats()

        elif command == 'help' or command == 'h':
            self.print_help()

        elif command == 'exit' or command == 'quit' or command == 'q':
            self.running = False

        else:
            print(f"❌ Unknown command: {command}")
            print("Type 'help' for available commands")

    def print_help(self):
        """Print help message."""
        help_text = """
📖 AVAILABLE COMMANDS

Navigation:
  next, n              Move to next cell
  prev, p              Move to previous cell
  jump <index>, j      Jump to specific cell
  first                Jump to first cell
  last                 Jump to last cell

Viewing:
  view [index], v      View cell content
  list [-c], ls        List all cells (-c shows content)
  search <pattern>     Search for pattern in cells

Editing:
  edit, e              Edit current cell
  clear [index]        Clear cell content
  delete [index], del  Delete cell
  insert [type]        Insert new cell (code/markdown)
  duplicate, dup       Duplicate current cell

Execution:
  run [index], r       Execute cell
  runall               Execute all cells
  clearoutputs [all]   Clear cell output(s)

Undo/Redo:
  undo, u              Undo last change
  redo                 Redo last undone change
  history, hist        Show history

Save:
  save, s              Save notebook
  saveas <path>        Save as new file

Info:
  stats                Show notebook statistics
  help, h              Show this help
  exit, quit, q        Exit interactive mode
"""
        print(help_text)


# ==================== MAIN ====================

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Notebook Controller - Professional Jupyter Notebook Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python notebook_controller.py notebook.ipynb

  # View specific cell
  python notebook_controller.py notebook.ipynb --view 5

  # Execute all cells
  python notebook_controller.py notebook.ipynb --execute-all

  # Clear all outputs
  python notebook_controller.py notebook.ipynb --clear-outputs

  # Search for pattern
  python notebook_controller.py notebook.ipynb --search "import pandas"
        """
    )

    parser.add_argument('notebook', help='Path to .ipynb file')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Start interactive CLI mode')
    parser.add_argument('-v', '--view', type=int, metavar='INDEX',
                       help='View specific cell')
    parser.add_argument('-l', '--list', action='store_true',
                       help='List all cells')
    parser.add_argument('-e', '--execute', type=int, metavar='INDEX',
                       help='Execute specific cell')
    parser.add_argument('--execute-all', action='store_true',
                       help='Execute all cells')
    parser.add_argument('-c', '--clear-outputs', action='store_true',
                       help='Clear all outputs')
    parser.add_argument('-s', '--search', type=str, metavar='PATTERN',
                       help='Search for pattern')
    parser.add_argument('--stats', action='store_true',
                       help='Show notebook statistics')
    parser.add_argument('--no-backup', action='store_true',
                       help='Disable automatic backups')

    args = parser.parse_args()

    # Create controller
    try:
        controller = NotebookController(args.notebook, auto_backup=not args.no_backup)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # Execute commands
    if args.view is not None:
        controller.view_cell(args.view)

    elif args.list:
        controller.list_all_cells(show_content=True)

    elif args.execute is not None:
        controller.execute_cell(args.execute)
        controller.save()

    elif args.execute_all:
        controller.execute_all_cells()
        controller.save()

    elif args.clear_outputs:
        controller.clear_all_outputs()
        controller.save()

    elif args.search:
        controller.search_cells(args.search)

    elif args.stats:
        controller.get_stats()

    elif args.interactive or len(sys.argv) == 2:
        # Default to interactive mode
        cli = NotebookCLI(controller)
        cli.run()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
