# 🏦 Bank Customer Retention Analytics Dashboard

> **Customer Engagement & Product Utilization Analytics for Retention Strategy**  
> Real European Bank Data | 10,000 Customers | Finance Analytics | Unified Mentor Internship

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.58-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-3.0.3-green?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-6.8-purple?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

---

## 🚀 Live Dashboard

🔗 **[View Live Dashboard →](https://retainiq-bank-analytics.streamlit.app)**

---

## 📌 Project Overview

This project analyzes **10,000 real European Bank customers** to uncover behavioral drivers of churn — going beyond demographics to focus on **engagement patterns** and **product utilization depth**.

Banks often rely on demographic data (age, salary, geography) to predict churn. This project proves that **behavioral engagement is the real driver** — active members retain at **85.73%** vs inactive members at **73.15%**.

---

## 🎯 Problem Statement

Despite having customer engagement and product data, banks often lack:
- Quantitative insight into **which behaviors drive retention**
- Clarity on whether **product depth reduces churn**
- Evidence on whether **high balances alone ensure loyalty**

This project solves all three — with real data and actionable strategy.

---

## 📊 Key Findings (Real Data)

| KPI | Value | Insight |
|-----|-------|---------|
| **Overall Churn Rate** | 20.37% | 2,037 customers lost |
| **Engagement Retention Ratio** | 1.17x | Active 85.73% vs Inactive 73.15% |
| **Product Depth Index** | 1.21x | Multi-product 87.23% vs Single 72.29% |
| **At-Risk Premium Customers** | 1,247 | $185.6M AUM at risk |
| **High-Balance Churn Rate** | 30.47% | 1.50x higher than average |
| **RSI Gap** | 4.92 points | Retained 49.61 vs Churned 44.69 |

---

## 🔍 Customer Segments Identified

| Segment | Customers | Churn Rate | Avg Balance |
|---------|-----------|------------|-------------|
| **Sticky Elite** | 1,565 | 11.82% | $65,295 |
| **Sticky Multi-Product** | 1,023 | 6.35% | $34,372 |
| **Sticky Active** | 2,012 | 17.59% | $102,316 |
| **At-Risk Premium** | 1,247 | 30.47% | $148,858 |
| **High Churn Risk** | 4,153 | 25.36% | $56,832 |

---

## 📦 Dashboard Features (6 Pages)

### 🎯 Page 1: Executive Dashboard
- Real-time KPI metrics
- Churn rate by engagement status
- Product impact on retention
- Geographic distribution

### 👥 Page 2: Engagement Analysis
- 4 behavioral customer profiles
- Age vs Tenure heatmap
- Engagement classification
- Profile comparison

### 📦 Page 3: Product Utilization
- Product count distribution
- Retention improvement curve
- Cross-sell opportunity matrix
- Product mix analysis

### ⚠️ Page 4: At-Risk Customers
- 1,247 premium inactive customers detected
- $185.6M AUM at risk
- Risk scoring and prioritization
- Intervention strategies

### 📈 Page 5: Retention Insights
- Relationship Strength Index (RSI)
- Retention driver analysis
- Sticky profile identification
- Strategic recommendations

### 🔍 Page 6: Customer Deep Dive
- Individual customer search
- Complete risk assessment
- Personal profile analysis
- Targeted recommendations

### 🎛️ Interactive Filters (Sidebar)
- Geography filter (France, Spain, Germany)
- Age range slider
- Balance range slider
- Real-time chart updates

---

## 🧠 Analytical Methodology

```
1. Data Ingestion & Validation
   └─ 10,000 records | 14 columns | 0 missing values

2. Engagement Classification
   └─ 4 behavioral profiles created

3. Product Utilization Analysis
   └─ Single vs multi-product retention comparison

4. Financial Commitment vs Engagement
   └─ Balance group analysis | Salary-balance mismatch

5. At-Risk Customer Detection
   └─ High-balance + inactive = critical segment

6. KPI Calculation (5 core metrics)
   └─ Engagement Ratio | Product Depth | RSI | CC Stickiness | Disengagement Rate
```

---

## 📂 Project Structure

```
bank-customer-retention/
├── dashboard.py              # 6-page Streamlit dashboard (911 lines)
├── eda_analysis.py           # EDA & KPI calculation
├── research_paper.py         # Research paper generation
├── bank_customer_data.csv    # Real European Bank data (10,000 records)
├── kpi_summary.json          # Pre-calculated KPI metrics
├── requirements.txt          # Python dependencies
└── .gitignore                # Git configuration
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.14** | Core language |
| **Pandas 3.0.3** | Data manipulation |
| **NumPy 2.4.6** | Numerical computing |
| **Plotly 6.8** | Interactive visualizations |
| **Streamlit 1.58** | Web dashboard |
| **SciPy 1.17** | Statistical analysis |
| **Matplotlib 3.10** | Static plots |
| **Seaborn 0.13** | Statistical visualization |

---

## ⚙️ Run Locally

```bash
# 1. Clone repository
git clone https://github.com/ashanthan03/bank-customer-retention.git
cd bank-customer-retention

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run EDA analysis
python eda_analysis.py

# 4. Launch dashboard
streamlit run dashboard.py

# 5. Open browser
# http://localhost:8501
```

---

## 📊 Dataset Description

| Column | Type | Description |
|--------|------|-------------|
| CustomerId | Integer | Unique customer identifier |
| CreditScore | Integer | Credit worthiness (350-850) |
| Geography | String | France / Spain / Germany |
| Gender | String | Male / Female |
| Age | Integer | Customer age (18-92) |
| Tenure | Integer | Years with bank (0-10) |
| Balance | Float | Account balance (€0-€250,898) |
| NumOfProducts | Integer | Products held (1-4) |
| HasCrCard | Binary | Credit card ownership (0/1) |
| IsActiveMember | Binary | Activity status (0/1) |
| EstimatedSalary | Float | Annual salary estimate |
| Exited | Binary | **Churn target** (0=Retained, 1=Churned) |

**Source:** European Central Bank Customer Database  
**Records:** 10,000 customers | **Churn Rate:** 20.37%

---

## 💡 Key Insights

**1. Engagement is the #1 Retention Driver**
> Active members retain at 85.73% vs inactive at 73.15% — a 1.17x difference

**2. Product 3 & 4 Show Anomalous Churn**
> 3-product customers churn at 82.71% and 4-product at 100% — indicating over-selling risk

**3. Zero-Balance Customers Are a Hidden Segment**
> 3,617 customers (36%) have zero balance — yet 13.82% churn rate suggests engagement matters more than balance

**4. At-Risk Premium Segment is Critical**
> 1,247 high-balance inactive customers face 30.47% churn — $185.6M AUM at risk

**5. RSI Predicts Churn**
> Retained customers average RSI 49.61 vs churned 44.69 — a reliable early warning indicator

---

## 🏆 Strategic Recommendations

| Priority | Action | Target Segment | Expected Impact |
|----------|--------|----------------|-----------------|
| 🔴 **Critical** | Activate inactive premium customers | 1,247 at-risk | Reduce $185.6M AUM loss |
| 🟠 **High** | Stop over-selling beyond 2 products | 326 customers (3-4 products) | Fix 82-100% churn rate |
| 🟡 **Medium** | Cross-sell to single-product active | 2,563 customers | Improve 18.92% → 9.66% churn |
| 🟢 **Standard** | Engagement program for inactive | 4,849 customers | Lift 73.15% → 85%+ retention |

---

## 📄 Deliverables

- ✅ **EDA Analysis** — Complete exploratory data analysis with real data
- ✅ **Interactive Dashboard** — 6-page Streamlit application
- ✅ **Research Paper** — Academic-quality analysis (run `research_paper.py`)
- ✅ **KPI Metrics** — 5 core retention KPIs calculated
- ✅ **Strategic Recommendations** — 4 prioritized business actions

---

## 👨‍💻 Author

**Shanthan Kumar Akkinapalli**  
Final Year B.E. Computer Engineering (Data Science & ML)  
Matrusri Engineering College, Hyderabad  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/shanthan-kumar-akkinapalli-914a81341)
[![GitHub](https://img.shields.io/badge/GitHub-ashanthan03-black?logo=github)](https://github.com/ashanthan03)

---

## 📝 License

This project is licensed under the MIT License.

---

*Built with ❤️ for Unified Mentor Finance Analytics Internship*
