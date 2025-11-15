#!/usr/bin/env python3
"""
Notebook to PDF Converter
=========================

Converts Jupyter notebooks to professional PDF documents with all outputs,
images, and analysis preserved.

Features:
- Extracts all markdown content
- Includes all code outputs (text, numerical, tables)
- Converts and embeds all images (matplotlib plots, etc.)
- Creates structured LaTeX document
- Compiles to professional PDF

Usage:
    python notebook_to_pdf.py notebook.ipynb output.pdf
"""

import sys
import os
import json
import base64
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'notebook_controller'))
from notebook_controller import NotebookController


class NotebookToPDFConverter:
    """Convert Jupyter notebooks to PDF via LaTeX."""

    def __init__(self, notebook_path, output_pdf_path):
        """
        Initialize converter.

        Args:
            notebook_path: Path to .ipynb file
            output_pdf_path: Path for output PDF
        """
        self.notebook_path = Path(notebook_path)
        self.output_pdf_path = Path(output_pdf_path)
        self.work_dir = self.output_pdf_path.parent / 'pdf_export_temp'
        self.images_dir = self.work_dir / 'images'
        self.nb_controller = None
        self.image_counter = 0

        # Create working directories
        self.work_dir.mkdir(exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)

        print(f"📓 Notebook: {self.notebook_path.name}")
        print(f"📄 Output PDF: {self.output_pdf_path}")
        print(f"📁 Working directory: {self.work_dir}")

    def load_notebook(self):
        """Load notebook using NotebookController."""
        print("\n📖 Loading notebook...")
        self.nb_controller = NotebookController(str(self.notebook_path), auto_backup=False)
        print(f"   ✓ Loaded {self.nb_controller.get_cell_count()} cells")

    def escape_latex(self, text):
        """Escape special LaTeX characters."""
        if not text:
            return ""

        # Characters that need escaping in LaTeX
        replacements = {
            '\\': r'\textbackslash{}',
            '{': r'\{',
            '}': r'\}',
            '$': r'\$',
            '&': r'\&',
            '%': r'\%',
            '#': r'\#',
            '_': r'\_',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }

        # Apply replacements
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        return text

    def markdown_to_latex(self, markdown_text):
        """Convert markdown to LaTeX."""
        if not markdown_text:
            return ""

        text = markdown_text

        # Headers
        text = re.sub(r'^# (.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', text, flags=re.MULTILINE)

        # Bold and italic
        text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
        text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)

        # Code inline
        text = re.sub(r'`(.+?)`', r'\\texttt{\1}', text)

        # Lists (simple conversion)
        text = re.sub(r'^\* (.+)$', r'\\item \1', text, flags=re.MULTILINE)
        text = re.sub(r'^- (.+)$', r'\\item \1', text, flags=re.MULTILINE)
        text = re.sub(r'^\d+\. (.+)$', r'\\item \1', text, flags=re.MULTILINE)

        # Horizontal rules
        text = re.sub(r'^---+$', r'\\hrule', text, flags=re.MULTILINE)

        return text

    def save_image_from_base64(self, base64_data, image_format='png'):
        """Save base64 image data to file."""
        self.image_counter += 1
        image_filename = f"image_{self.image_counter:03d}.{image_format}"
        image_path = self.images_dir / image_filename

        # Decode and save
        image_bytes = base64.b64decode(base64_data)
        with open(image_path, 'wb') as f:
            f.write(image_bytes)

        print(f"   💾 Saved image: {image_filename}")
        return image_path

    def process_output(self, output):
        """Process a single cell output and return LaTeX code."""
        latex_parts = []
        output_type = output.get('output_type', '')

        if output_type == 'stream':
            # Text output
            text = ''.join(output.get('text', []))
            if text.strip():
                escaped_text = self.escape_latex(text)
                latex_parts.append(r'\begin{verbatim}')
                latex_parts.append(text)  # Use raw text in verbatim
                latex_parts.append(r'\end{verbatim}')

        elif output_type == 'execute_result' or output_type == 'display_data':
            data = output.get('data', {})

            # Handle images
            if 'image/png' in data:
                image_path = self.save_image_from_base64(data['image/png'], 'png')
                rel_path = image_path.relative_to(self.work_dir)
                latex_parts.append(r'\begin{figure}[H]')
                latex_parts.append(r'\centering')
                latex_parts.append(f'\\includegraphics[width=0.9\\textwidth]{{{rel_path}}}')
                latex_parts.append(r'\end{figure}')

            # Handle text/plain output
            elif 'text/plain' in data:
                text = ''.join(data['text/plain'])
                if text.strip():
                    latex_parts.append(r'\begin{verbatim}')
                    latex_parts.append(text)
                    latex_parts.append(r'\end{verbatim}')

            # Handle HTML tables (basic conversion)
            elif 'text/html' in data:
                html = ''.join(data['text/html'])
                # For now, just mention there's a table
                latex_parts.append(r'\textit{[Table output - see notebook for details]}')

        elif output_type == 'error':
            # Error output
            ename = output.get('ename', 'Error')
            evalue = output.get('evalue', '')
            latex_parts.append(r'\begin{verbatim}')
            latex_parts.append(f"ERROR: {ename}: {evalue}")
            latex_parts.append(r'\end{verbatim}')

        return '\n'.join(latex_parts)

    def generate_latex(self):
        """Generate LaTeX document from notebook."""
        print("\n🔧 Generating LaTeX document...")

        latex_lines = []

        # Document header
        latex_lines.extend([
            r'\documentclass[11pt,a4paper]{article}',
            r'\usepackage[utf8]{inputenc}',
            r'\usepackage[T1]{fontenc}',
            r'\usepackage{graphicx}',
            r'\usepackage{float}',
            r'\usepackage{amsmath}',
            r'\usepackage{amssymb}',
            r'\usepackage{hyperref}',
            r'\usepackage{listings}',
            r'\usepackage{xcolor}',
            r'\usepackage{fancyhdr}',
            r'\usepackage{geometry}',
            r'\usepackage{longtable}',
            r'\usepackage{booktabs}',
            r'',
            r'% Page geometry',
            r'\geometry{margin=1in}',
            r'',
            r'% Code listing style',
            r'\lstset{',
            r'    basicstyle=\ttfamily\small,',
            r'    breaklines=true,',
            r'    frame=single,',
            r'    backgroundcolor=\color{gray!10},',
            r'    numbers=left,',
            r'    numberstyle=\tiny\color{gray},',
            r'}',
            r'',
            r'% Header/Footer',
            r'\pagestyle{fancy}',
            r'\fancyhf{}',
            r'\rhead{Ames Housing Price Prediction}',
            r'\lhead{Analysis Report}',
            r'\cfoot{\thepage}',
            r'',
            r'\begin{document}',
            r'',
        ])

        # Title page
        latex_lines.extend([
            r'\begin{titlepage}',
            r'\centering',
            r'\vspace*{2cm}',
            r'{\Huge\bfseries Ames Housing Price Prediction\\[0.5cm]}',
            r'{\Large Advanced Apex Project\\[0.3cm]}',
            r'{\large Real Estate Price Modeling\\[2cm]}',
            r'',
            r'{\large\textbf{Team:} The Outliers\\[0.3cm]}',
            r'{\large\textbf{Institution:} BITS Pilani\\[0.3cm]}',
            r'{\large\textbf{Course:} Advanced Apex Project 1\\[0.3cm]}',
            r'',
            r'\vfill',
            r'{\large Generated: ' + datetime.now().strftime('%B %d, %Y') + r'}',
            r'\end{titlepage}',
            r'',
            r'\tableofcontents',
            r'\newpage',
            r'',
        ])

        # Process each cell
        cell_count = self.nb_controller.get_cell_count()
        code_cell_num = 0

        for i in range(cell_count):
            cell = self.nb_controller.view_cell(i, show_output=False)
            cell_type = cell['cell_type']
            source = ''.join(cell.get('source', []))

            if cell_type == 'markdown':
                # Add markdown content
                if source.strip():
                    latex_content = self.markdown_to_latex(source)
                    latex_lines.append(latex_content)
                    latex_lines.append('')

            elif cell_type == 'code':
                code_cell_num += 1

                # Add code block
                if source.strip():
                    latex_lines.append(r'\subsubsection*{Code Cell ' + str(code_cell_num) + '}')
                    latex_lines.append(r'\begin{lstlisting}[language=Python]')
                    latex_lines.append(source)
                    latex_lines.append(r'\end{lstlisting}')
                    latex_lines.append('')

                # Add outputs
                outputs = cell.get('outputs', [])
                if outputs:
                    latex_lines.append(r'\textbf{Output:}')
                    latex_lines.append('')

                    for output in outputs:
                        output_latex = self.process_output(output)
                        if output_latex:
                            latex_lines.append(output_latex)
                            latex_lines.append('')

                latex_lines.append(r'\vspace{0.5cm}')
                latex_lines.append('')

        # Document footer
        latex_lines.extend([
            r'\end{document}',
        ])

        # Save LaTeX file
        tex_file = self.work_dir / 'document.tex'
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(latex_lines))

        print(f"   ✓ LaTeX file created: {tex_file}")
        print(f"   ✓ Processed {cell_count} cells ({code_cell_num} code cells)")
        print(f"   ✓ Extracted {self.image_counter} images")

        return tex_file

    def compile_pdf(self, tex_file):
        """Compile LaTeX to PDF using pdflatex."""
        print("\n📝 Compiling PDF...")

        # Run pdflatex twice for proper references
        for run in range(2):
            print(f"   Running pdflatex (pass {run + 1}/2)...")

            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file.name],
                cwd=self.work_dir,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"   ⚠️  pdflatex warnings/errors (pass {run + 1}):")
                # Show last 20 lines of output
                lines = result.stdout.split('\n')
                for line in lines[-20:]:
                    if line.strip():
                        print(f"      {line}")

        # Check if PDF was created
        pdf_file = self.work_dir / 'document.pdf'
        if pdf_file.exists():
            # Move to final location
            import shutil
            shutil.copy(pdf_file, self.output_pdf_path)
            print(f"\n✅ PDF created successfully: {self.output_pdf_path}")
            print(f"   Size: {self.output_pdf_path.stat().st_size / 1024 / 1024:.2f} MB")
            return True
        else:
            print(f"\n❌ PDF compilation failed!")
            print(f"   Check log file: {self.work_dir / 'document.log'}")
            return False

    def cleanup(self, keep_temp=False):
        """Clean up temporary files."""
        if not keep_temp:
            print("\n🧹 Cleaning up temporary files...")
            import shutil
            try:
                shutil.rmtree(self.work_dir)
                print("   ✓ Temporary files removed")
            except Exception as e:
                print(f"   ⚠️  Could not remove temp files: {e}")

    def convert(self, keep_temp=False):
        """Run the full conversion process."""
        print("\n" + "="*70)
        print("NOTEBOOK TO PDF CONVERTER")
        print("="*70)

        try:
            # Load notebook
            self.load_notebook()

            # Generate LaTeX
            tex_file = self.generate_latex()

            # Compile to PDF
            success = self.compile_pdf(tex_file)

            # Cleanup
            if success:
                self.cleanup(keep_temp=keep_temp)

            print("\n" + "="*70)
            if success:
                print("✅ CONVERSION COMPLETED SUCCESSFULLY")
            else:
                print("❌ CONVERSION FAILED")
            print("="*70 + "\n")

            return success

        except Exception as e:
            print(f"\n❌ Error during conversion: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert Jupyter notebook to PDF with all outputs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert notebook to PDF
  python notebook_to_pdf.py notebook.ipynb output.pdf

  # Keep temporary files for debugging
  python notebook_to_pdf.py notebook.ipynb output.pdf --keep-temp

  # Using full paths
  python notebook_to_pdf.py notebooks/analysis.ipynb reports/analysis.pdf
        """
    )

    parser.add_argument('notebook', help='Path to .ipynb file')
    parser.add_argument('output', help='Path for output PDF file')
    parser.add_argument('--keep-temp', action='store_true',
                       help='Keep temporary files for debugging')

    args = parser.parse_args()

    # Check if pdflatex is available
    try:
        result = subprocess.run(['pdflatex', '--version'],
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Error: pdflatex is not installed!")
            print("\nPlease install LaTeX:")
            print("  Ubuntu/Debian: sudo apt-get install texlive-full")
            print("  macOS: brew install --cask mactex")
            print("  Or: sudo apt-get install texlive-latex-extra texlive-fonts-recommended")
            sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: pdflatex is not installed!")
        print("\nPlease install LaTeX:")
        print("  Ubuntu/Debian: sudo apt-get install texlive-full")
        print("  macOS: brew install --cask mactex")
        print("  Or: sudo apt-get install texlive-latex-extra texlive-fonts-recommended")
        sys.exit(1)

    # Create converter and run
    converter = NotebookToPDFConverter(args.notebook, args.output)
    success = converter.convert(keep_temp=args.keep_temp)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
