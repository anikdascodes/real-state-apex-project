# Notebook to PDF Converter

Professional PDF generation from Jupyter notebooks with all outputs, images, and analysis preserved.

## Features

✅ **Complete Content Extraction**
- All markdown content with headers, lists, formatting
- All code cells with syntax highlighting
- All outputs (text, numerical, tables)
- All images (matplotlib plots, charts, graphs)
- Error outputs

✅ **Professional Formatting**
- Clean, modern design
- Proper page breaks
- Styled code blocks
- Embedded images
- Responsive tables
- Color-coded outputs

✅ **Multiple Output Formats**
- PDF (primary output)
- HTML (intermediate format, can be viewed in browser)

✅ **Easy to Use**
- Single command execution
- No LaTeX required (uses HTML + weasyprint)
- Automatic image extraction and embedding
- Clean temporary file management

## Installation

### Requirements

```bash
# Install weasyprint for PDF generation
pip install weasyprint

# Or using uv (project standard)
uv pip install weasyprint
```

### Alternative PDF Generators (if weasyprint fails)

```bash
# Option 1: wkhtmltopdf
sudo apt-get install wkhtmltopdf

# Option 2: Use Chrome/Chromium (usually pre-installed)
# No installation needed - script will detect automatically
```

## Usage

### Basic Usage

```bash
# Convert notebook to PDF
python automation/pdf_export/notebook_to_html_pdf.py notebook.ipynb output.pdf
```

### With Project Notebook

```bash
# Generate analysis report PDF
python automation/pdf_export/notebook_to_html_pdf.py \
    notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb \
    reports/Ames_Housing_Analysis_Report.pdf
```

### Keep Temporary Files (for debugging)

```bash
# Keep HTML and images for inspection
python automation/pdf_export/notebook_to_html_pdf.py \
    notebook.ipynb output.pdf --keep-temp
```

## Output Structure

### PDF Document Includes:

1. **Title Page**
   - Project title
   - Team information
   - Institution details
   - Generation date

2. **All Markdown Content**
   - Headers (H1-H4)
   - Formatted text (bold, italic)
   - Lists and bullet points
   - Horizontal rules

3. **All Code Cells**
   - Syntax-highlighted Python code
   - Cell numbers for reference
   - Clean, readable formatting

4. **All Outputs**
   - Text output (print statements, results)
   - Numerical data (calculations, statistics)
   - DataFrames and tables
   - Matplotlib plots and charts
   - Error messages (if any)

5. **All Images**
   - Extracted from base64
   - Embedded in PDF
   - Properly scaled
   - Centered with borders

## Examples

### Example 1: Generate Project Report

```bash
python automation/pdf_export/notebook_to_html_pdf.py \
    notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb \
    reports/Final_Analysis_Report.pdf
```

**Output:**
```
📓 Notebook: Ames_Housing_Price_Prediction_EXECUTED.ipynb
📄 Output PDF: reports/Final_Analysis_Report.pdf
📁 Working directory: reports/pdf_export_temp

======================================================================
NOTEBOOK TO PDF CONVERTER (HTML-based)
======================================================================

📖 Loading notebook...
   ✓ Loaded 81 cells

🔧 Generating HTML document...
   💾 Saved image: image_001.png
   💾 Saved image: image_002.png
   [... images 3-11 ...]
   ✓ HTML file created: reports/pdf_export_temp/document.html
   ✓ Processed 81 cells (42 code cells)
   ✓ Extracted 11 images

📝 Compiling PDF...
   Trying weasyprint...
   Using weasyprint...

✅ PDF created successfully using weasyprint: reports/Final_Analysis_Report.pdf
   Size: 1.30 MB

🧹 Cleaning up temporary files...
   ✓ Temporary files removed

======================================================================
✅ CONVERSION COMPLETED SUCCESSFULLY
======================================================================
```

### Example 2: Debug Mode (Keep HTML)

```bash
python automation/pdf_export/notebook_to_html_pdf.py \
    notebook.ipynb report.pdf --keep-temp
```

This keeps:
- `pdf_export_temp/document.html` - HTML version (can open in browser)
- `pdf_export_temp/images/` - All extracted images

### Example 3: Batch Convert Multiple Notebooks

```bash
#!/bin/bash
# Convert all notebooks to PDF

for notebook in notebooks/*.ipynb; do
    basename=$(basename "$notebook" .ipynb)
    echo "Converting $notebook..."
    python automation/pdf_export/notebook_to_html_pdf.py \
        "$notebook" \
        "reports/${basename}_Report.pdf"
done
```

## PDF Styling

The generated PDF includes professional styling:

### Colors
- **Headers**: Dark blue (#2c3e50)
- **Code blocks**: Light gray background (#f8f9fa)
- **Code border**: Blue (#3498db)
- **Output border**: Green (#2ecc71)
- **Error boxes**: Red background (#ffe6e6)

### Fonts
- **Body**: Helvetica Neue, Arial
- **Code**: Courier New, monospace
- **Size**: 11pt (adjustable in CSS)

### Layout
- **Paper**: A4
- **Margins**: 2cm all sides
- **Page numbers**: Bottom center
- **Headers**: Project title and section

## How It Works

### Process Flow

1. **Load Notebook**
   - Uses NotebookController to read .ipynb file
   - Extracts all cells (markdown and code)

2. **Process Markdown**
   - Converts markdown to HTML
   - Handles headers, lists, formatting
   - Preserves structure

3. **Process Code Cells**
   - Syntax highlighting
   - Code block formatting
   - Cell numbering

4. **Extract Outputs**
   - Text output → `<pre>` blocks
   - Images → PNG files + `<img>` tags
   - Tables → HTML tables
   - Errors → Styled error blocks

5. **Generate HTML**
   - Combine all content
   - Add CSS styling
   - Create title page
   - Add metadata

6. **Convert to PDF**
   - Try weasyprint (best quality)
   - Fallback to wkhtmltopdf
   - Fallback to Chrome headless
   - Apply page breaks, formatting

7. **Cleanup**
   - Remove temporary files (unless --keep-temp)
   - Report statistics

## Technical Details

### Image Extraction

```python
def save_image_from_base64(self, base64_data, image_format='png'):
    """Save base64 image data to file."""
    self.image_counter += 1
    image_filename = f"image_{self.image_counter:03d}.{image_format}"
    image_path = self.images_dir / image_filename

    # Decode and save
    image_bytes = base64.b64decode(base64_data)
    with open(image_path, 'wb') as f:
        f.write(image_bytes)

    return image_path
```

### Markdown to HTML Conversion

```python
def markdown_to_html(self, markdown_text):
    """Convert markdown to HTML (simple implementation)."""
    html = markdown_text

    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Code inline
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

    return html
```

### CSS Styling

Professional CSS included for:
- Typography
- Code highlighting
- Output formatting
- Page layout
- Print optimization

## Troubleshooting

### Issue: weasyprint ImportError

**Solution**: Install weasyprint
```bash
pip install weasyprint
```

### Issue: PDF Generation Failed

**Solution**: Try alternative method
```bash
# Install wkhtmltopdf
sudo apt-get install wkhtmltopdf

# Or use Chrome (often pre-installed)
# Script will detect automatically
```

### Issue: Images Not Showing

**Solution**: Use --keep-temp to debug
```bash
python automation/pdf_export/notebook_to_html_pdf.py \
    notebook.ipynb output.pdf --keep-temp

# Check images directory
ls pdf_export_temp/images/

# Open HTML in browser to verify
firefox pdf_export_temp/document.html
```

### Issue: Large PDF Size

**Cause**: Many high-resolution images

**Solutions**:
1. Reduce image DPI in notebook (matplotlib: `dpi=72`)
2. Compress images before export
3. Use `--keep-temp` to manually optimize images

### Issue: Formatting Issues

**Solution**: Inspect HTML file
```bash
# Generate with --keep-temp
python automation/pdf_export/notebook_to_html_pdf.py \
    notebook.ipynb output.pdf --keep-temp

# Open HTML in browser
firefox pdf_export_temp/document.html

# Edit CSS in automation/pdf_export/notebook_to_html_pdf.py
# Look for get_css() method
```

## Advanced Usage

### Custom CSS Styling

Edit the `get_css()` method in `notebook_to_html_pdf.py`:

```python
def get_css(self):
    """Get CSS styles for the HTML document."""
    return """
    <style>
        /* Modify colors */
        h1 { color: #your-color; }

        /* Modify fonts */
        body { font-family: 'Your Font'; }

        /* Modify layout */
        @page { margin: 3cm; }
    </style>
    """
```

### Add Custom Header/Footer

Modify the HTML generation in `generate_html()`:

```python
# Add custom header
html_parts.append('<div class="header">Your Custom Header</div>')

# Add custom footer
html_parts.append('<div class="footer">Page {page_number}</div>')
```

## Integration

### With Automation Workflow

```python
from automation.pdf_export.notebook_to_html_pdf import NotebookToHTMLPDFConverter

# Convert notebook
converter = NotebookToHTMLPDFConverter(
    'notebooks/analysis.ipynb',
    'reports/analysis.pdf'
)
success = converter.convert(keep_temp=False)

if success:
    print("PDF generated successfully!")
```

### With CI/CD Pipeline

```yaml
# .github/workflows/generate-reports.yml
name: Generate PDF Reports

on: [push]

jobs:
  generate-pdf:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install jupyter weasyprint

      - name: Generate PDF report
        run: |
          python automation/pdf_export/notebook_to_html_pdf.py \
            notebooks/analysis.ipynb \
            reports/analysis.pdf

      - name: Upload PDF
        uses: actions/upload-artifact@v2
        with:
          name: analysis-report
          path: reports/analysis.pdf
```

## Performance

### Statistics (Ames Housing Notebook)

- **Input**: 81 cells (42 code, 39 markdown)
- **Images**: 11 plots/charts
- **Output Size**: 1.3 MB
- **Generation Time**: ~10 seconds
- **HTML Size**: ~500 KB

### Optimization Tips

1. **Reduce image count**: Combine related plots
2. **Lower DPI**: Use `plt.savefig(dpi=72)` in notebook
3. **Minimize output**: Clear unnecessary print statements
4. **Use caching**: Keep temp files for repeated generation

## Comparison

### vs. Jupyter nbconvert

| Feature | This Tool | nbconvert |
|---------|-----------|-----------|
| PDF Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Styling | Custom CSS | Limited |
| Dependencies | weasyprint | LaTeX (large) |
| Speed | Fast | Slow |
| Customization | Easy | Complex |

### vs. Manual Export

| Feature | This Tool | Manual |
|---------|-----------|--------|
| Automation | ✅ | ❌ |
| Consistency | ✅ | ❌ |
| Batch Processing | ✅ | ❌ |
| Version Control | ✅ | ❌ |

## License

Part of the Ames Housing Price Prediction automation toolkit.

## Support

For issues or questions:
- Check main automation README: `automation/README.md`
- Run with `--keep-temp` to debug
- Inspect HTML output in browser

## Version

1.0.0 - Initial release

---

**Generated PDF Example**: `reports/Ames_Housing_Analysis_Report.pdf` (1.3 MB, 81 cells, 11 images)
