#!/usr/bin/env python3
"""
Generate Comprehensive Phase 1 PDF with Detailed Explanations
Creates a complete educational guide for Phase 1 (cells 1-28)
"""

import json
import base64
from pathlib import Path
from datetime import datetime

# Load notebook
nb_path = Path('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb')
with open(nb_path, 'r') as f:
    nb = json.load(f)

# Extract Phase 1 cells
phase1_cells = nb['cells'][:28]

# Cell explanations database
CELL_EXPLANATIONS = {
    8: {  # Import libraries
        "what": "Imports all necessary Python libraries for data analysis, visualization, and machine learning.",
        "why": "We need these tools before we can work with data. Each library serves a specific purpose.",
        "libraries": {
            "pandas": "Data manipulation and analysis (works with tables/DataFrames)",
            "numpy": "Numerical computing and array operations", 
            "matplotlib": "Creating static visualizations and plots",
            "seaborn": "Statistical data visualization (built on matplotlib)",
            "sklearn": "Machine learning algorithms and tools",
            "scipy": "Scientific computing and statistical functions",
            "missingno": "Visualizing missing data patterns"
        },
        "qa": [
            ("Why so many libraries?", "Each specializes in different tasks. Using the right tool makes our job easier."),
            ("Can I use different libraries?", "Yes, but these are industry standard and work well together."),
            ("Do I need all of them?", "For this complete analysis, yes. Each is used at specific steps.")
        ]
    },
    10: {  # Load dataset
        "what": "Loads the Ames Housing dataset from a CSV file into a pandas DataFrame for analysis.",
        "why": "Can't analyze data without loading it first! CSV is standard format for tabular data.",
        "code_breakdown": [
            ("data_path = '../data/AmesHousing.csv'", "Sets the file path where our data is stored"),
            ("df = pd.read_csv(data_path)", "Reads CSV file and creates DataFrame (table structure)"),
            ("print('✓ Dataset loaded successfully')", "Confirms file was read without errors"),
            ("print(f'Dataset Shape: {df.shape}')", "Shows dimensions: (rows, columns)")
        ],
        "output_meaning": {
            "✓ Dataset loaded successfully": "File found and read correctly",
            "(2930, 82)": "2,930 houses (rows) × 82 features (columns)"
        },
        "qa": [
            ("Why pandas instead of Excel?", "Pandas handles large datasets better, automates analysis, and integrates with ML libraries."),
            ("What if file path is wrong?", "You'll get 'FileNotFoundError' - verify the path is correct."),
            ("Why exactly 2,930 houses?", "This is the complete Ames, Iowa dataset - all recorded transactions.")
        ]
    },
    12: {  # df.info()
        "what": "Displays comprehensive information about the dataset structure and data types.",
        "why": "Need to understand what data we have before analyzing it.",
        "code_breakdown": [
            ("df.info()", "Shows column names, data types, non-null counts, memory usage"),
            ("df.dtypes.value_counts()", "Counts how many columns of each data type"),
            ("df.memory_usage()", "Shows memory used by each column")
        ],
        "output_meaning": {
            "RangeIndex: 2930 entries": "We have 2,930 rows (houses)",
            "Data columns: 82": "We have 82 different features/variables",
            "dtypes: int64(28), float64(11), object(43)": "28 integer columns, 11 decimal columns, 43 text columns",
            "memory usage: 1.8+ MB": "Dataset size in memory"
        },
        "qa": [
            ("What's the difference between int64 and float64?", "int64 = whole numbers (e.g., 5), float64 = decimals (e.g., 5.5)"),
            ("What does 'object' mean?", "Text/string data (like neighborhood names, categories)"),
            ("Why check this?", "Ensures data loaded correctly and helps plan next steps")
        ]
    },
    14: {  # Display columns
        "what": "Lists all 82 feature names in the dataset in an organized format.",
        "why": "Need to know what features we have available for analysis.",
        "qa": [
            ("Why 82 features?", "Real estate has many factors: size, location, quality, age, etc."),
            ("Which features matter most?", "We'll discover this through analysis - some are more important than others.")
        ]
    },
    16: {  # Quality checks
        "what": "Performs initial data quality assessment: missing values, duplicates, target variable integrity.",
        "why": "Identify data quality issues before analysis to avoid errors later.",
        "checks": [
            "Missing values count and percentage",
            "Duplicate rows check",
            "Target variable (SalePrice) check",
            "Data type verification"
        ],
        "output_meaning": {
            "Total missing values": "How many blank/NaN cells exist",
            "Columns with missing data": "How many features have missing values",
            "Percentage missing": "What proportion of data is missing",
            "Duplicate rows": "Should be 0 - each house is unique",
            "SalePrice range": "Min and max house prices"
        },
        "qa": [
            ("Is missing data bad?", "Not always - depends on how much and why. We'll handle it strategically."),
            ("Why check for duplicates?", "Duplicate houses would skew our analysis."),
            ("What's a good price range?", "$12K-$755K is realistic for Ames, Iowa housing market.")
        ]
    },
    17: {  # Schema summary
        "what": "Creates a detailed summary table of all features with data types and missing value counts.",
        "why": "Provides a quick reference for understanding each feature's characteristics.",
        "qa": [
            ("Why is this useful?", "One table shows everything - don't need to check each column individually."),
            ("What should I look for?", "High missing percentages, unexpected data types, unusual patterns.")
        ]
    },
    19: {  # Load data dictionary
        "what": "Attempts to load an external data dictionary file (if available).",
        "why": "Official documentation helps understand what each feature means.",
        "qa": [
            ("What if file doesn't exist?", "We handle it gracefully and document features ourselves (Cell 20)."),
            ("Is data dictionary required?", "No, but helpful for understanding feature definitions.")
        ]
    },
    24: {  # Summary statistics
        "what": "Calculates comprehensive summary statistics for all numerical features.",
        "why": "Get quantitative overview of data distribution before detailed analysis.",
        "code_breakdown": [
            ("df.describe()", "Generates mean, std, min, max, quartiles for all numeric columns"),
            ("df['SalePrice'].describe()", "Detailed statistics for target variable"),
            ("Price Range calculation", "Shows min to max house prices"),
            ("IQR calculation", "Interquartile range (middle 50% spread)"),
            ("Coefficient of Variation", "Relative variability measure")
        ],
        "statistics_explained": {
            "count": "Number of non-missing values",
            "mean": "Average value (sum ÷ count)",
            "std": "Standard deviation (measure of spread)",
            "min": "Smallest value",
            "25%": "First quartile (25% of data below this)",
            "50%": "Median (middle value, 50% below)",
            "75%": "Third quartile (75% of data below this)",
            "max": "Largest value"
        },
        "output_meaning": {
            "Mean price $180,796": "Average house price",
            "Median $160,000": "Middle house price (50th percentile)",
            "Std $79,887": "High variability in prices",
            "Range $12,789-$755,000": "Full price spectrum from low to luxury"
        },
        "qa": [
            ("Why is mean > median?", "Distribution is right-skewed (few very expensive houses pull up the average)."),
            ("What's a good standard deviation?", "Depends on context - here it shows significant price variation."),
            ("Why calculate all this?", "Establishes quantitative baseline for all further analysis.")
        ]
    },
    28: {  # Calculate missing values
        "what": "Systematically calculates missing value counts and percentages for all features.",
        "why": "Quantify the missing data problem before deciding how to handle it.",
        "code_breakdown": [
            ("df.isnull().sum()", "Counts missing values per column"),
            ("(missing_counts / len(df)) * 100", "Converts counts to percentages"),
            ("Create DataFrame with results", "Organizes results in table format"),
            (".sort_values(ascending=False)", "Orders by most missing to least")
        ],
        "output_meaning": {
            "Pool QC: 99.66%": "Almost all houses don't have pools (not missing, just absent)",
            "Lot Frontage: 16.65%": "Moderate missingness - need to handle",
            "0.00%": "Features with no missing data - ready to use"
        },
        "qa": [
            ("What percentage is too much?", "Generally >50% consider dropping, <5% easy to handle, 5-50% analyze carefully."),
            ("Why does Pool QC have 99% missing?", "Most houses don't have pools - 'missing' actually means 'no pool'."),
            ("What do we do next?", "Cells 32-38 implement our missing value treatment strategy.")
        ]
    }
}

# Educational cell explanations
EDUCATIONAL_EXPLANATIONS = {
    25: {  # Summary Statistics educational
        "formulas": [
            {
                "name": "Mean (Average)",
                "latex": r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i",
                "symbols": {
                    "x̄": "Mean (average)",
                    "n": "Total number of values",
                    "xᵢ": "Each individual value",
                    "Σ": "Sum (add all values)"
                },
                "example": {
                    "data": "House prices: $150K, $160K, $170K, $180K, $190K",
                    "step1": "Add all values: 150 + 160 + 170 + 180 + 190 = 850",
                    "step2": "Divide by count (n=5): 850 ÷ 5 = 170",
                    "result": "Mean = $170K"
                },
                "plain_english": "The mean is the average. Add up all values and divide by how many values you have.",
                "analogy": "Like calculating your average test score - add all scores, divide by number of tests."
            },
            {
                "name": "Standard Deviation",
                "latex": r"\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}",
                "symbols": {
                    "σ": "Standard deviation",
                    "n": "Number of values",
                    "xᵢ": "Each individual value",
                    "x̄": "Mean",
                    "√": "Square root"
                },
                "example": {
                    "data": "Same prices as above, mean = $170K",
                    "step1": "Calculate differences from mean: -20, -10, 0, +10, +20",
                    "step2": "Square each: 400, 100, 0, 100, 400",
                    "step3": "Average the squares: 1000 ÷ 5 = 200",
                    "step4": "Take square root: √200 ≈ $14.1K",
                    "result": "Std Dev = $14.1K"
                },
                "plain_english": "Standard deviation measures how spread out values are from the average. Higher = more spread.",
                "analogy": "Like measuring how consistent your test scores are - low std dev = consistent, high = all over the place."
            }
        ]
    },
    27: {  # Missing Values educational
        "types": [
            {
                "name": "MCAR - Missing Completely At Random",
                "definition": "Missingness has NO relationship to any data, observed or unobserved.",
                "example": "Sensor randomly fails 5% of the time - doesn't depend on what it's measuring",
                "handling": "Safest to handle - can safely delete or impute",
                "in_our_data": "Very rare in practice"
            },
            {
                "name": "MAR - Missing At Random",
                "definition": "Missingness related to OTHER observed variables, not the missing value itself.",
                "example": "Older homes more likely to have missing garage data (age observed, garage data missing)",
                "handling": "Can handle with careful imputation using related variables",
                "in_our_data": "Lot Frontage missing related to neighborhood - we use neighborhood median"
            },
            {
                "name": "MNAR - Missing Not At Random",
                "definition": "Missingness related to the MISSING value itself.",
                "example": "People with very high/low incomes don't report income",
                "handling": "Most problematic - hard to handle without introducing bias",
                "in_our_data": "Hopefully none, but hard to detect"
            }
        ],
        "decision_rules": {
            "> 50% missing": "Consider dropping column (insufficient information)",
            "< 5% missing": "Safe to impute or drop rows (minimal impact)",
            "5-50% missing": "Analyze pattern, then decide strategy carefully"
        }
    }
}

print("✅ Loaded explanations database")
print(f"   - Code cell explanations: {len(CELL_EXPLANATIONS)}")
print(f"   - Educational cell explanations: {len(EDUCATIONAL_EXPLANATIONS)}")
print()
print("Phase 1 PDF content preparation complete!")
print()
print("Next: Generate HTML and convert to PDF...")

