# E-Commerce Sales Analysis — Python & Pandas

## Project Overview
End-to-end exploratory data analysis (EDA) on a simulated e-commerce dataset of 1,000 orders across 2023. The goal is to uncover revenue trends, top-performing categories, regional patterns, and discount behavior to support business decision-making.

## Tools & Technologies
- **Python** (Pandas, NumPy)
- **Data Visualization** — Matplotlib, Seaborn
- **Skills demonstrated** — EDA, KPI analysis, business insight generation, data cleaning

## Dataset
- 1,000 orders | Jan 2023 – Dec 2023
- Features: order date, category, region, payment method, quantity, unit price, discount %, order status

## Analysis Performed

| # | Analysis | Key Finding |
|---|----------|-------------|
| 1 | Data Cleaning & Validation | Zero missing values, clean dataset |
| 2 | Monthly Revenue Trend | Peak revenue in May & Q4 (festive season) |
| 3 | Category Performance | Electronics = 79% of total revenue |
| 4 | Regional Analysis | North region leads in both revenue and orders |
| 5 | Payment Method Preferences | Cash on Delivery & UPI most used |
| 6 | Discount Impact on Revenue | 25-30% discounts do not increase order volume |

## Key Business Insights
1. **Electronics** drives 79% of revenue despite fewer orders — high AOV category worth prioritizing in marketing spend
2. **Q4 revenue spikes** align with festive season demand (Diwali, year-end sales)
3. **UPI & Credit Card** are growing payment modes — targeted cashback campaigns could boost conversion
4. **Discount optimization opportunity** — deep discounts (25-30%) don't drive more orders; capping at 20% could protect margins
5. **Return rate at 17.3%** — worth monitoring by category to reduce revenue leakage

## Charts Generated
- `monthly_revenue_trend.png` — Line chart of monthly revenue
- `category_performance.png` — Bar + pie chart of category breakdown
- `regional_analysis.png` — Revenue and orders by region
- `payment_methods.png` — Payment preference bar chart
- `discount_analysis.png` — Discount % vs order volume & AOV

## How to Run
```bash
pip install pandas numpy matplotlib seaborn
python ecommerce_analysis.py
```

## Project Structure
```
ecommerce-sales-analysis/
|-- ecommerce_sales_data.csv       # Dataset (1000 rows)
|-- ecommerce_analysis.py          # Full analysis script
|-- monthly_revenue_trend.png
|-- category_performance.png
|-- regional_analysis.png
|-- payment_methods.png
|-- discount_analysis.png
|-- README.md
```

---
*Project by Afeera Begum | Data Analyst | Bangalore, India*
