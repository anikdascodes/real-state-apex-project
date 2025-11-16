#!/usr/bin/env python3
"""
Phase 1 PDF Generator - Comprehensive Educational Guide
Generates professional PDF for Phase 1: Data Acquisition (Cells 1-28)
"""

import json
from pathlib import Path
from datetime import datetime
import base64
import re

# ============================================================================
# CELL EXPLANATIONS DATABASE
# ============================================================================

CELL_EXPLANATIONS = {
    10: {  # Load dataset
        "what": "Loads the Ames Housing dataset from a CSV file into a pandas DataFrame for analysis.",
        "why": "Can't analyze data without loading it first! CSV is standard format for tabular data.",
        "code_breakdown": [
            ("data_path = '../data/AmesHousing.csv'", "Sets the file path where our data is stored"),
            ("df = pd.read_csv(data_path)", "Reads CSV file and creates DataFrame (table structure)"),
            ("print('✓ Dataset loaded successfully')", "Confirms file was read without errors"),
        ],
        "output_meaning": "Confirms the CSV file was found and loaded correctly into memory.",
        "qa": [
            ("Why pandas instead of Excel?", "Pandas handles large datasets better (1000s of rows), automates analysis, and integrates seamlessly with ML libraries."),
            ("What if file path is wrong?", "You'll get 'FileNotFoundError' - verify the path is correct relative to notebook location."),
            ("What is a DataFrame?", "A table-like structure (rows and columns) that makes data manipulation easy. Think Excel spreadsheet in Python."),
        ]
    },

    12: {  # Display shape
        "what": "Shows the dimensions of our dataset: how many houses (rows) and how many features (columns).",
        "why": "Gives us a quick understanding of dataset size before diving into analysis.",
        "code_breakdown": [
            ("df.shape", "Returns tuple: (number of rows, number of columns)"),
        ],
        "output_meaning": "(2930, 82) means 2,930 houses with 82 features each. That's 240,060 data points total!",
        "qa": [
            ("Is 2,930 houses enough data?", "Yes! For machine learning, 2,000+ samples is generally good. More data = better model accuracy."),
            ("Why 82 features?", "Each feature describes something about the house (size, quality, location, etc.). More features can improve predictions but also add complexity."),
        ]
    },

    14: {  # Display first few rows
        "what": "Shows the first 5 rows of the dataset to see what the actual data looks like.",
        "why": "Lets us visually inspect data structure, column names, and sample values before processing.",
        "code_breakdown": [
            ("df.head()", "Returns first 5 rows by default (can specify different number)"),
        ],
        "output_meaning": "A table showing 5 houses with all their features. Each row = one house. Each column = one attribute.",
        "qa": [
            ("Why only 5 rows?", "Gives a quick preview without overwhelming output. For deeper inspection, use head(20) or head(50)."),
            ("What do column names mean?", "They describe house attributes: 'Gr Liv Area' = above ground living area, 'Sale Price' = final price, etc."),
        ]
    },

    16: {  # Display column names
        "what": "Lists all 82 column (feature) names in our dataset.",
        "why": "Need to know what features are available before selecting which ones to use for predictions.",
        "code_breakdown": [
            ("df.columns.tolist()", "Extracts column names and converts to a list"),
        ],
        "output_meaning": "Complete inventory of all available features, from 'Order' to 'SalePrice'.",
        "qa": [
            ("Do we use all 82 features?", "No! Later we'll remove irrelevant ones (like 'Order' which is just an ID number) and handle missing values."),
            ("How to remember what each means?", "The data dictionary (in Phase 1) explains each feature. We'll focus on the most important ones."),
        ]
    },

    18: {  # Display data types
        "what": "Shows the data type of each column (integer, float, object/text).",
        "why": "Machine learning models need numerical data. This helps identify which columns need conversion.",
        "code_breakdown": [
            ("df.dtypes", "Returns data type for each column"),
        ],
        "output_meaning": "Shows whether each feature is numerical (int64, float64) or text (object). Text features need encoding later.",
        "qa": [
            ("What's the difference between int64 and float64?", "int64 = whole numbers (1, 2, 3). float64 = decimals (1.5, 2.7). Both are numerical."),
            ("What is 'object' type?", "Text/string data like 'Brick', 'Colonial', 'Residential'. Can't feed text directly into math models."),
            ("Why does this matter?", "Models only understand numbers. Text features must be converted (encoded) to numbers first."),
        ]
    },

    20: {  # Display basic statistics
        "what": "Generates summary statistics (count, mean, std dev, min, max, quartiles) for all numerical columns.",
        "why": "Provides bird's-eye view of data distribution, helps spot outliers and understand value ranges.",
        "code_breakdown": [
            ("df.describe()", "Calculates 8 statistical measures for each numerical column"),
        ],
        "output_meaning": "For each numerical feature, shows: count (non-null values), mean (average), std (spread), min/max (range), and quartiles (25%, 50%, 75%).",
        "qa": [
            ("What are quartiles?", "25% = 25% of values are below this. 50% = median (middle value). 75% = 75% of values are below this."),
            ("Why is mean different from 50%?", "Mean is average (sum ÷ count). 50% is median (middle value). If data is skewed, they differ."),
            ("What is 'std'?", "Standard deviation - measures spread. High std = values vary a lot. Low std = values are similar."),
        ]
    },

    22: {  # Check missing values
        "what": "Counts how many missing (null/NaN) values exist in each column.",
        "why": "Missing data is a major problem - models can't handle it. Must identify before cleaning.",
        "code_breakdown": [
            ("df.isnull().sum()", "For each column, counts True values (missing = True)"),
            (".sort_values(ascending=False)", "Sorts columns by missing count (highest first)"),
        ],
        "output_meaning": "Shows which features have missing data and how many values are missing. Some columns have 0, others have hundreds or thousands.",
        "qa": [
            ("Why is data missing?", "Various reasons: not applicable (no pool = no pool quality), not recorded, data collection errors."),
            ("Can we just delete rows with missing values?", "No! We'd lose most of our data. Better to use imputation (fill with reasonable values) or drop only columns with >50% missing."),
            ("What's NaN?", "'Not a Number' - standard way to represent missing numerical values in pandas."),
        ]
    },

    24: {  # Summary statistics detailed
        "what": "Comprehensive summary statistics broken down by data type and displayed in organized sections.",
        "why": "Provides detailed statistical overview separated by numerical vs categorical features for better understanding.",
        "code_breakdown": [
            ("df.describe()", "Calculates statistics for numerical features"),
            ("df.describe(include=['object'])", "Calculates statistics for categorical (text) features"),
        ],
        "output_meaning": "Shows statistical summaries for both numerical features (mean, std, quartiles) and categorical features (count, unique values, top value, frequency).",
        "qa": [
            ("What's the difference between numerical and categorical stats?", "Numerical: mean, std dev make sense. Categorical: we see most common values and how many unique categories exist."),
            ("Why separate them?", "Different types of features need different analysis methods. Can't calculate 'average' of text categories!"),
        ]
    },
}

EDUCATIONAL_EXPLANATIONS = {
    25: {  # Understanding Summary Statistics
        "topic": "Summary Statistics",
        "what": "Summary statistics are numerical measures that describe the main characteristics of a dataset in a concise way.",
        "why": [
            "Get a 'bird's eye view' of the data without looking at every single value",
            "Quickly spot unusual patterns or potential problems",
            "Compare different features on the same scale",
            "Make informed decisions about data cleaning and preprocessing",
        ],
        "formulas": [
            {
                "name": "Mean (Average)",
                "latex": r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i",
                "symbols": {
                    "x̄": "Mean (average value)",
                    "n": "Total number of values",
                    "xᵢ": "Each individual value",
                    "Σ": "Sum of all values",
                },
                "plain_english": "Add all values together, then divide by how many values you have.",
                "example": {
                    "data": "House prices: $150K, $160K, $170K, $180K, $190K",
                    "calculation": "($150K + $160K + $170K + $180K + $190K) ÷ 5 = $850K ÷ 5 = $170K",
                    "result": "Mean price = $170K",
                }
            },
            {
                "name": "Standard Deviation",
                "latex": r"\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}",
                "symbols": {
                    "σ": "Standard deviation (spread)",
                    "n": "Total number of values",
                    "xᵢ": "Each individual value",
                    "x̄": "Mean value",
                },
                "plain_english": "Measures how spread out the values are from the average. High = lots of variation, Low = values are similar.",
                "example": {
                    "data": "Prices: $150K, $160K, $170K, $180K, $190K (Mean = $170K)",
                    "calculation": "Step 1: Find differences from mean: -20, -10, 0, 10, 20\nStep 2: Square them: 400, 100, 0, 100, 400\nStep 3: Average: (400+100+0+100+400)÷5 = 200\nStep 4: Square root: √200 ≈ 14.14",
                    "result": "Standard Deviation ≈ $14,140",
                }
            },
        ],
        "real_world_meaning": {
            "For Ames Housing": "We see that SalePrice has mean ~$180K and std ~$80K. This tells us most houses are between $100K-$260K, with some outliers.",
            "Quartiles help too": "Q1=$130K, Q2(median)=$160K, Q3=$213K means 50% of houses cost between $130K-$213K.",
        },
    },

    27: {  # Understanding Missing Values
        "topic": "Missing Values",
        "what": "Missing values (also called NaN, null, or empty cells) are data points that weren't recorded or don't apply.",
        "why": [
            "Machine learning models cannot handle missing values - they'll throw errors",
            "Missing data can introduce bias if not handled correctly",
            "Understanding WHY data is missing helps choose the right solution",
            "Large amounts of missing data might indicate a useless feature",
        ],
        "types_of_missingness": [
            {
                "type": "MCAR (Missing Completely At Random)",
                "explanation": "Data is missing for random reasons, unrelated to the data itself.",
                "example": "Survey responses lost due to computer glitch - happens randomly to any respondent.",
                "solution": "Safe to impute (fill with mean/median) or delete rows - no bias introduced.",
            },
            {
                "type": "MAR (Missing At Random)",
                "explanation": "Missingness is related to other observed variables, but not the missing value itself.",
                "example": "Older houses more likely to have missing 'Pool Quality' because pools weren't common back then.",
                "solution": "Use group-based imputation (e.g., fill based on house age).",
            },
            {
                "type": "MNAR (Missing Not At Random)",
                "explanation": "Missingness is related to the value itself.",
                "example": "High-income people less likely to report income - the missing value IS related to the actual income.",
                "solution": "Most challenging - may need advanced techniques or accept bias.",
            },
        ],
        "our_strategy": {
            "Step 1": "Drop columns with >50% missing (too little data to trust)",
            "Step 2": "For categorical: impute with 'None' or 'Missing' category",
            "Step 3": "For numerical: impute with 0, mean, or median depending on feature",
            "Step 4": "Special case (Lot Frontage): use neighborhood median (grouped imputation)",
        },
        "decision_rules": [
            ("Missing > 50%", "DROP the column entirely", "Not enough data to be useful"),
            ("Missing < 5%", "IMPUTE safely", "So few missing that method doesn't matter much"),
            ("Missing 5-50%", "ANALYZE carefully", "Understand why it's missing before choosing method"),
        ],
    },
}

# ============================================================================
# HTML TEMPLATE WITH CSS
# ============================================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ames Housing - Phase 1: Data Acquisition - Complete Guide</title>
    <style>
        @page {
            size: A4;
            margin: 2cm 1.5cm;
            @top-center {
                content: "Ames Housing Price Prediction - Phase 1";
                font-size: 10pt;
                color: #666;
            }
            @bottom-right {
                content: "Page " counter(page);
                font-size: 10pt;
                color: #666;
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: white;
        }

        .cover-page {
            text-align: center;
            padding: 100px 50px;
            page-break-after: always;
        }

        .cover-page h1 {
            font-size: 36pt;
            color: #2c3e50;
            margin-bottom: 20px;
            font-weight: bold;
        }

        .cover-page h2 {
            font-size: 24pt;
            color: #3498db;
            margin-bottom: 40px;
        }

        .cover-page .subtitle {
            font-size: 16pt;
            color: #7f8c8d;
            margin: 30px 0;
            line-height: 1.8;
        }

        .cover-page .metadata {
            font-size: 12pt;
            color: #95a5a6;
            margin-top: 60px;
        }

        .toc {
            page-break-after: always;
            padding: 30px;
        }

        .toc h2 {
            font-size: 24pt;
            color: #2c3e50;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }

        .toc ul {
            list-style: none;
        }

        .toc li {
            padding: 8px 0;
            border-bottom: 1px dotted #ddd;
        }

        .toc a {
            text-decoration: none;
            color: #2980b9;
        }

        .guide-section {
            padding: 30px;
            page-break-after: always;
        }

        .guide-section h2 {
            font-size: 20pt;
            color: #2c3e50;
            margin-bottom: 20px;
        }

        .guide-section ul {
            margin-left: 30px;
            margin-top: 15px;
        }

        .guide-section li {
            margin: 10px 0;
        }

        .cell-block {
            margin: 30px 0;
            page-break-inside: avoid;
        }

        .cell-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            font-size: 14pt;
            font-weight: bold;
        }

        .cell-header.markdown {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }

        .cell-header.educational {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }

        .info-box {
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 15px 20px;
            margin: 15px 0;
            background: #ebf5fb;
        }

        .info-box h3 {
            color: #2874a6;
            margin-bottom: 10px;
            font-size: 13pt;
        }

        .why-box {
            border: 2px solid #27ae60;
            border-radius: 8px;
            padding: 15px 20px;
            margin: 15px 0;
            background: #eafaf1;
        }

        .why-box h3 {
            color: #1e8449;
            margin-bottom: 10px;
            font-size: 13pt;
        }

        .code-block {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 0 0 8px 8px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
            line-height: 1.5;
            overflow-x: auto;
        }

        .code-block pre {
            margin: 0;
            white-space: pre-wrap;
        }

        .code-line {
            margin: 3px 0;
        }

        .line-number {
            display: inline-block;
            width: 30px;
            color: #95a5a6;
            margin-right: 15px;
            text-align: right;
        }

        .breakdown-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }

        .breakdown-table th {
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }

        .breakdown-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }

        .breakdown-table tr:nth-child(even) {
            background: #f8f9fa;
        }

        .output-box {
            background: #f8f9fa;
            border-left: 4px solid #9b59b6;
            padding: 15px 20px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }

        .output-box h3 {
            color: #8e44ad;
            margin-bottom: 10px;
            font-family: 'Segoe UI', sans-serif;
            font-size: 12pt;
        }

        .qa-section {
            background: #fff8e1;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }

        .qa-section h3 {
            color: #f39c12;
            margin-bottom: 15px;
            font-size: 13pt;
        }

        .qa-item {
            margin: 15px 0;
        }

        .qa-question {
            color: #d68910;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .qa-answer {
            color: #5d4037;
            margin-left: 20px;
        }

        .formula-box {
            background: white;
            border: 2px solid #9b59b6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }

        .formula-box h4 {
            color: #8e44ad;
            margin-bottom: 15px;
            font-size: 12pt;
        }

        .formula {
            text-align: center;
            font-size: 14pt;
            margin: 20px 0;
            padding: 15px;
            background: #f5eef8;
            border-radius: 5px;
        }

        .symbols-table {
            width: 100%;
            margin: 15px 0;
        }

        .symbols-table td {
            padding: 8px;
            border-bottom: 1px solid #e8daef;
        }

        .symbols-table td:first-child {
            font-weight: bold;
            color: #8e44ad;
            width: 100px;
        }

        .example-box {
            background: #e8f8f5;
            border-left: 4px solid #16a085;
            padding: 15px;
            margin: 15px 0;
        }

        .example-box h5 {
            color: #138d75;
            margin-bottom: 10px;
        }

        .markdown-content {
            padding: 20px;
            line-height: 1.8;
        }

        .markdown-content h1 {
            font-size: 22pt;
            color: #2c3e50;
            margin: 20px 0 15px 0;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }

        .markdown-content h2 {
            font-size: 18pt;
            color: #34495e;
            margin: 18px 0 12px 0;
        }

        .markdown-content h3 {
            font-size: 14pt;
            color: #5d6d7e;
            margin: 15px 0 10px 0;
        }

        .markdown-content ul {
            margin-left: 30px;
            margin-top: 10px;
        }

        .markdown-content li {
            margin: 8px 0;
        }

        .markdown-content strong {
            color: #2c3e50;
        }

        .highlight {
            background: #fff9c4;
            padding: 2px 5px;
            border-radius: 3px;
        }

        .key-point {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 15px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
{content}
</body>
</html>
"""

# ============================================================================
# GENERATOR CLASS
# ============================================================================

class Phase1PDFGenerator:
    def __init__(self, notebook_path):
        self.notebook_path = Path(notebook_path)
        with open(self.notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)
        self.cells = self.notebook['cells']
        self.phase1_cells = self.cells[0:28]  # Cells 1-28

    def generate_html(self):
        """Generate complete HTML content"""
        content_parts = []

        # Cover page
        content_parts.append(self.generate_cover_page())

        # Table of contents
        content_parts.append(self.generate_toc())

        # How to use guide
        content_parts.append(self.generate_guide())

        # Process each cell
        for idx, cell in enumerate(self.phase1_cells):
            cell_number = idx + 1
            cell_type = cell['cell_type']

            if cell_type == 'markdown':
                # Check if educational
                source = ''.join(cell.get('source', []))
                if '🎓 Understanding' in source:
                    content_parts.append(self.generate_educational_cell(cell_number, source))
                else:
                    content_parts.append(self.generate_markdown_cell(cell_number, source))
            elif cell_type == 'code':
                content_parts.append(self.generate_code_cell(cell_number, cell))

        # Wrap in HTML template
        full_html = HTML_TEMPLATE.replace('{content}', '\n'.join(content_parts))
        return full_html

    def generate_cover_page(self):
        """Generate cover page"""
        return f"""
<div class="cover-page">
    <h1>🏠 Ames Housing Price Prediction</h1>
    <h2>Phase 1: Data Acquisition & Exploration</h2>
    <div class="subtitle">
        <strong>Complete Educational Guide</strong><br>
        Comprehensive cell-by-cell explanation with code breakdowns,<br>
        mathematical formulas, and Q&A for all team members
    </div>
    <div class="metadata">
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p><strong>Cells Covered:</strong> 1-28 (Data Acquisition Phase)</p>
        <p><strong>Total Pages:</strong> ~40-45 pages</p>
    </div>
</div>
"""

    def generate_toc(self):
        """Generate table of contents"""
        toc_items = []

        for idx, cell in enumerate(self.phase1_cells):
            cell_number = idx + 1
            cell_type = cell['cell_type']
            source = ''.join(cell.get('source', []))

            if cell_type == 'markdown':
                # Extract first header or first line
                if '🎓 Understanding' in source:
                    topic = source.split('🎓 Understanding')[1].split('\n')[0].strip()
                    title = f"🎓 Understanding {topic}"
                else:
                    first_line = source.strip().split('\n')[0]
                    title = first_line.replace('#', '').replace('*', '').strip()[:60]
            else:  # code
                # Get explanation title if available
                if cell_number in CELL_EXPLANATIONS:
                    title = f"CODE: {CELL_EXPLANATIONS[cell_number]['what'][:50]}..."
                else:
                    title = f"Code Cell {cell_number}"

            toc_items.append(f'<li>Cell {cell_number:02d}: {title}</li>')

        return f"""
<div class="toc">
    <h2>📚 Table of Contents</h2>
    <ul>
        {''.join(toc_items)}
    </ul>
</div>
"""

    def generate_guide(self):
        """Generate how-to-use guide"""
        return """
<div class="guide-section">
    <h2>📖 How to Use This Guide</h2>

    <h3>🎯 Who Is This For?</h3>
    <ul>
        <li><strong>Non-Coders:</strong> Every step is explained in plain English with real-world analogies</li>
        <li><strong>Coders:</strong> Mathematical formulas and technical details are included</li>
        <li><strong>Team Members:</strong> Use this to understand what was done and answer stakeholder questions confidently</li>
    </ul>

    <h3>🔍 What You'll Find</h3>
    <ul>
        <li><strong>📘 WHAT boxes:</strong> Plain English explanation of what the code does</li>
        <li><strong>🎯 WHY boxes:</strong> Business justification - why this step matters</li>
        <li><strong>💻 Code Breakdown:</strong> Line-by-line explanation for every code cell</li>
        <li><strong>📊 Output Meaning:</strong> What the results tell us</li>
        <li><strong>❓ Q&A Sections:</strong> Common questions answered</li>
        <li><strong>📐 Mathematical Formulas:</strong> For statistical concepts (with examples)</li>
    </ul>

    <h3>🎨 Color Coding</h3>
    <ul>
        <li><strong style="color: #667eea;">Purple Headers:</strong> Code cells (executable Python)</li>
        <li><strong style="color: #f5576c;">Pink Headers:</strong> Markdown cells (documentation)</li>
        <li><strong style="color: #00f2fe;">Blue Headers:</strong> Educational cells (🎓 concepts explained)</li>
        <li><strong style="color: #3498db;">Blue Boxes:</strong> WHAT this does</li>
        <li><strong style="color: #27ae60;">Green Boxes:</strong> WHY we do this</li>
        <li><strong style="color: #f39c12;">Yellow Boxes:</strong> Q&A sections</li>
    </ul>

    <h3>💡 Tips for Reading</h3>
    <ul>
        <li>Read sequentially - each cell builds on previous ones</li>
        <li>Don't skip the educational cells (🎓) - they explain complex concepts</li>
        <li>Code cells show actual Python code + explanations</li>
        <li>Formulas are nice-to-know but not required for understanding</li>
        <li>Use Q&A sections to prepare for stakeholder questions</li>
    </ul>
</div>
"""

    def generate_markdown_cell(self, cell_number, source):
        """Generate HTML for markdown cell"""
        # Basic markdown to HTML (simplified)
        html_content = source

        # Convert headers
        html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)

        # Convert bold
        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)

        # Convert lists
        html_content = re.sub(r'^\- (.*?)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'(<li>.*?</li>\n?)+', r'<ul>\g<0></ul>', html_content, flags=re.DOTALL)

        # Convert line breaks
        html_content = html_content.replace('\n\n', '</p><p>')

        return f"""
<div class="cell-block">
    <div class="cell-header markdown">Cell {cell_number} [MARKDOWN]</div>
    <div class="markdown-content">
        <p>{html_content}</p>
    </div>
</div>
"""

    def generate_code_cell(self, cell_number, cell):
        """Generate HTML for code cell with full explanation"""
        source = ''.join(cell.get('source', []))
        outputs = cell.get('outputs', [])

        # Get explanation if available
        explanation = CELL_EXPLANATIONS.get(cell_number, {})

        html_parts = []

        # Cell header
        html_parts.append(f'<div class="cell-block">')
        html_parts.append(f'<div class="cell-header">Cell {cell_number} [CODE]</div>')

        # WHAT box
        if 'what' in explanation:
            html_parts.append(f'''
<div class="info-box">
    <h3>📘 WHAT THIS CODE DOES</h3>
    <p>{explanation['what']}</p>
</div>
''')

        # Code block
        code_lines = source.strip().split('\n')
        code_html = '<div class="code-block"><pre>'
        for i, line in enumerate(code_lines, 1):
            code_html += f'<div class="code-line"><span class="line-number">{i}</span>{self.escape_html(line)}</div>\n'
        code_html += '</pre></div>'
        html_parts.append(code_html)

        # Line-by-line breakdown
        if 'code_breakdown' in explanation:
            html_parts.append('<table class="breakdown-table">')
            html_parts.append('<tr><th>Code</th><th>Explanation</th></tr>')
            for code, exp in explanation['code_breakdown']:
                html_parts.append(f'<tr><td><code>{self.escape_html(code)}</code></td><td>{exp}</td></tr>')
            html_parts.append('</table>')

        # WHY box
        if 'why' in explanation:
            html_parts.append(f'''
<div class="why-box">
    <h3>🎯 WHY WE DO THIS</h3>
    <p>{explanation['why']}</p>
</div>
''')

        # Output
        if outputs:
            output_text = self.extract_output_text(outputs)
            html_parts.append(f'''
<div class="output-box">
    <h3>📊 OUTPUT</h3>
    <pre>{self.escape_html(output_text[:500])}{'...' if len(output_text) > 500 else ''}</pre>
</div>
''')

            # Output meaning
            if 'output_meaning' in explanation:
                html_parts.append(f'''
<div class="key-point">
    <strong>💡 What This Output Means:</strong><br>
    {explanation['output_meaning']}
</div>
''')

        # Q&A
        if 'qa' in explanation:
            html_parts.append('<div class="qa-section">')
            html_parts.append('<h3>❓ COMMON QUESTIONS</h3>')
            for question, answer in explanation['qa']:
                html_parts.append(f'''
<div class="qa-item">
    <div class="qa-question">Q: {question}</div>
    <div class="qa-answer">A: {answer}</div>
</div>
''')
            html_parts.append('</div>')

        html_parts.append('</div>')  # Close cell-block

        return '\n'.join(html_parts)

    def generate_educational_cell(self, cell_number, source):
        """Generate HTML for educational cell with formulas"""
        explanation = EDUCATIONAL_EXPLANATIONS.get(cell_number, {})

        html_parts = []

        # Cell header
        topic = explanation.get('topic', 'Educational Content')
        html_parts.append(f'<div class="cell-block">')
        html_parts.append(f'<div class="cell-header educational">Cell {cell_number} [EDUCATIONAL]: 🎓 Understanding {topic}</div>')

        html_parts.append('<div class="markdown-content">')

        # WHAT
        if 'what' in explanation:
            html_parts.append(f'''
<div class="info-box">
    <h3>📘 WHAT IS THIS?</h3>
    <p>{explanation['what']}</p>
</div>
''')

        # WHY
        if 'why' in explanation:
            html_parts.append('<div class="why-box">')
            html_parts.append('<h3>🎯 WHY DO WE NEED THIS?</h3>')
            html_parts.append('<ul>')
            for reason in explanation['why']:
                html_parts.append(f'<li>{reason}</li>')
            html_parts.append('</ul>')
            html_parts.append('</div>')

        # Formulas
        if 'formulas' in explanation:
            for formula_data in explanation['formulas']:
                html_parts.append('<div class="formula-box">')
                html_parts.append(f'<h4>📐 {formula_data["name"]}</h4>')

                # Formula (placeholder - would need actual LaTeX rendering)
                html_parts.append(f'<div class="formula"><strong>{formula_data["latex"]}</strong></div>')

                # Plain English
                html_parts.append(f'<p><strong>In Plain English:</strong> {formula_data["plain_english"]}</p>')

                # Symbols
                if 'symbols' in formula_data:
                    html_parts.append('<table class="symbols-table">')
                    for symbol, meaning in formula_data['symbols'].items():
                        html_parts.append(f'<tr><td>{symbol}</td><td>{meaning}</td></tr>')
                    html_parts.append('</table>')

                # Example
                if 'example' in formula_data:
                    ex = formula_data['example']
                    html_parts.append('<div class="example-box">')
                    html_parts.append('<h5>🔢 Example Calculation:</h5>')
                    html_parts.append(f'<p><strong>Data:</strong> {ex.get("data", "")}</p>')
                    html_parts.append(f'<p><strong>Calculation:</strong><br>{ex.get("calculation", "").replace(chr(10), "<br>")}</p>')
                    html_parts.append(f'<p><strong>Result:</strong> {ex.get("result", "")}</p>')
                    html_parts.append('</div>')

                html_parts.append('</div>')  # Close formula-box

        # Real-world meaning
        if 'real_world_meaning' in explanation:
            html_parts.append('<div class="key-point">')
            html_parts.append('<h3>💡 Real-World Meaning</h3>')
            for key, value in explanation['real_world_meaning'].items():
                html_parts.append(f'<p><strong>{key}:</strong> {value}</p>')
            html_parts.append('</div>')

        # Types (for missing values)
        if 'types_of_missingness' in explanation:
            for type_data in explanation['types_of_missingness']:
                html_parts.append(f'''
<div class="formula-box">
    <h4>{type_data["type"]}</h4>
    <p><strong>Explanation:</strong> {type_data["explanation"]}</p>
    <p><strong>Example:</strong> {type_data["example"]}</p>
    <p><strong>Solution:</strong> {type_data["solution"]}</p>
</div>
''')

        # Strategy
        if 'our_strategy' in explanation:
            html_parts.append('<div class="key-point">')
            html_parts.append('<h3>✅ Our Strategy</h3>')
            for step, action in explanation['our_strategy'].items():
                html_parts.append(f'<p><strong>{step}:</strong> {action}</p>')
            html_parts.append('</div>')

        # Decision rules
        if 'decision_rules' in explanation:
            html_parts.append('<table class="breakdown-table">')
            html_parts.append('<tr><th>Condition</th><th>Action</th><th>Reasoning</th></tr>')
            for condition, action, reasoning in explanation['decision_rules']:
                html_parts.append(f'<tr><td>{condition}</td><td>{action}</td><td>{reasoning}</td></tr>')
            html_parts.append('</table>')

        html_parts.append('</div>')  # Close markdown-content
        html_parts.append('</div>')  # Close cell-block

        return '\n'.join(html_parts)

    def escape_html(self, text):
        """Escape HTML special characters"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

    def extract_output_text(self, outputs):
        """Extract text from output cells"""
        text_parts = []
        for output in outputs:
            if output.get('output_type') == 'stream':
                text_parts.append(''.join(output.get('text', [])))
            elif output.get('output_type') == 'execute_result':
                data = output.get('data', {})
                if 'text/plain' in data:
                    text_parts.append(''.join(data['text/plain']))
        return '\n'.join(text_parts)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*80)
    print("PHASE 1 PDF GENERATION")
    print("="*80)
    print()

    # Initialize generator
    notebook_path = Path('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb')
    generator = Phase1PDFGenerator(notebook_path)

    print(f"✓ Loaded notebook: {notebook_path}")
    print(f"✓ Phase 1 cells: 1-28 ({len(generator.phase1_cells)} cells)")
    print()

    # Generate HTML
    print("⏳ Generating HTML content...")
    html_content = generator.generate_html()

    # Save HTML
    output_dir = Path('detail_documentation')
    output_dir.mkdir(exist_ok=True)

    html_path = output_dir / 'Phase1_Complete_Guide.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✓ HTML generated: {html_path}")
    print(f"  Size: {len(html_content):,} bytes")
    print()

    # Convert to PDF using weasyprint
    try:
        from weasyprint import HTML

        print("⏳ Converting to PDF (this may take a minute)...")
        pdf_path = output_dir / 'Phase1_Complete_Guide.pdf'
        HTML(string=html_content).write_pdf(pdf_path)

        print(f"✓ PDF generated: {pdf_path}")
        print(f"  Size: {pdf_path.stat().st_size / 1024 / 1024:.2f} MB")
        print()

        print("="*80)
        print("✅ PHASE 1 PDF GENERATION COMPLETE!")
        print("="*80)
        print()
        print(f"📄 Output files:")
        print(f"   HTML: {html_path}")
        print(f"   PDF:  {pdf_path}")
        print()
        print("🎯 Next steps:")
        print("   1. Open the PDF to review format and content")
        print("   2. Verify all cells are properly explained")
        print("   3. Check formulas and code breakdowns")
        print("   4. If approved, we'll generate the complete PDF (all 94 cells)")
        print()

    except ImportError:
        print("⚠️  weasyprint not installed")
        print("   HTML file generated successfully")
        print(f"   You can open {html_path} in a browser and print to PDF")
        print()
        print("   To install weasyprint: pip install weasyprint")
        print()

if __name__ == '__main__':
    main()
