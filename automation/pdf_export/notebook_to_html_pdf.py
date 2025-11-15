#!/usr/bin/env python3
"""
Notebook to PDF Converter (HTML-based)
======================================

Converts Jupyter notebooks to professional PDF documents via HTML.
Uses weasyprint for PDF generation (no LaTeX required).

Features:
- Extracts all markdown content
- Includes all code outputs (text, numerical, tables)
- Converts and embeds all images
- Creates structured HTML document with CSS
- Converts to PDF using weasyprint

Usage:
    python notebook_to_html_pdf.py notebook.ipynb output.pdf
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


class NotebookToHTMLPDFConverter:
    """Convert Jupyter notebooks to PDF via HTML."""

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

    def markdown_to_html(self, markdown_text):
        """Convert markdown to HTML (simple implementation)."""
        if not markdown_text:
            return ""

        html = markdown_text

        # Headers
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

        # Code inline
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

        # Lists
        html = re.sub(r'^\* (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

        # Horizontal rules
        html = re.sub(r'^---+$', r'<hr/>', html, flags=re.MULTILINE)

        # Line breaks
        html = html.replace('\n\n', '<br/><br/>')

        return html

    def process_output(self, output):
        """Process a single cell output and return HTML code."""
        html_parts = []
        output_type = output.get('output_type', '')

        if output_type == 'stream':
            # Text output
            text = ''.join(output.get('text', []))
            if text.strip():
                escaped_text = text.replace('<', '&lt;').replace('>', '&gt;')
                html_parts.append(f'<pre class="output-text">{escaped_text}</pre>')

        elif output_type == 'execute_result' or output_type == 'display_data':
            data = output.get('data', {})

            # Handle images
            if 'image/png' in data:
                image_path = self.save_image_from_base64(data['image/png'], 'png')
                rel_path = image_path.relative_to(self.work_dir)
                html_parts.append(f'<div class="output-image"><img src="{rel_path}" alt="Output image"/></div>')

            # Handle text/plain output
            elif 'text/plain' in data:
                text = ''.join(data['text/plain'])
                if text.strip():
                    escaped_text = text.replace('<', '&lt;').replace('>', '&gt;')
                    html_parts.append(f'<pre class="output-text">{escaped_text}</pre>')

            # Handle HTML output
            elif 'text/html' in data:
                html = ''.join(data['text/html'])
                html_parts.append(f'<div class="output-html">{html}</div>')

        elif output_type == 'error':
            # Error output
            ename = output.get('ename', 'Error')
            evalue = output.get('evalue', '')
            html_parts.append(f'<pre class="output-error">ERROR: {ename}: {evalue}</pre>')

        return '\n'.join(html_parts)

    def get_css(self):
        """Get CSS styles for the HTML document."""
        return """
        <style>
            @page {
                size: A4;
                margin: 2cm;
            }

            body {
                font-family: 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 100%;
                margin: 0;
                padding: 20px;
            }

            .title-page {
                text-align: center;
                page-break-after: always;
                padding-top: 100px;
            }

            .title-page h1 {
                font-size: 36pt;
                color: #2c3e50;
                margin-bottom: 20px;
            }

            .title-page .subtitle {
                font-size: 18pt;
                color: #7f8c8d;
                margin: 10px 0;
            }

            .title-page .meta {
                font-size: 12pt;
                color: #95a5a6;
                margin-top: 50px;
            }

            h1 {
                color: #2c3e50;
                font-size: 24pt;
                margin-top: 30px;
                margin-bottom: 15px;
                page-break-after: avoid;
            }

            h2 {
                color: #34495e;
                font-size: 20pt;
                margin-top: 25px;
                margin-bottom: 12px;
                page-break-after: avoid;
            }

            h3 {
                color: #5d6d7e;
                font-size: 16pt;
                margin-top: 20px;
                margin-bottom: 10px;
                page-break-after: avoid;
            }

            h4 {
                color: #85929e;
                font-size: 14pt;
                margin-top: 15px;
                margin-bottom: 8px;
            }

            .cell {
                margin-bottom: 30px;
                page-break-inside: avoid;
            }

            .code-cell {
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin: 20px 0;
                page-break-inside: avoid;
            }

            .code-cell-header {
                font-weight: bold;
                color: #3498db;
                margin-bottom: 10px;
                font-size: 10pt;
            }

            pre.code {
                background-color: #fff;
                border: 1px solid #e1e8ed;
                padding: 10px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                line-height: 1.4;
            }

            .output {
                margin-top: 10px;
                padding: 10px;
                background-color: #fff;
                border-left: 4px solid #2ecc71;
            }

            .output-label {
                font-weight: bold;
                color: #2ecc71;
                margin-bottom: 5px;
                font-size: 9pt;
            }

            .output-text {
                background-color: #f8f9fa;
                padding: 10px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 9pt;
                line-height: 1.4;
                border: 1px solid #e1e8ed;
            }

            .output-image {
                text-align: center;
                margin: 15px 0;
                page-break-inside: avoid;
            }

            .output-image img {
                max-width: 100%;
                height: auto;
                border: 1px solid #e1e8ed;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .output-html {
                margin: 10px 0;
            }

            .output-html table {
                border-collapse: collapse;
                width: 100%;
                font-size: 9pt;
            }

            .output-html th,
            .output-html td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }

            .output-html th {
                background-color: #3498db;
                color: white;
            }

            .output-html tr:nth-child(even) {
                background-color: #f8f9fa;
            }

            .output-error {
                background-color: #ffe6e6;
                border: 1px solid #ff4444;
                padding: 10px;
                color: #cc0000;
                font-family: 'Courier New', monospace;
                font-size: 9pt;
            }

            hr {
                border: none;
                border-top: 2px solid #e1e8ed;
                margin: 20px 0;
            }

            strong {
                font-weight: 600;
            }

            em {
                font-style: italic;
            }

            code {
                background-color: #f8f9fa;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 9pt;
            }

            li {
                margin: 5px 0;
            }

            .page-break {
                page-break-after: always;
            }

            @media print {
                body {
                    print-color-adjust: exact;
                    -webkit-print-color-adjust: exact;
                }
            }
        </style>
        """

    def generate_html(self):
        """Generate HTML document from notebook."""
        print("\n🔧 Generating HTML document...")

        html_parts = []

        # Document header
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html>')
        html_parts.append('<head>')
        html_parts.append('<meta charset="UTF-8">')
        html_parts.append('<title>Ames Housing Price Prediction - Analysis Report</title>')
        html_parts.append(self.get_css())
        html_parts.append('</head>')
        html_parts.append('<body>')

        # Title page
        html_parts.append('<div class="title-page">')
        html_parts.append('<h1>Ames Housing Price Prediction</h1>')
        html_parts.append('<div class="subtitle">Advanced Apex Project</div>')
        html_parts.append('<div class="subtitle">Real Estate Price Modeling</div>')
        html_parts.append('<div class="meta">')
        html_parts.append('<p><strong>Team:</strong> The Outliers</p>')
        html_parts.append('<p><strong>Institution:</strong> BITS Pilani</p>')
        html_parts.append('<p><strong>Course:</strong> Advanced Apex Project 1</p>')
        html_parts.append(f'<p><strong>Generated:</strong> {datetime.now().strftime("%B %d, %Y")}</p>')
        html_parts.append('</div>')
        html_parts.append('</div>')

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
                    html_content = self.markdown_to_html(source)
                    html_parts.append(f'<div class="cell markdown-cell">{html_content}</div>')

            elif cell_type == 'code':
                code_cell_num += 1

                # Add code block
                if source.strip():
                    html_parts.append('<div class="cell code-cell">')
                    html_parts.append(f'<div class="code-cell-header">Code Cell {code_cell_num}</div>')
                    escaped_code = source.replace('<', '&lt;').replace('>', '&gt;')
                    html_parts.append(f'<pre class="code">{escaped_code}</pre>')

                    # Add outputs
                    outputs = cell.get('outputs', [])
                    if outputs:
                        html_parts.append('<div class="output">')
                        html_parts.append('<div class="output-label">Output:</div>')

                        for output in outputs:
                            output_html = self.process_output(output)
                            if output_html:
                                html_parts.append(output_html)

                        html_parts.append('</div>')

                    html_parts.append('</div>')

        # Document footer
        html_parts.append('</body>')
        html_parts.append('</html>')

        # Save HTML file
        html_file = self.work_dir / 'document.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_parts))

        print(f"   ✓ HTML file created: {html_file}")
        print(f"   ✓ Processed {cell_count} cells ({code_cell_num} code cells)")
        print(f"   ✓ Extracted {self.image_counter} images")

        return html_file

    def html_to_pdf_weasyprint(self, html_file):
        """Convert HTML to PDF using weasyprint."""
        try:
            from weasyprint import HTML
            print(f"   Using weasyprint...")
            HTML(filename=str(html_file)).write_pdf(self.output_pdf_path)
            return True
        except ImportError:
            print(f"   ⚠️  weasyprint not available")
            return False

    def html_to_pdf_wkhtmltopdf(self, html_file):
        """Convert HTML to PDF using wkhtmltopdf."""
        try:
            result = subprocess.run(
                ['wkhtmltopdf', '--enable-local-file-access', str(html_file), str(self.output_pdf_path)],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            print(f"   ⚠️  wkhtmltopdf not available")
            return False

    def html_to_pdf_chrome(self, html_file):
        """Convert HTML to PDF using Chrome headless."""
        chrome_commands = [
            'google-chrome',
            'chromium',
            'chromium-browser',
            'chrome'
        ]

        for chrome_cmd in chrome_commands:
            try:
                result = subprocess.run(
                    [chrome_cmd, '--headless', '--disable-gpu', '--print-to-pdf=' + str(self.output_pdf_path),
                     str(html_file)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0 and self.output_pdf_path.exists():
                    return True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        print(f"   ⚠️  Chrome/Chromium not available")
        return False

    def compile_pdf(self, html_file):
        """Compile HTML to PDF using available tools."""
        print("\n📝 Compiling PDF...")

        # Try different PDF generation methods
        methods = [
            ("weasyprint", self.html_to_pdf_weasyprint),
            ("wkhtmltopdf", self.html_to_pdf_wkhtmltopdf),
            ("Chrome/Chromium", self.html_to_pdf_chrome),
        ]

        for method_name, method_func in methods:
            print(f"   Trying {method_name}...")
            try:
                if method_func(html_file):
                    if self.output_pdf_path.exists():
                        print(f"\n✅ PDF created successfully using {method_name}: {self.output_pdf_path}")
                        print(f"   Size: {self.output_pdf_path.stat().st_size / 1024 / 1024:.2f} MB")
                        return True
            except Exception as e:
                print(f"   ⚠️  {method_name} failed: {e}")

        print(f"\n❌ PDF compilation failed!")
        print(f"   HTML file available at: {html_file}")
        print(f"\nPlease install one of the following:")
        print(f"  - weasyprint: pip install weasyprint")
        print(f"  - wkhtmltopdf: apt-get install wkhtmltopdf")
        print(f"  - Chrome/Chromium browser")
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
        print("NOTEBOOK TO PDF CONVERTER (HTML-based)")
        print("="*70)

        try:
            # Load notebook
            self.load_notebook()

            # Generate HTML
            html_file = self.generate_html()

            # Compile to PDF
            success = self.compile_pdf(html_file)

            # Cleanup
            if success:
                self.cleanup(keep_temp=keep_temp)
            else:
                print(f"\n💡 Tip: You can open the HTML file in a browser and print to PDF:")
                print(f"   file://{html_file.absolute()}")

            print("\n" + "="*70)
            if success:
                print("✅ CONVERSION COMPLETED SUCCESSFULLY")
            else:
                print("⚠️  PDF conversion incomplete - HTML file available")
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
        description='Convert Jupyter notebook to PDF via HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert notebook to PDF
  python notebook_to_html_pdf.py notebook.ipynb output.pdf

  # Keep temporary files for debugging
  python notebook_to_html_pdf.py notebook.ipynb output.pdf --keep-temp

  # Using full paths
  python notebook_to_html_pdf.py notebooks/analysis.ipynb reports/analysis.pdf

Requirements:
  One of the following PDF generators:
  - weasyprint: pip install weasyprint
  - wkhtmltopdf: apt-get install wkhtmltopdf
  - Chrome/Chromium browser
        """
    )

    parser.add_argument('notebook', help='Path to .ipynb file')
    parser.add_argument('output', help='Path for output PDF file')
    parser.add_argument('--keep-temp', action='store_true',
                       help='Keep temporary files (HTML, images) for debugging')

    args = parser.parse_args()

    # Create converter and run
    converter = NotebookToHTMLPDFConverter(args.notebook, args.output)
    success = converter.convert(keep_temp=args.keep_temp)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
