"""
Bank Customer Retention Analytics - EDA & Analysis
Customer Engagement & Product Utilization Analysis
Dataset: REAL European Central Bank Customer Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# SECTION 1: DATA LOADING (Real European Bank dataset)
# ============================================================================

def load_real_dataset():
    """Load real European Bank customer dataset"""
    print("Loading real European Bank dataset...")
    df = pd.read_csv('bank_customer_data.csv')
    return df

# ============================================================================
# SECTION 2: DATA VALIDATION & QUALITY CHECKS
# ============================================================================

print("=" * 80)
print("BANK CUSTOMER RETENTION ANALYTICS - EDA")
print("=" * 80)
print("\n[1/7] Loading real European Bank dataset...")

df = load_real_dataset()

print("\n[2/7] Data Validation & Quality Checks")
print("-" * 80)

print(f"Dataset Shape: {df.shape}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nData Types:\n{df.dtypes}")

print("\n--- Binary Variables Consistency ---")
print(f"IsActiveMember unique values: {df['IsActiveMember'].unique()}")
print(f"HasCrCard unique values: {df['HasCrCard'].unique()}")
print(f"Exited (Churn) unique values: {df['Exited'].unique()}")

print("\n--- Geographic Distribution ---")
print(df['Geography'].value_counts())

print("\n--- Summary Statistics ---")
print(df.describe().round(2))

# ============================================================================
# SECTION 3: ENGAGEMENT CLASSIFICATION
# ============================================================================

print("\n[3/7] Engagement Classification & Customer Segmentation")
print("-" * 80)

def classify_engagement(row):
    """Classify customers into engagement profiles"""
    if row['IsActiveMember'] == 1 and row['NumOfProducts'] >= 2:
        return 'Active Engaged (Multi-Product)'
    elif row['IsActiveMember'] == 1 and row['NumOfProducts'] == 1:
        return 'Active Low-Product'
    elif row['IsActiveMember'] == 0 and row['Balance'] > df['Balance'].quantile(0.75):
        return 'Inactive Premium'
    else:
        return 'Inactive Disengaged'

df['EngagementProfile'] = df.apply(classify_engagement, axis=1)

print("\nEngagement Profile Distribution:")
print(df['EngagementProfile'].value_counts())
print("\nChurn Rate by Engagement Profile:")
engagement_churn = df.groupby('EngagementProfile')['Exited'].agg(['count', 'sum', 'mean'])
engagement_churn.columns = ['Total Customers', 'Churned', 'Churn Rate']
engagement_churn['Churn Rate'] = (engagement_churn['Churn Rate'] * 100).round(2)
print(engagement_churn)

# ============================================================================
# SECTION 4: PRODUCT UTILIZATION ANALYSIS
# ============================================================================

print("\n[4/7] Product Utilization & Retention Analysis")
print("-" * 80)

product_churn = df.groupby('NumOfProducts')['Exited'].agg(['count', 'sum', 'mean'])
product_churn.columns = ['Total Customers', 'Churned', 'Churn Rate']
product_churn['Churn Rate'] = (product_churn['Churn Rate'] * 100).round(2)
print("\nChurn Rate by Number of Products:")
print(product_churn)

single_vs_multi = df.copy()
single_vs_multi['ProductType'] = single_vs_multi['NumOfProducts'].apply(
    lambda x: 'Single Product' if x == 1 else 'Multi-Product'
)
product_type_churn = single_vs_multi.groupby('ProductType')['Exited'].agg(['count', 'sum', 'mean'])
product_type_churn.columns = ['Total Customers', 'Churned', 'Churn Rate']
product_type_churn['Churn Rate'] = (product_type_churn['Churn Rate'] * 100).round(2)
print("\nSingle vs Multi-Product Retention:")
print(product_type_churn)

print("\n--- Product Depth Effect on Churn ---")
product_depth_analysis = df.groupby('NumOfProducts').agg({
    'Exited': ['count', 'mean'],
    'Balance': 'mean',
    'Age': 'mean',
    'Tenure': 'mean',
    'EstimatedSalary': 'mean'
})
print(product_depth_analysis)

# ============================================================================
# SECTION 5: FINANCIAL COMMITMENT VS ENGAGEMENT
# ============================================================================

print("\n[5/7] Financial Commitment vs Engagement Analysis")
print("-" * 80)

# Fix for real data: many customers have Balance=0, causing duplicate bin edges
# Use custom bins instead of qcut for Balance
balance_bins = [df['Balance'].min() - 1, 0, 50000, 125000, df['Balance'].max() + 1]
balance_labels = ['Zero Balance', 'Low', 'High', 'Very High']
df['BalanceGroup'] = pd.cut(df['Balance'], bins=balance_bins, labels=balance_labels)
df['SalaryGroup'] = pd.qcut(df['EstimatedSalary'], q=4, labels=['Low', 'Medium', 'High', 'Very High'], duplicates='drop')

print("\nChurn Rate by Balance Group:")
balance_churn = df.groupby('BalanceGroup', observed=True)['Exited'].agg(['count', 'sum', 'mean'])
balance_churn.columns = ['Total', 'Churned', 'Churn Rate %']
balance_churn['Churn Rate %'] = (balance_churn['Churn Rate %'] * 100).round(2)
print(balance_churn)

print("\n--- Salary-Balance Mismatch Detection ---")
df['SalaryBalanceRatio'] = df['EstimatedSalary'] / (df['Balance'] + 1)
print(f"Customers with high salary but low balance (potential risk): {(df['SalaryBalanceRatio'] > 2).sum()}")

# ============================================================================
# SECTION 6: HIGH-VALUE DISENGAGED CUSTOMERS (AT-RISK SEGMENT)
# ============================================================================

print("\n[6/7] High-Value Disengaged Customer Detector")
print("-" * 80)

balance_75th = df['Balance'].quantile(0.75)
engagement_threshold = 0.5

at_risk_premium = df[
    (df['Balance'] > balance_75th) & 
    (df['IsActiveMember'] == 0)
]

print(f"\nAt-Risk Premium Customers (High Balance + Inactive):")
print(f"Total Count: {len(at_risk_premium)}")
print(f"Churn Rate: {(at_risk_premium['Exited'].mean() * 100):.2f}%")
print(f"Total Balance at Risk: ${at_risk_premium['Balance'].sum():,.0f}")
print(f"Avg Balance per Customer: ${at_risk_premium['Balance'].mean():,.0f}")

print("\nComparison:")
print(f"Overall Churn Rate: {(df['Exited'].mean() * 100):.2f}%")
print(f"At-Risk Premium Churn Rate: {(at_risk_premium['Exited'].mean() * 100):.2f}%")
print(f"Risk Multiplier: {(at_risk_premium['Exited'].mean() / df['Exited'].mean()):.2f}x higher")

# ============================================================================
# SECTION 7: KEY PERFORMANCE INDICATORS (KPIs)
# ============================================================================

print("\n[7/7] Key Performance Indicators (KPIs)")
print("-" * 80)

# 1. Engagement Retention Ratio
active_churn_rate = df[df['IsActiveMember'] == 1]['Exited'].mean()
inactive_churn_rate = df[df['IsActiveMember'] == 0]['Exited'].mean()
engagement_retention_ratio = (1 - active_churn_rate) / (1 - inactive_churn_rate)

print(f"\n1. ENGAGEMENT RETENTION RATIO")
print(f"   Active Member Retention: {((1 - active_churn_rate) * 100):.2f}%")
print(f"   Inactive Member Retention: {((1 - inactive_churn_rate) * 100):.2f}%")
print(f"   Ratio: {engagement_retention_ratio:.2f}x")

# 2. Product Depth Index
multi_product_churn = df[df['NumOfProducts'] >= 2]['Exited'].mean()
single_product_churn = df[df['NumOfProducts'] == 1]['Exited'].mean()
product_depth_index = (1 - multi_product_churn) / (1 - single_product_churn)

print(f"\n2. PRODUCT DEPTH INDEX")
print(f"   Multi-Product Retention: {((1 - multi_product_churn) * 100):.2f}%")
print(f"   Single-Product Retention: {((1 - single_product_churn) * 100):.2f}%")
print(f"   Depth Index: {product_depth_index:.2f}x")

# 3. High-Balance Disengagement Rate
high_balance_disengaged_rate = (
    df[(df['Balance'] > balance_75th) & (df['IsActiveMember'] == 0)]['Exited'].mean() * 100
)

print(f"\n3. HIGH-BALANCE DISENGAGEMENT RATE")
print(f"   Churn Rate (Premium Inactive): {high_balance_disengaged_rate:.2f}%")
print(f"   Risk Level: {'CRITICAL' if high_balance_disengaged_rate > 40 else 'HIGH' if high_balance_disengaged_rate > 30 else 'MODERATE'}")

# 4. Credit Card Stickiness Score
cc_churn = df[df['HasCrCard'] == 1]['Exited'].mean()
no_cc_churn = df[df['HasCrCard'] == 0]['Exited'].mean()
cc_stickiness = (1 - cc_churn) / (1 - no_cc_churn)

print(f"\n4. CREDIT CARD STICKINESS SCORE")
print(f"   With Credit Card Retention: {((1 - cc_churn) * 100):.2f}%")
print(f"   Without Credit Card Retention: {((1 - no_cc_churn) * 100):.2f}%")
print(f"   Stickiness Score: {cc_stickiness:.2f}x")

# 5. Relationship Strength Index (RSI)
def calculate_relationship_strength(row):
    """Calculate composite relationship strength (0-100)"""
    score = 0
    score += row['IsActiveMember'] * 25
    score += min(row['NumOfProducts'] / 4 * 25, 25)
    score += min(row['Tenure'] / 10 * 25, 25)
    score += (1 if row['HasCrCard'] == 1 else 0) * 15
    score += min(row['Balance'] / df['Balance'].max() * 10, 10)
    return score

df['RelationshipStrengthIndex'] = df.apply(calculate_relationship_strength, axis=1)

print(f"\n5. RELATIONSHIP STRENGTH INDEX (0-100 scale)")
rsi_stats = df.groupby('Exited')['RelationshipStrengthIndex'].agg(['mean', 'median', 'std'])
print(f"\n   Retained Customers - Mean RSI: {rsi_stats.loc[0, 'mean']:.2f}")
print(f"   Churned Customers - Mean RSI: {rsi_stats.loc[1, 'mean']:.2f}")
print(f"   RSI Difference: {(rsi_stats.loc[0, 'mean'] - rsi_stats.loc[1, 'mean']):.2f} points")

# ============================================================================
# SECTION 8: RETENTION STRENGTH ASSESSMENT
# ============================================================================

print("\n[BONUS] Retention Strength Assessment by Engagement Tier")
print("-" * 80)

def classify_sticky_profile(row):
    """Define sticky customer profile"""
    if row['IsActiveMember'] == 1 and row['NumOfProducts'] >= 2 and row['RelationshipStrengthIndex'] > 60:
        return 'Sticky Elite'
    elif row['IsActiveMember'] == 1 and row['NumOfProducts'] >= 2:
        return 'Sticky Multi-Product'
    elif row['IsActiveMember'] == 1 and row['RelationshipStrengthIndex'] > 50:
        return 'Sticky Active'
    elif row['IsActiveMember'] == 0 and row['Balance'] > balance_75th:
        return 'At-Risk Premium'
    else:
        return 'High Churn Risk'

df['StickyProfile'] = df.apply(classify_sticky_profile, axis=1)

retention_by_profile = df.groupby('StickyProfile').agg({
    'Exited': ['count', 'sum', 'mean'],
    'RelationshipStrengthIndex': 'mean',
    'Balance': 'mean'
})
retention_by_profile.columns = ['Total', 'Churned', 'Churn Rate', 'Avg RSI', 'Avg Balance']
retention_by_profile['Churn Rate'] = (retention_by_profile['Churn Rate'] * 100).round(2)
retention_by_profile['Avg Balance'] = retention_by_profile['Avg Balance'].apply(lambda x: f"${x:,.0f}")
retention_by_profile['Avg RSI'] = retention_by_profile['Avg RSI'].round(2)

print("\nCustomer Profile Analysis:")
print(retention_by_profile)

# ============================================================================
# SECTION 9: SAVE PROCESSED DATA
# ============================================================================

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - SAVING DATA FOR DASHBOARD")
print("=" * 80)

# Remove 'Year' column if it exists (not needed)
if 'Year' in df.columns:
    df = df.drop('Year', axis=1)

df.to_csv('bank_customer_data.csv', index=False)
print("\n✓ Processed dataset saved: bank_customer_data.csv")

# Save summary statistics
summary_stats = {
    'total_customers': len(df),
    'overall_churn_rate': df['Exited'].mean(),
    'engagement_retention_ratio': engagement_retention_ratio,
    'product_depth_index': product_depth_index,
    'cc_stickiness_score': cc_stickiness,
    'at_risk_premium_count': len(at_risk_premium),
    'at_risk_premium_churn_rate': at_risk_premium['Exited'].mean(),
    'avg_relationship_strength_retained': rsi_stats.loc[0, 'mean'],
    'avg_relationship_strength_churned': rsi_stats.loc[1, 'mean'],
}

import json
with open('kpi_summary.json', 'w') as f:
    json.dump(summary_stats, f, indent=2)

print("✓ KPI Summary saved: kpi_summary.json")

print("\n" + "=" * 80)
print("✓ EDA COMPLETE - Ready for Streamlit Dashboard Build")
print("=" * 80)
