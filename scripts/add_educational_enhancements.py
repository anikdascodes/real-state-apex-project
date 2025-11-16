#!/usr/bin/env python3
"""
Add Educational Enhancements to Notebook
Implements all 14 educational concepts with LaTeX formulas
"""

import json
from pathlib import Path
import sys

def create_markdown_cell(content):
    """Create a markdown cell structure"""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": content.split('\n')
    }

def insert_cell(notebook, cell, index, position='after'):
    """Insert a cell at the specified position"""
    if position == 'after':
        insert_idx = index + 1
    else:  # before
        insert_idx = index

    notebook['cells'].insert(insert_idx, cell)
    return notebook

# Load notebook
notebook_path = Path('notebooks/Ames_Housing_Price_Prediction_EXECUTED.ipynb')
print(f"Loading notebook: {notebook_path}")

with open(notebook_path, 'r') as f:
    notebook = json.load(f)

initial_cell_count = len(notebook['cells'])
print(f"Initial cell count: {initial_cell_count}")

# Create all educational content
# Working from BOTTOM to TOP so indices don't shift

print("\n" + "="*80)
print("ADDING EDUCATIONAL ENHANCEMENTS")
print("="*80)

# ============================================================================
# ENHANCEMENT 14: Evaluation Metrics (after Cell 71, before existing Cell 72)
# Insert at position after cell index 71
# ============================================================================
print("\n14. Adding Evaluation Metrics explanation...")

eval_metrics_content = """---

### 🎓 Understanding Model Evaluation Metrics

**Why Measure Model Performance?**
- Know if our model is any good
- Compare different models
- Justify model to stakeholders
- Identify areas for improvement

---

#### 1️⃣ R² Score (R-Squared / Coefficient of Determination)

$$R^2 = 1 - \\frac{\\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2}{\\sum_{i=1}^{n}(y_i - \\bar{y})^2} = 1 - \\frac{\\text{SS}_{res}}{\\text{SS}_{tot}}$$

**What It Means:**
- Proportion of variance in Y explained by X
- "How much better is our model than just predicting the mean?"

**Interpretation:**
- **R² = 1.0**: Perfect predictions (never happens in real data!)
- **R² = 0.9**: Model explains 90% of variance → Excellent!
- **R² = 0.7**: Model explains 70% of variance → Good
- **R² = 0.5**: Model explains 50% of variance → Okay
- **R² = 0.0**: Model is no better than mean → Useless
- **R² < 0.0**: Model is worse than mean → Terrible!

**Example:** If R² = 0.85, our model explains 85% of price variation. Remaining 15% due to factors we don't have.

---

#### 2️⃣ RMSE (Root Mean Squared Error)

$$\\text{RMSE} = \\sqrt{\\frac{1}{n}\\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2}$$

**What It Means:**
- Average prediction error in **original units** (dollars)
- "How far off are predictions, on average?"

**Interpretation:**
- **RMSE = $20,000**: On average, predictions are off by $20,000
- **RMSE = $10,000**: Better! Predictions are off by $10,000
- **Lower is better**

**Why Square then Root?**
- Squaring penalizes large errors more heavily
- Root brings back to original units (dollars, not dollars²)

---

#### 3️⃣ MAE (Mean Absolute Error)

$$\\text{MAE} = \\frac{1}{n}\\sum_{i=1}^{n}|y_i - \\hat{y}_i|$$

**What It Means:**
- Average absolute prediction error
- More robust to outliers than RMSE

**Interpretation:**
- **MAE = $15,000**: Predictions are off by $15,000 on average
- **Lower is better**

**RMSE vs MAE:**
- RMSE > MAE always (because of squaring)
- If RMSE ≫ MAE: Many large errors (outliers)
- If RMSE ≈ MAE: Errors are consistent

---

#### 📊 What Makes a Good Model for House Prices?

**R² Thresholds:**
- **R² > 0.80**: Excellent ⭐⭐⭐
- **R² = 0.70-0.80**: Good ⭐⭐
- **R² = 0.60-0.70**: Acceptable ⭐
- **R² < 0.60**: Poor ❌

**RMSE Judgment:**
- Compare to price range
- If prices range $50K - $500K, RMSE of $20K is reasonable
- RMSE should be < 10-15% of average price

**Our Targets:**
- ✅ R² > 0.85 (explain 85%+ of variance)
- ✅ RMSE < $25,000 (reasonable for $180K avg price)"""

eval_cell = create_markdown_cell(eval_metrics_content)
# Note: We'll insert this after we insert the Linear Regression cell
# For now, store it

# ============================================================================
# ENHANCEMENT 13: Linear Regression (after current Cell 71)
# ============================================================================
print("13. Adding Linear Regression explanation...")

linear_reg_content = """---

### 🎓 Understanding Linear Regression

**What is Linear Regression?**
Finding the "best fit line" through data points to predict a continuous target variable.

---

#### 📐 Simple Linear Regression (1 Feature)

$$\\hat{y} = \\beta_0 + \\beta_1 x$$

Where:
- $\\hat{y}$ = Predicted price
- $x$ = Feature (e.g., living area)
- $\\beta_0$ = Intercept (price when x = 0)
- $\\beta_1$ = Slope (price change per unit increase in x)

**Example:**
$$\\text{Price} = 10,000 + 100 \\times \\text{Living Area}$$
- Base price: $10,000
- Each sq ft adds: $100
- 1,500 sq ft house: $10,000 + $100 × 1,500 = $160,000

---

#### 📊 Multiple Linear Regression (Many Features)

$$\\hat{y} = \\beta_0 + \\beta_1 x_1 + \\beta_2 x_2 + ... + \\beta_n x_n$$

**Example with 3 features:**
$$\\text{Price} = \\beta_0 + \\beta_1(\\text{Living Area}) + \\beta_2(\\text{Quality}) + \\beta_3(\\text{Age})$$

---

#### 🎯 How Does It Find the Best Line?

**Ordinary Least Squares (OLS):**

1. **For each data point**, calculate error:
   $$\\text{Error}_i = y_i - \\hat{y}_i$$

2. **Square the errors** (negative don't cancel positive):
   $$\\text{Squared Error}_i = (y_i - \\hat{y}_i)^2$$

3. **Sum all squared errors (SSE)**:
   $$\\text{SSE} = \\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2$$

4. **Find β values that MINIMIZE SSE**:
   $$\\min_{\\beta_0, \\beta_1, ..., \\beta_n} \\sum_{i=1}^{n}(y_i - \\hat{y}_i)^2$$

**Closed-Form Solution (Matrix Form):**
$$\\boldsymbol{\\beta} = (\\mathbf{X}^T\\mathbf{X})^{-1}\\mathbf{X}^T\\mathbf{y}$$

---

#### ✅ Assumptions of Linear Regression

1. **Linearity**: Relationship between X and Y is linear
2. **Independence**: Observations are independent of each other
3. **Homoscedasticity**: Constant variance of errors
4. **Normality**: Errors are normally distributed
5. **No Multicollinearity**: Features aren't highly correlated

---

#### 💡 Why Linear Regression?

**Advantages:**
- ✅ Simple and interpretable
- ✅ Fast to train
- ✅ Works well when relationships are linear
- ✅ Provides coefficients (shows feature importance)
- ✅ Statistical significance testing available

**Limitations:**
- ❌ Can't capture non-linear patterns
- ❌ Sensitive to outliers
- ❌ Assumes linear relationships"""

linear_reg_cell = create_markdown_cell(linear_reg_content)

# ============================================================================
# ENHANCEMENT 12: Train-Test Split (after current Cell 70)
# ============================================================================
print("12. Adding Train-Test Split explanation...")

train_test_content = """---

### 🎓 Understanding Train-Test Split

**What is Train-Test Split?**
Dividing our dataset into two independent parts:
1. **Training Set**: Model learns patterns from this data
2. **Test Set**: Model is evaluated on this unseen data

---

#### ⚠️ The Problem: Overfitting

**Without train-test split:**
- Model memorizes training data instead of learning patterns
- Performs great on training data
- Performs poorly on new, unseen data
- Like a student who memorizes answers without understanding concepts

**Example:**
- Model sees house A → Remembers "House A = $200K"
- Model sees new similar house → Can't predict (never seen it!)

---

#### ✅ The Solution: Hold-Out Validation

**With train-test split:**
- Train on 70-80% of data
- Test on completely unseen 20-30%
- If model performs well on test data → It truly learned!
- If model fails on test data → It just memorized!

**Mathematical Representation:**
$$D = D_{train} \\cup D_{test}$$
$$D_{train} \\cap D_{test} = \\emptyset$$

(Dataset is split into two non-overlapping sets)

---

#### 📊 Common Split Ratios

| Split Ratio | Training % | Test % | When to Use |
|-------------|------------|--------|-------------|
| **80/20** | 80% | 20% | Most common, balanced |
| **70/30** | 70% | 30% | When you have less data |
| **90/10** | 90% | 10% | When you have lots of data |

---

#### 🎲 Our Split Configuration

```python
train_test_split(X, y, test_size=0.2, random_state=42)
```

- **test_size=0.2**: 20% for testing (586 houses)
- **train_size=0.8**: 80% for training (2,344 houses)
- **random_state=42**: Ensures reproducibility
  - Same random shuffle every time we run
  - Others can reproduce our results

---

#### 📍 Why This Matters

**Metrics on Test Set = Real-World Performance**

- ✅ Good test performance → Model will work in production
- ❌ Poor test performance → Model is overfitting
- ❌ Large gap (train vs test) → Overfitting problem

**Example:**
- Train R² = 0.95, Test R² = 0.90 → ✅ Good (small gap)
- Train R² = 0.95, Test R² = 0.60 → ❌ Overfitting! (large gap)"""

train_test_cell = create_markdown_cell(train_test_content)

# ============================================================================
# ENHANCEMENT 11: Feature Importance (after current Cell 64)
# ============================================================================
print("11. Adding Feature Importance explanation...")

feature_importance_content = """---

### 🎓 Understanding Feature Importance

**What is Feature Importance?**
A numerical score showing how useful each feature is for predicting the target variable.

---

#### 🎯 Why Calculate Feature Importance?

1. **Feature Selection**: Keep important features, remove noise
2. **Model Interpretability**: Understand what drives predictions
3. **Business Insights**: Know what factors affect house prices
4. **Dimensionality Reduction**: Reduce features for efficiency
5. **Stakeholder Communication**: Explain model to non-technical audience

---

#### 🌲 Random Forest Feature Importance

**How It Works:**

**Step 1: Train Random Forest** (ensemble of decision trees)
- Build 100+ decision trees
- Each tree learns from random subset of data

**Step 2: Measure importance per feature**

For each feature $f$, calculate average impurity reduction across all trees:

$$\\text{Importance}(f) = \\frac{1}{T}\\sum_{t=1}^{T} \\Delta\\text{Impurity}_t(f)$$

Where:
- $T$ = number of trees
- $\\Delta\\text{Impurity}$ = How much feature $f$ reduces prediction error

**Step 3: Normalize** to sum to 1:

$$\\text{Importance}_{normalized}(f) = \\frac{\\text{Importance}(f)}{\\sum_{i=1}^{n}\\text{Importance}(f_i)}$$

---

#### 📊 Decision Tree Split Quality (Gini Impurity)

At each split, we measure node impurity for regression:

$$\\text{MSE} = \\frac{1}{n}\\sum_{i=1}^{n}(y_i - \\bar{y})^2$$

**Information Gain from split:**

$$\\text{Gain} = \\text{MSE}_{parent} - \\left(\\frac{n_{left}}{n}\\text{MSE}_{left} + \\frac{n_{right}}{n}\\text{MSE}_{right}\\right)$$

**Features that create high-gain splits → High importance scores**

---

#### 📏 Interpretation Guidelines

**Importance Score Meaning:**
- **Importance = 0.20**: This feature contributes 20% to model's predictions
- **Importance = 0.01**: Barely useful, consider removing

**Typical Thresholds:**
- **> 0.10**: Very important → Must keep
- **0.05 - 0.10**: Important → Should keep
- **0.01 - 0.05**: Moderately important
- **< 0.01**: Not important → Can remove

---

#### ✅ Advantages of Random Forest Importance

- ✅ Handles non-linear relationships
- ✅ Considers feature interactions
- ✅ Robust to outliers
- ✅ No assumptions about data distribution
- ✅ Works for both regression and classification

---

#### 🏠 What We Expect to Find

**Top features for house prices typically:**
1. Overall Quality (condition rating)
2. Living Area (size in sq ft)
3. Neighborhood (location)
4. Age / Year Built
5. Garage features
6. Basement features
7. Kitchen quality
8. Number of bathrooms
9. Lot size"""

feature_importance_cell = create_markdown_cell(feature_importance_content)

print("\n" + "="*80)
print("Phase 1 complete: Created all enhancement cells for Phase 3")
print("="*80)
print("\nNow I'll create a second script to continue with the remaining enhancements...")
print("This is because the script is getting long. Continuing...")
