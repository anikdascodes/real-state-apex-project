#!/usr/bin/env python3
"""
Analyze Jupyter notebook cells and outputs
"""
import json
import sys

def analyze_notebook(notebook_path):
    """Analyze all cells in a Jupyter notebook"""

    with open(notebook_path, 'r') as f:
        notebook = json.load(f)

    print("=" * 100)
    print(f"NOTEBOOK ANALYSIS: {notebook_path}")
    print("=" * 100)
    print(f"\nTotal Cells: {len(notebook['cells'])}")

    # Count cell types
    cell_types = {}
    for cell in notebook['cells']:
        cell_type = cell['cell_type']
        cell_types[cell_type] = cell_types.get(cell_type, 0) + 1

    print(f"\nCell Type Distribution:")
    for cell_type, count in cell_types.items():
        print(f"  - {cell_type}: {count}")

    print("\n" + "=" * 100)
    print("DETAILED CELL-BY-CELL ANALYSIS")
    print("=" * 100)

    for idx, cell in enumerate(notebook['cells'], 1):
        print(f"\n{'#' * 100}")
        print(f"CELL {idx}/{len(notebook['cells'])} - Type: {cell['cell_type'].upper()}")
        print('#' * 100)

        # Get cell source
        source = cell.get('source', [])
        if isinstance(source, list):
            source_text = ''.join(source)
        else:
            source_text = source

        # Display source (first 500 chars)
        if source_text.strip():
            print(f"\n--- SOURCE ---")
            if len(source_text) > 1000:
                print(source_text[:1000] + "\n... [truncated] ...")
            else:
                print(source_text)

        # For code cells, analyze outputs
        if cell['cell_type'] == 'code':
            outputs = cell.get('outputs', [])

            if outputs:
                print(f"\n--- OUTPUTS ({len(outputs)} output(s)) ---")

                for out_idx, output in enumerate(outputs, 1):
                    output_type = output.get('output_type', 'unknown')
                    print(f"\n  Output {out_idx}: {output_type}")

                    if output_type == 'stream':
                        text = ''.join(output.get('text', []))
                        if text:
                            print(f"  Stream ({output.get('name', 'stdout')}):")
                            if len(text) > 500:
                                print(f"  {text[:500]}... [truncated]")
                            else:
                                print(f"  {text}")

                    elif output_type == 'execute_result':
                        data = output.get('data', {})
                        if 'text/plain' in data:
                            text = ''.join(data['text/plain'])
                            print(f"  Result: {text[:500] if len(text) > 500 else text}")
                        if 'text/html' in data:
                            print(f"  HTML output present (length: {len(''.join(data['text/html']))} chars)")
                        if 'image/png' in data:
                            print(f"  Image output present (PNG)")

                    elif output_type == 'display_data':
                        data = output.get('data', {})
                        if 'text/plain' in data:
                            text = ''.join(data['text/plain'])
                            print(f"  Display: {text[:300] if len(text) > 300 else text}")
                        if 'image/png' in data:
                            print(f"  Image/Plot generated (PNG)")
                        if 'text/html' in data:
                            print(f"  HTML display (length: {len(''.join(data['text/html']))} chars)")

                    elif output_type == 'error':
                        print(f"  ERROR: {output.get('ename', 'Unknown')}")
                        print(f"  Message: {output.get('evalue', '')}")
            else:
                print(f"\n--- NO OUTPUTS ---")

            # Check execution count
            exec_count = cell.get('execution_count')
            if exec_count is not None:
                print(f"\nExecution Count: {exec_count}")

    print("\n" + "=" * 100)
    print("SUMMARY STATISTICS")
    print("=" * 100)

    # Count cells with outputs
    code_cells = [c for c in notebook['cells'] if c['cell_type'] == 'code']
    cells_with_output = sum(1 for c in code_cells if c.get('outputs'))
    cells_with_errors = sum(1 for c in code_cells
                           if any(o.get('output_type') == 'error' for o in c.get('outputs', [])))
    cells_with_plots = sum(1 for c in code_cells
                          if any('image/png' in o.get('data', {}) for o in c.get('outputs', [])))

    print(f"\nCode cells with outputs: {cells_with_output}/{len(code_cells)}")
    print(f"Code cells with errors: {cells_with_errors}")
    print(f"Code cells with plots/images: {cells_with_plots}")

    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)

if __name__ == "__main__":
    notebook_path = "notebooks/Ames_Housing_Analysis_Output.ipynb"
    analyze_notebook(notebook_path)
