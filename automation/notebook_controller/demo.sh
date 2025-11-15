#!/bin/bash
#
# Notebook Controller Demo Script
# ===============================
#
# This script demonstrates the key features of the Notebook Controller tool
#
# Usage: bash automation/notebook_controller/demo.sh
#

echo "======================================================================"
echo "NOTEBOOK CONTROLLER - DEMONSTRATION"
echo "======================================================================"
echo ""

NOTEBOOK="notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb"
SCRIPT="automation/notebook_controller/notebook_controller.py"

# Check if notebook exists
if [ ! -f "$NOTEBOOK" ]; then
    echo "❌ Error: Notebook not found: $NOTEBOOK"
    exit 1
fi

echo "📓 Using notebook: $NOTEBOOK"
echo ""

# Demo 1: Show Statistics
echo "======================================================================"
echo "DEMO 1: Show Notebook Statistics"
echo "======================================================================"
python $SCRIPT $NOTEBOOK --stats
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 2: View Specific Cell
echo "======================================================================"
echo "DEMO 2: View Specific Cell (Cell 0)"
echo "======================================================================"
python $SCRIPT $NOTEBOOK --view 0
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 3: List All Cells
echo "======================================================================"
echo "DEMO 3: List All Cells (first 20)"
echo "======================================================================"
python $SCRIPT $NOTEBOOK --list | head -30
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 4: Search for Pattern
echo "======================================================================"
echo "DEMO 4: Search for 'import' Statements"
echo "======================================================================"
python $SCRIPT $NOTEBOOK --search "import pandas"
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 5: Python API Example
echo "======================================================================"
echo "DEMO 5: Python API Usage"
echo "======================================================================"
cat << 'EOF'
Python API Example:

from scripts.notebook_controller import NotebookController

# Load notebook
nb = NotebookController('notebook.ipynb')

# Navigate
nb.jump_to_cell(5)
nb.view_cell()

# Edit
nb.edit_cell("print('Hello World')", index=5)

# Execute
nb.execute_cell(5)

# Save
nb.save()
EOF
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 6: Show Available Examples
echo "======================================================================"
echo "DEMO 6: Practical Examples"
echo "======================================================================"
echo "Run automation examples:"
echo ""
echo "  python automation/notebook_controller/examples.py 1   # Basic Navigation"
echo "  python automation/notebook_controller/examples.py 2   # Search & Analyze"
echo "  python automation/notebook_controller/examples.py 3   # Cell Manipulation"
echo "  python automation/notebook_controller/examples.py 4   # Undo/Redo"
echo "  python automation/notebook_controller/examples.py 5   # Batch Operations"
echo "  python automation/notebook_controller/examples.py 6   # Output Management"
echo "  python automation/notebook_controller/examples.py 7   # Export/Import"
echo "  python automation/notebook_controller/examples.py 8   # Validation"
echo "  python automation/notebook_controller/examples.py all # All examples"
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 7: Interactive Mode Information
echo "======================================================================"
echo "DEMO 7: Interactive Mode"
echo "======================================================================"
echo "To start interactive mode:"
echo ""
echo "  python automation/notebook_controller/notebook_controller.py $NOTEBOOK"
echo ""
echo "Then use commands like:"
echo "  - list          List all cells"
echo "  - view 5        View cell 5"
echo "  - jump 10       Jump to cell 10"
echo "  - search pandas Search for 'pandas'"
echo "  - stats         Show statistics"
echo "  - help          Show all commands"
echo "  - exit          Exit"
echo ""
read -p "Press Enter to finish demo..."
echo ""

echo "======================================================================"
echo "DEMO COMPLETE!"
echo "======================================================================"
echo ""
echo "📚 Documentation:"
echo "  - Main README:  automation/README.md"
echo "  - Quick Start:  automation/docs/QUICK_START.md"
echo "  - API Reference: automation/docs/API_REFERENCE.md"
echo "  - Examples:     automation/docs/EXAMPLES.md"
echo ""
echo "🧪 Try it yourself:"
echo "  python automation/notebook_controller/notebook_controller.py $NOTEBOOK"
echo ""
echo "❓ Get help:"
echo "  python automation/notebook_controller/notebook_controller.py --help"
echo ""
