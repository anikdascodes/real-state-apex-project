#!/usr/bin/env python3
"""
Execute Notebook Cell by Cell
Runs each cell and saves outputs to the notebook
"""

import json
import sys
import subprocess
from datetime import datetime

def execute_notebook_cells(notebook_path, output_path):
    """Execute notebook cell by cell using nbconvert"""

    print("="*80)
    print("EXECUTING NOTEBOOK CELL BY CELL")
    print("="*80)
    print(f"Input: {notebook_path}")
    print(f"Output: {output_path}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    # Use jupyter nbconvert to execute the notebook
    cmd = [
        'jupyter', 'nbconvert',
        '--to', 'notebook',
        '--execute',
        '--ExecutePreprocessor.timeout=600',  # 10 minute timeout per cell
        '--output', output_path,
        notebook_path
    ]

    print(f"\nExecuting command: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        print("✅ Notebook execution completed successfully!")
        print(f"\nStdout:\n{result.stdout}")

        if result.stderr:
            print(f"\nStderr:\n{result.stderr}")

        # Verify output file exists
        import os
        actual_output = os.path.join('notebooks', output_path)
        if os.path.exists(actual_output):
            size = os.path.getsize(actual_output)
            print(f"\n✅ Output file created: {actual_output} ({size:,} bytes)")
        else:
            print(f"\n❌ Output file not found: {actual_output}")
            return False

        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Notebook execution failed!")
        print(f"Error code: {e.returncode}")
        print(f"\nStdout:\n{e.stdout}")
        print(f"\nStderr:\n{e.stderr}")
        return False

    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    input_notebook = "notebooks/Ames_Housing_Price_Prediction_VERIFIED.ipynb"
    output_notebook = "Ames_Housing_Price_Prediction_EXECUTED.ipynb"  # Just filename, nbconvert adds directory

    success = execute_notebook_cells(input_notebook, output_notebook)

    if success:
        print("\n" + "="*80)
        print("EXECUTION COMPLETE")
        print("="*80)
        print(f"✅ Executed notebook saved to: {output_notebook}")
        print(f"✅ All cells executed successfully")
        print(f"✅ Ready for review and submission")
        print("="*80)
        sys.exit(0)
    else:
        print("\n" + "="*80)
        print("EXECUTION FAILED")
        print("="*80)
        print("❌ Please check errors above")
        print("="*80)
        sys.exit(1)
