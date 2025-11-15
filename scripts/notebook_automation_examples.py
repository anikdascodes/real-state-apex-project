#!/usr/bin/env python3
"""
Notebook Automation Examples
=============================

Practical examples demonstrating the Notebook Controller API for various
automation tasks.

Run with: python scripts/notebook_automation_examples.py
"""

from notebook_controller import NotebookController
import sys


def example_1_basic_navigation():
    """Example 1: Basic navigation and viewing."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Navigation and Viewing")
    print("="*70 + "\n")

    # Load notebook
    nb = NotebookController('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb',
                           auto_backup=False)

    # Navigate through cells
    print("1. Viewing first cell:")
    nb.first_cell()
    nb.view_cell()

    print("\n2. Jumping to cell 10:")
    nb.jump_to_cell(10)
    nb.view_cell()

    print("\n3. Moving to next cell:")
    nb.next_cell()

    print("\n4. Jumping to last cell:")
    nb.last_cell()
    print(f"   Current cell: {nb.current_cell_index}")

    print("\n✅ Example 1 completed!")


def example_2_search_and_analyze():
    """Example 2: Search for patterns and analyze content."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Search and Analyze")
    print("="*70 + "\n")

    nb = NotebookController('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb',
                           auto_backup=False)

    # Search for imports
    print("1. Searching for 'import' statements:")
    matches = nb.search_cells('import', cell_type='code')

    # Get statistics
    print("\n2. Notebook statistics:")
    nb.get_stats()

    # Find all code cells
    print("3. Analyzing cell types:")
    code_cells = nb.filter_cells('code')
    markdown_cells = nb.filter_cells('markdown')

    print(f"   Code cells: {len(code_cells)}")
    print(f"   Markdown cells: {len(markdown_cells)}")

    print("\n✅ Example 2 completed!")


def example_3_cell_manipulation():
    """Example 3: Edit, insert, and delete cells (creates test notebook)."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Cell Manipulation")
    print("="*70 + "\n")

    # Create a test notebook from existing one
    nb = NotebookController('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb')

    # Save as test notebook
    test_path = 'notebooks/test_manipulation.ipynb'
    nb.save_as(test_path)

    # Reload test notebook
    nb = NotebookController(test_path)

    print("1. Original cell count:", nb.get_cell_count())

    # Insert a new markdown cell at the beginning
    print("\n2. Inserting new markdown cell at position 0:")
    nb.jump_to_cell(0)
    nb.insert_cell("# TEST CELL\nThis is a test cell inserted by automation",
                   cell_type='markdown',
                   position='before')

    print("   New cell count:", nb.get_cell_count())

    # Edit a cell
    print("\n3. Editing the newly inserted cell:")
    nb.edit_cell("# MODIFIED TEST CELL\nThis cell has been modified",
                index=0,
                cell_type='markdown')

    # Duplicate a cell
    print("\n4. Duplicating cell 5:")
    original_count = nb.get_cell_count()
    nb.duplicate_cell(5)
    print(f"   Cell count: {original_count} → {nb.get_cell_count()}")

    # Delete the test cell
    print("\n5. Deleting the first test cell:")
    nb.delete_cell(0)
    print("   New cell count:", nb.get_cell_count())

    # Save changes
    nb.save()

    print("\n✅ Example 3 completed! Test notebook saved to:", test_path)


def example_4_undo_redo():
    """Example 4: Demonstrate undo/redo functionality."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Undo/Redo Functionality")
    print("="*70 + "\n")

    # Use test notebook from example 3
    nb = NotebookController('notebooks/test_manipulation.ipynb')

    print("1. Original cell count:", nb.get_cell_count())
    original_count = nb.get_cell_count()

    # Make some changes
    print("\n2. Deleting cell 5:")
    nb.delete_cell(5)
    print("   Cell count after delete:", nb.get_cell_count())

    print("\n3. Inserting a new cell:")
    nb.insert_cell("print('Test')", cell_type='code', position='after')
    print("   Cell count after insert:", nb.get_cell_count())

    # Show history
    print("\n4. Current history:")
    nb.show_history()

    # Undo operations
    print("\n5. Undoing last operation (insert):")
    nb.undo()
    print("   Cell count after undo:", nb.get_cell_count())

    print("\n6. Undoing again (delete):")
    nb.undo()
    print("   Cell count after undo:", nb.get_cell_count())

    # Redo operation
    print("\n7. Redoing one operation:")
    nb.redo()
    print("   Cell count after redo:", nb.get_cell_count())

    print("\n✅ Example 4 completed!")


def example_5_batch_operations():
    """Example 5: Batch operations on multiple cells."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Batch Operations")
    print("="*70 + "\n")

    nb = NotebookController('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb',
                           auto_backup=False)

    # Find all markdown cells
    print("1. Finding all markdown cells:")
    markdown_indices = nb.filter_cells('markdown')
    print(f"   Found {len(markdown_indices)} markdown cells")
    print(f"   Indices: {markdown_indices[:10]}..." if len(markdown_indices) > 10
          else f"   Indices: {markdown_indices}")

    # Find all code cells
    print("\n2. Finding all code cells:")
    code_indices = nb.filter_cells('code')
    print(f"   Found {len(code_indices)} code cells")

    # Search for specific pattern
    print("\n3. Searching for 'DataFrame' in code cells:")
    matches = nb.search_cells('DataFrame', cell_type='code')
    print(f"   Found in {len(matches)} cells")

    # Count cells with outputs
    print("\n4. Analyzing cells with outputs:")
    cells_with_output = 0
    for i in code_indices:
        cell = nb.view_cell(i, show_output=False)
        if cell.get('outputs'):
            cells_with_output += 1

    print(f"   Code cells with output: {cells_with_output}/{len(code_indices)}")

    print("\n✅ Example 5 completed!")


def example_6_output_management():
    """Example 6: Clear and manage cell outputs."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Output Management")
    print("="*70 + "\n")

    # Create test notebook
    nb = NotebookController('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb')
    test_path = 'notebooks/test_outputs.ipynb'
    nb.save_as(test_path)

    nb = NotebookController(test_path)

    # Count outputs before
    print("1. Counting cells with outputs:")
    code_cells = nb.filter_cells('code')
    outputs_before = 0
    for i in code_cells:
        cell = nb.view_cell(i, show_output=False)
        if cell.get('outputs'):
            outputs_before += 1

    print(f"   Cells with outputs: {outputs_before}")

    # Clear specific cell output
    print("\n2. Clearing output from cell 7:")
    nb.clear_outputs(7)

    # Clear all outputs
    print("\n3. Clearing all outputs:")
    nb.clear_all_outputs()

    # Count outputs after
    outputs_after = 0
    for i in code_cells:
        cell = nb.view_cell(i, show_output=False)
        if cell.get('outputs'):
            outputs_after += 1

    print(f"   Cells with outputs after clearing: {outputs_after}")

    # Save
    nb.save()

    print(f"\n✅ Example 6 completed! Clean notebook saved to: {test_path}")


def example_7_export_import():
    """Example 7: Export and import cells."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Export and Import")
    print("="*70 + "\n")

    nb = NotebookController('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb',
                           auto_backup=False)

    # Export a code cell
    print("1. Exporting cell 7 (import statements) to file:")
    exported_content = nb.export_cell(index=7, output_file='notebooks/exported_cell.py')
    print("   ✅ Exported to: notebooks/exported_cell.py")

    # View what was exported
    print("\n2. Content of exported cell:")
    with open('notebooks/exported_cell.py', 'r') as f:
        content = f.read()
        print("   " + content[:200].replace('\n', '\n   ') + "...")

    print("\n✅ Example 7 completed!")


def example_8_validation():
    """Example 8: Validate notebook structure."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Notebook Validation")
    print("="*70 + "\n")

    nb = NotebookController('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb',
                           auto_backup=False)

    issues = []

    # Check 1: Empty cells
    print("1. Checking for empty cells...")
    empty_count = 0
    for i in range(nb.get_cell_count()):
        cell = nb.view_cell(i, show_output=False)
        source = ''.join(cell.get('source', []))
        if not source.strip():
            empty_count += 1
            issues.append(f"Cell {i}: Empty cell")

    print(f"   Empty cells found: {empty_count}")

    # Check 2: Cells with errors
    print("\n2. Checking for execution errors...")
    error_count = 0
    code_cells = nb.filter_cells('code')
    for i in code_cells:
        cell = nb.view_cell(i, show_output=False)
        outputs = cell.get('outputs', [])

        for output in outputs:
            if output.get('output_type') == 'error':
                error_count += 1
                error_name = output.get('ename', 'Unknown')
                issues.append(f"Cell {i}: {error_name} error")

    print(f"   Cells with errors: {error_count}")

    # Check 3: Verify structure
    print("\n3. Verifying notebook structure...")
    print(f"   Total cells: {nb.get_cell_count()}")
    print(f"   Code cells: {len(nb.filter_cells('code'))}")
    print(f"   Markdown cells: {len(nb.filter_cells('markdown'))}")

    # Report
    print("\n4. Validation Summary:")
    if issues:
        print(f"   ⚠️  Found {len(issues)} issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"      - {issue}")
        if len(issues) > 10:
            print(f"      ... and {len(issues) - 10} more")
    else:
        print("   ✅ All checks passed!")

    print("\n✅ Example 8 completed!")


def run_all_examples():
    """Run all examples in sequence."""
    examples = [
        ("Basic Navigation", example_1_basic_navigation),
        ("Search and Analyze", example_2_search_and_analyze),
        ("Cell Manipulation", example_3_cell_manipulation),
        ("Undo/Redo", example_4_undo_redo),
        ("Batch Operations", example_5_batch_operations),
        ("Output Management", example_6_output_management),
        ("Export/Import", example_7_export_import),
        ("Validation", example_8_validation),
    ]

    print("\n" + "="*70)
    print("NOTEBOOK AUTOMATION EXAMPLES")
    print("="*70)
    print("\nRunning all examples...\n")

    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {str(e)}")

        input("\nPress Enter to continue to next example...")

    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED!")
    print("="*70 + "\n")


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        example_num = sys.argv[1]

        examples = {
            '1': example_1_basic_navigation,
            '2': example_2_search_and_analyze,
            '3': example_3_cell_manipulation,
            '4': example_4_undo_redo,
            '5': example_5_batch_operations,
            '6': example_6_output_management,
            '7': example_7_export_import,
            '8': example_8_validation,
        }

        if example_num in examples:
            examples[example_num]()
        elif example_num == 'all':
            run_all_examples()
        else:
            print("Invalid example number. Available: 1-8, all")
    else:
        print("""
Notebook Automation Examples
============================

Usage:
  python scripts/notebook_automation_examples.py <example_number>
  python scripts/notebook_automation_examples.py all

Available examples:
  1 - Basic Navigation and Viewing
  2 - Search and Analyze
  3 - Cell Manipulation
  4 - Undo/Redo Functionality
  5 - Batch Operations
  6 - Output Management
  7 - Export and Import
  8 - Notebook Validation
  all - Run all examples

Example:
  python scripts/notebook_automation_examples.py 1
  python scripts/notebook_automation_examples.py all
        """)


if __name__ == '__main__':
    main()
