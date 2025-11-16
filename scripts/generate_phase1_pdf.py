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
            margin: 2.5cm 2cm;
            @top-center {
                content: "Ames Housing Price Prediction - Phase 1: Data Acquisition";
                font-size: 9pt;
                color: #666;
            }
            @bottom-right {
                content: "Page " counter(page);
                font-size: 9pt;
                color: #666;
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            color: #000;
            background: white;
        }

        .cover-page {
            text-align: center;
            padding: 120px 50px;
            page-break-after: always;
            border-bottom: 2px solid #000;
        }

        .cover-page h1 {
            font-size: 32pt;
            color: #000;
            margin-bottom: 30px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .cover-page h2 {
            font-size: 20pt;
            color: #000;
            margin-bottom: 50px;
            font-weight: normal;
        }

        .cover-page .subtitle {
            font-size: 13pt;
            color: #333;
            margin: 40px 0;
            line-height: 2;
        }

        .cover-page .metadata {
            font-size: 11pt;
            color: #666;
            margin-top: 80px;
            line-height: 1.8;
        }

        .toc {
            page-break-after: always;
            padding: 20px 0;
        }

        .toc h2 {
            font-size: 20pt;
            color: #000;
            margin-bottom: 30px;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
        }

        .toc ul {
            list-style: none;
        }

        .toc li {
            padding: 10px 0;
            border-bottom: 1px solid #ddd;
            font-size: 11pt;
        }

        .guide-section {
            padding: 20px 0;
            page-break-after: always;
        }

        .guide-section h2 {
            font-size: 18pt;
            color: #000;
            margin-bottom: 25px;
            border-bottom: 2px solid #000;
            padding-bottom: 8px;
        }

        .guide-section h3 {
            font-size: 13pt;
            color: #000;
            margin: 20px 0 12px 0;
            font-weight: bold;
        }

        .guide-section ul {
            margin-left: 35px;
            margin-top: 12px;
        }

        .guide-section li {
            margin: 8px 0;
            font-size: 11pt;
        }

        .cell-block {
            margin: 40px 0;
            page-break-inside: avoid;
            border: 1px solid #000;
        }

        .cell-header {
            background: #f5f5f5;
            color: #000;
            padding: 12px 20px;
            font-size: 12pt;
            font-weight: bold;
            border-bottom: 2px solid #000;
            font-family: 'Arial', sans-serif;
        }

        .info-box {
            border: 1px solid #000;
            padding: 15px 20px;
            margin: 20px;
            background: white;
        }

        .info-box h3 {
            color: #000;
            margin-bottom: 10px;
            font-size: 11pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .info-box p {
            font-size: 11pt;
            line-height: 1.6;
        }

        .why-box {
            border: 1px solid #000;
            padding: 15px 20px;
            margin: 20px;
            background: white;
        }

        .why-box h3 {
            color: #000;
            margin-bottom: 10px;
            font-size: 11pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .why-box p {
            font-size: 11pt;
            line-height: 1.6;
        }

        .code-block {
            background: #f8f8f8;
            color: #000;
            padding: 15px 20px;
            margin: 20px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.6;
            border: 1px solid #ddd;
            border-left: 3px solid #000;
        }

        .code-block pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .code-line {
            margin: 1px 0;
            padding: 2px 0;
        }

        .line-number {
            display: inline-block;
            width: 30px;
            color: #999;
            margin-right: 15px;
            text-align: right;
            font-weight: normal;
            user-select: none;
        }

        .code-content {
            color: #000;
        }

        /* Syntax highlighting for Python */
        .code-comment {
            color: #6a737d;
            font-style: italic;
        }

        .code-string {
            color: #032f62;
        }

        .code-keyword {
            color: #000;
            font-weight: bold;
        }

        .code-function {
            color: #000;
        }

        .breakdown-table {
            width: calc(100% - 40px);
            border-collapse: collapse;
            margin: 20px;
            font-size: 10pt;
        }

        .breakdown-table th {
            background: #f5f5f5;
            color: #000;
            padding: 10px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #000;
        }

        .breakdown-table td {
            padding: 10px;
            border: 1px solid #ccc;
            line-height: 1.5;
        }

        .breakdown-table td:first-child {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #fafafa;
            width: 40%;
        }

        .output-box {
            background: #fafafa;
            border: 1px solid #000;
            padding: 15px 20px;
            margin: 20px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }

        .output-box h3 {
            color: #000;
            margin-bottom: 10px;
            font-family: 'Arial', sans-serif;
            font-size: 11pt;
            font-weight: bold;
        }

        .output-box pre {
            white-space: pre-wrap;
            line-height: 1.4;
        }

        .qa-section {
            background: white;
            border: 1px solid #000;
            padding: 20px;
            margin: 20px;
        }

        .qa-section h3 {
            color: #000;
            margin-bottom: 15px;
            font-size: 11pt;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .qa-item {
            margin: 15px 0;
            padding-left: 10px;
        }

        .qa-question {
            color: #000;
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 10pt;
        }

        .qa-answer {
            color: #333;
            margin-left: 15px;
            font-size: 10pt;
            line-height: 1.5;
        }

        .formula-box {
            background: white;
            border: 2px solid #000;
            padding: 20px;
            margin: 20px;
        }

        .formula-box h4 {
            color: #000;
            margin-bottom: 15px;
            font-size: 12pt;
            font-weight: bold;
        }

        .formula {
            text-align: center;
            font-size: 13pt;
            margin: 20px 0;
            padding: 20px;
            background: #fafafa;
            border: 1px solid #ccc;
            font-family: 'Times New Roman', serif;
        }

        .symbols-table {
            width: 100%;
            margin: 15px 0;
            border-collapse: collapse;
        }

        .symbols-table td {
            padding: 8px;
            border-bottom: 1px solid #ddd;
            font-size: 10pt;
        }

        .symbols-table td:first-child {
            font-weight: bold;
            color: #000;
            width: 100px;
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
        }

        .example-box {
            background: #fafafa;
            border-left: 3px solid #000;
            padding: 15px;
            margin: 15px 0;
        }

        .example-box h5 {
            color: #000;
            margin-bottom: 10px;
            font-size: 11pt;
            font-weight: bold;
        }

        .example-box p {
            font-size: 10pt;
            line-height: 1.5;
            margin: 5px 0;
        }

        .markdown-content {
            padding: 20px;
            line-height: 1.8;
        }

        .markdown-content h1 {
            font-size: 18pt;
            color: #000;
            margin: 25px 0 15px 0;
            border-bottom: 2px solid #000;
            padding-bottom: 8px;
        }

        .markdown-content h2 {
            font-size: 14pt;
            color: #000;
            margin: 20px 0 12px 0;
            font-weight: bold;
        }

        .markdown-content h3 {
            font-size: 12pt;
            color: #000;
            margin: 15px 0 10px 0;
            font-weight: bold;
        }

        .markdown-content ul {
            margin-left: 30px;
            margin-top: 10px;
        }

        .markdown-content li {
            margin: 8px 0;
            font-size: 11pt;
        }

        .markdown-content p {
            font-size: 11pt;
            margin: 10px 0;
        }

        .markdown-content strong {
            color: #000;
            font-weight: bold;
        }

        .key-point {
            background: #fafafa;
            border-left: 3px solid #000;
            padding: 15px;
            margin: 20px;
        }

        .key-point h3 {
            font-size: 11pt;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .key-point p {
            font-size: 10pt;
            line-height: 1.5;
            margin: 5px 0;
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

        # About the Dataset section
        content_parts.append(self.generate_about_dataset())

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
    <h1>AMES HOUSING PRICE PREDICTION</h1>
    <h2>Phase 1: Data Acquisition & Exploration</h2>
    <div class="subtitle">
        <strong>Complete Educational Guide</strong><br><br>
        Comprehensive cell-by-cell explanation with code breakdowns,<br>
        mathematical formulas, and Q&A for all team members
    </div>
    <div class="metadata">
        <p><strong>Document Generated:</strong> {datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
        <p><strong>Coverage:</strong> Cells 1-28 (Data Acquisition Phase)</p>
        <p><strong>Notebook:</strong> Ames_Housing_Price_Prediction_EXECUTED.ipynb</p>
    </div>
</div>
"""

    def generate_toc(self):
        """Generate table of contents with topics"""
        sections = [
            ("About the Dataset", None),
            ("", None),  # Separator
            ("SECTION 1: PROJECT INTRODUCTION", None),
            ("Project Title & Overview", 1),
            ("Team Members", 3),
            ("", None),  # Separator
            ("SECTION 2: ENVIRONMENT SETUP", None),
            ("Import Required Libraries", 8),
            ("", None),  # Separator
            ("SECTION 3: DATA LOADING", None),
            ("Load Ames Housing Dataset", 10),
            ("", None),  # Separator
            ("SECTION 4: INITIAL DATA EXPLORATION", None),
            ("Dataset Dimensions & Structure", 12),
            ("Preview First Rows", 14),
            ("Column Names & Data Types", 14),
            ("", None),  # Separator
            ("SECTION 5: DATA QUALITY ASSESSMENT", None),
            ("Comprehensive Quality Checks", 16),
            ("Schema Summary Table", 17),
            ("", None),  # Separator
            ("SECTION 6: DATA DICTIONARY", None),
            ("Data Dictionary Cross-Reference", 18),
            ("Load Data Dictionary", 19),
            ("Key Features Overview", 20),
            ("", None),  # Separator
            ("SECTION 7: SUMMARY STATISTICS", None),
            ("Comprehensive Summary Statistics", 24),
            ("Understanding Summary Statistics (Educational)", 25),
            ("", None),  # Separator
            ("SECTION 8: MISSING VALUE ANALYSIS", None),
            ("Calculate Missing Value Statistics", 28),
            ("Understanding Missing Values (Educational)", 27),
        ]

        toc_html = '<ul>'
        for title, cell_num in sections:
            if title == "":
                toc_html += '<li style="border:none; height:10px;"></li>'  # Empty separator
            elif cell_num is None:
                toc_html += f'<li style="font-weight:bold; background:#f5f5f5; margin-top:10px;">{title}</li>'
            else:
                toc_html += f'<li>Cell {cell_num:02d}: {title}</li>'
        toc_html += '</ul>'

        return f"""
<div class="toc">
    <h2>Table of Contents</h2>
    {toc_html}
</div>
"""

    def generate_about_dataset(self):
        """Generate About the Dataset section"""
        return """
<div class="guide-section">
    <h2>About the Dataset</h2>

    <h3>Ames Housing Dataset Overview</h3>
    <p>The Ames Housing dataset contains comprehensive information about residential properties sold in Ames, Iowa between 2006 and 2010. This dataset is widely used in machine learning and data science education due to its richness and real-world complexity.</p>

    <h3>Dataset Characteristics</h3>
    <ul>
        <li><strong>Total Records:</strong> 2,930 houses</li>
        <li><strong>Total Features:</strong> 82 variables (80 predictors + 2 identifiers)</li>
        <li><strong>Target Variable:</strong> SalePrice (final sale price in dollars)</li>
        <li><strong>Data Source:</strong> Ames, Iowa Assessor's Office</li>
        <li><strong>Time Period:</strong> 2006-2010</li>
    </ul>

    <h3>Feature Categories</h3>
    <p>The 82 features describe various aspects of residential homes:</p>
    <ul>
        <li><strong>Physical Characteristics:</strong> Square footage, number of rooms, building type, architectural style</li>
        <li><strong>Quality & Condition:</strong> Overall quality, material quality, condition ratings</li>
        <li><strong>Location:</strong> Neighborhood, zoning classification, proximity to features</li>
        <li><strong>Age:</strong> Year built, year remodeled</li>
        <li><strong>Lot Information:</strong> Lot size, shape, contour, configuration</li>
        <li><strong>Basement:</strong> Basement type, finish, quality, square footage</li>
        <li><strong>Garage:</strong> Type, size, quality, year built</li>
        <li><strong>Utilities & Systems:</strong> Heating, cooling, electrical, plumbing</li>
        <li><strong>External Features:</strong> Pool, fence, deck, porch</li>
        <li><strong>Sale Details:</strong> Sale type, condition, price</li>
    </ul>

    <h3>What We'll Cover in Phase 1</h3>
    <p>This document focuses on <strong>Phase 1: Data Acquisition & Initial Exploration</strong>, which includes:</p>
    <ul>
        <li><strong>Section 1:</strong> Project Introduction & Setup</li>
        <li><strong>Section 2:</strong> Importing Required Libraries</li>
        <li><strong>Section 3:</strong> Loading the Dataset</li>
        <li><strong>Section 4:</strong> Initial Data Exploration (shape, structure, columns)</li>
        <li><strong>Section 5:</strong> Data Quality Assessment</li>
        <li><strong>Section 6:</strong> Data Dictionary Reference</li>
        <li><strong>Section 7:</strong> Summary Statistics</li>
        <li><strong>Section 8:</strong> Missing Value Analysis</li>
        <li><strong>Section 9:</strong> Educational Concepts (Statistics, Missing Values)</li>
    </ul>

    <h3>Why This Dataset?</h3>
    <p>The Ames Housing dataset offers several advantages for learning and practicing data science:</p>
    <ul>
        <li><strong>Real-World Complexity:</strong> Contains missing values, outliers, and mixed data types - just like production data</li>
        <li><strong>Rich Features:</strong> 82 variables provide many opportunities for feature engineering and selection</li>
        <li><strong>Documented:</strong> Comprehensive data dictionary available with detailed feature descriptions</li>
        <li><strong>Challenging:</strong> Requires thoughtful handling of categorical variables, missing data, and outliers</li>
        <li><strong>Practical:</strong> House price prediction is relatable and has clear business value</li>
    </ul>

    <p><strong>Document Purpose:</strong> This guide explains every step of Phase 1 with code explanations, outputs, and Q&A to help team members understand the data acquisition and initial exploration process.</p>
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
