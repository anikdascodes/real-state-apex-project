#!/usr/bin/env python3
"""
Comprehensive Cell-by-Cell Notebook Verification
Checks every single cell in the notebook systematically
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

class NotebookCellVerifier:
    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
        self.cells = self.notebook['cells']
        self.total_cells = len(self.cells)
        self.verification_results = []

    def check_cell_has_content(self, cell: Dict) -> bool:
        """Check if cell has actual content"""
        source = cell.get('source', [])
        if isinstance(source, list):
            content = ''.join(source).strip()
        else:
            content = source.strip()
        return len(content) > 0

    def check_code_cell_has_output(self, cell: Dict) -> tuple:
        """Check if code cell has output"""
        if cell['cell_type'] != 'code':
            return (None, None)

        outputs = cell.get('outputs', [])
        has_output = len(outputs) > 0

        output_types = []
        for output in outputs:
            output_type = output.get('output_type', 'unknown')
            output_types.append(output_type)

        return (has_output, output_types)

    def get_cell_content_preview(self, cell: Dict, max_length: int = 100) -> str:
        """Get preview of cell content"""
        source = cell.get('source', [])
        if isinstance(source, list):
            content = ''.join(source).strip()
        else:
            content = source.strip()

        if len(content) > max_length:
            return content[:max_length] + '...'
        return content

    def categorize_cell(self, cell_idx: int, cell: Dict) -> str:
        """Categorize what this cell does based on content"""
        source = cell.get('source', [])
        if isinstance(source, list):
            content = ''.join(source).lower()
        else:
            content = source.lower()

        # Phase 1: Data Acquisition
        if any(kw in content for kw in ['import', 'pandas', 'numpy', 'matplotlib']):
            if cell_idx < 10:
                return 'PHASE_1_IMPORTS'
        if any(kw in content for kw in ['read_csv', 'load', 'data']):
            return 'PHASE_1_DATA_LOAD'
        if any(kw in content for kw in ['head(', 'shape', 'info(', 'columns']):
            return 'PHASE_1_INITIAL_EXPLORE'

        # Phase 2: Preprocessing & EDA
        if any(kw in content for kw in ['missing', 'isnull', 'fillna', 'dropna']):
            return 'PHASE_2_MISSING_DATA'
        if any(kw in content for kw in ['describe(', 'summary statistics']):
            return 'PHASE_2_STATISTICS'
        if any(kw in content for kw in ['plot', 'scatter', 'histogram', 'visualization']):
            return 'PHASE_2_VISUALIZATION'
        if any(kw in content for kw in ['encode', 'labelencoder', 'categorical']):
            return 'PHASE_2_ENCODING'
        if any(kw in content for kw in ['outlier', 'iqr']):
            return 'PHASE_2_OUTLIERS'
        if any(kw in content for kw in ['correlation', 'corr(']):
            return 'PHASE_2_CORRELATION'

        # Phase 3: Modeling
        if any(kw in content for kw in ['train_test_split', 'split']):
            return 'PHASE_3_DATA_SPLIT'
        if any(kw in content for kw in ['linearregression', 'model', 'fit(']):
            return 'PHASE_3_MODEL_TRAINING'
        if any(kw in content for kw in ['predict', 'prediction']):
            return 'PHASE_3_PREDICTION'
        if any(kw in content for kw in ['r2_score', 'mean_squared_error', 'evaluation']):
            return 'PHASE_3_EVALUATION'

        # Markdown sections
        if cell['cell_type'] == 'markdown':
            if any(kw in content for kw in ['#', 'introduction', 'overview']):
                return 'MARKDOWN_HEADER'
            if 'data dictionary' in content:
                return 'MARKDOWN_DATA_DICT'
            if any(kw in content for kw in ['conclusion', 'summary']):
                return 'MARKDOWN_CONCLUSION'
            return 'MARKDOWN_EXPLANATION'

        return 'OTHER'

    def verify_cell(self, cell_idx: int) -> Dict[str, Any]:
        """Verify a single cell comprehensively"""
        cell = self.cells[cell_idx]
        cell_type = cell['cell_type']

        result = {
            'cell_number': cell_idx + 1,  # 1-indexed for human reading
            'cell_type': cell_type,
            'has_content': self.check_cell_has_content(cell),
            'content_preview': self.get_cell_content_preview(cell, 150),
            'category': self.categorize_cell(cell_idx, cell),
            'issues': []
        }

        # Check for empty cells
        if not result['has_content']:
            result['issues'].append('EMPTY_CELL')

        # For code cells, check outputs
        if cell_type == 'code':
            has_output, output_types = self.check_code_cell_has_output(cell)
            result['has_output'] = has_output
            result['output_types'] = output_types

            # Check if code cell should have output but doesn't
            source = ''.join(cell.get('source', [])).strip()
            if source and not source.startswith('#') and not has_output:
                # Some cells might not produce output (assignments, imports)
                if not any(kw in source for kw in ['import ', '=', 'def ', 'class ']):
                    result['issues'].append('NO_OUTPUT')

        # For markdown cells, check quality
        if cell_type == 'markdown':
            content = ''.join(cell.get('source', []))
            # Check for AI-like patterns (excessive emojis, etc.)
            emoji_count = sum(1 for char in content if ord(char) > 127000)
            if emoji_count > 3:
                result['issues'].append('EXCESSIVE_EMOJIS')

        return result

    def verify_all_cells(self):
        """Verify all cells in the notebook"""
        print("="*80)
        print("COMPREHENSIVE CELL-BY-CELL NOTEBOOK VERIFICATION")
        print("="*80)
        print(f"Notebook: {self.notebook_path.name}")
        print(f"Total cells: {self.total_cells}")
        print("="*80)
        print()

        for i in range(self.total_cells):
            result = self.verify_cell(i)
            self.verification_results.append(result)

    def print_detailed_report(self):
        """Print detailed verification report"""
        # Group by category
        categories = {}
        for result in self.verification_results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)

        print("\n" + "="*80)
        print("DETAILED VERIFICATION REPORT - GROUPED BY CATEGORY")
        print("="*80)

        for category, cells in sorted(categories.items()):
            print(f"\n{'='*80}")
            print(f"CATEGORY: {category}")
            print(f"{'='*80}")
            print(f"Total cells in category: {len(cells)}\n")

            for result in cells:
                cell_num = result['cell_number']
                cell_type = result['cell_type'].upper()
                status = '✅' if not result['issues'] else '⚠️'

                print(f"{status} Cell {cell_num:3d} [{cell_type:8s}] {result['category']}")
                print(f"    Preview: {result['content_preview'][:100]}")

                if cell_type == 'CODE':
                    if result.get('has_output'):
                        print(f"    Output: {', '.join(result['output_types'])}")
                    else:
                        print(f"    Output: None")

                if result['issues']:
                    print(f"    Issues: {', '.join(result['issues'])}")

                print()

    def print_summary(self):
        """Print summary statistics"""
        total_code = sum(1 for r in self.verification_results if r['cell_type'] == 'code')
        total_markdown = sum(1 for r in self.verification_results if r['cell_type'] == 'markdown')

        code_with_output = sum(1 for r in self.verification_results
                               if r['cell_type'] == 'code' and r.get('has_output', False))

        cells_with_issues = sum(1 for r in self.verification_results if r['issues'])

        print("\n" + "="*80)
        print("VERIFICATION SUMMARY")
        print("="*80)
        print(f"Total Cells: {self.total_cells}")
        print(f"  - Code cells: {total_code}")
        print(f"  - Markdown cells: {total_markdown}")
        print(f"\nCode Cells with Output: {code_with_output}/{total_code}")
        print(f"Cells with Issues: {cells_with_issues}/{self.total_cells}")

        if cells_with_issues == 0:
            print("\n✅ ALL CELLS VERIFIED SUCCESSFULLY - NO ISSUES FOUND")
        else:
            print(f"\n⚠️  {cells_with_issues} cells have potential issues")

        print("="*80)

    def print_checkpoint_verification(self):
        """Print verification by phase checkpoints"""
        print("\n" + "="*80)
        print("CHECKPOINT VERIFICATION BY PHASES")
        print("="*80)

        # Define checkpoints
        checkpoints = {
            'CHECKPOINT 1: Phase 1 - Data Acquisition & Setup': range(0, 19),
            'CHECKPOINT 2: Phase 2 - Preprocessing & EDA': range(19, 58),
            'CHECKPOINT 3: Phase 3 - Modeling & Evaluation': range(58, self.total_cells)
        }

        for checkpoint_name, cell_range in checkpoints.items():
            print(f"\n{'='*80}")
            print(f"{checkpoint_name}")
            print(f"Cells: {cell_range.start + 1} to {cell_range.stop}")
            print(f"{'='*80}")

            checkpoint_cells = [r for i, r in enumerate(self.verification_results)
                               if i in cell_range]

            code_cells = [r for r in checkpoint_cells if r['cell_type'] == 'code']
            md_cells = [r for r in checkpoint_cells if r['cell_type'] == 'markdown']

            code_with_output = [r for r in code_cells if r.get('has_output', False)]
            cells_with_issues = [r for r in checkpoint_cells if r['issues']]

            print(f"Total cells: {len(checkpoint_cells)}")
            print(f"  Code: {len(code_cells)} (with output: {len(code_with_output)})")
            print(f"  Markdown: {len(md_cells)}")
            print(f"Issues: {len(cells_with_issues)}")

            if cells_with_issues:
                print(f"\nCells with issues:")
                for r in cells_with_issues:
                    print(f"  - Cell {r['cell_number']}: {', '.join(r['issues'])}")
            else:
                print(f"\n✅ Checkpoint passed - all cells verified")


if __name__ == '__main__':
    notebook_path = 'notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb'

    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]

    verifier = NotebookCellVerifier(notebook_path)
    verifier.verify_all_cells()
    verifier.print_checkpoint_verification()
    verifier.print_detailed_report()
    verifier.print_summary()
