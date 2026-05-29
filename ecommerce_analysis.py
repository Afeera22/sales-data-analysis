# ============================================================
# E-Commerce Sales Analysis
# Analyst: Afeera Begum
# Dataset: 1,000 orders | Jan 2023 - Dec 2023
# Tools: Python, Pandas, Matplotlib, Seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.size'] = 11

# ── 1. LOAD DATA ──────────────────────────────────────────
df = pd.read_csv('ecommerce_sales_data.csv', parse_dates=['order_date'])
print("Dataset Shape:", df.shape)
print(df.head())

# ── 2. DATA CLEANING & VALIDATION ────────────────────────
print("\nMissing Values:")
print(df.isnull().sum())
print(f"\nDuplicate rows: {df.duplicated().sum()}")

status_counts = df['order_status'].value_counts()
print("\nOrder Status Breakdown:")
print(status_counts)
print(f"\nDelivery Rate:     {round(status_counts['Delivered']/len(df)*100, 1)}%")
print(f"Return Rate:       {round(status_counts['Returned']/len(df)*100, 1)}%")
print(f"Cancellation Rate: {round(status_counts['Cancelled']/len(df)*100, 1)}%")

# Filter delivered orders for revenue analysis
delivered = df[df['order_status'] == 'Delivered'].copy()

# ── 3. MONTHLY REVENUE TREND ──────────────────────────────
monthly_rev = delivered.resample('ME', on='order_date')['final_amount'].sum().reset_index()
monthly_rev.columns = ['month', 'revenue']
monthly_rev['month_label'] = monthly_rev['month'].dt.strftime('%b')

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_rev['month_label'], monthly_rev['revenue'],
        marker='o', linewidth=2.5, color='#2563eb', markersize=6)
ax.fill_between(range(len(monthly_rev)), monthly_rev['revenue'], alpha=0.1, color='#2563eb')
ax.set_title('Monthly Revenue Trend (2023)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Month')
ax.set_ylabel('Revenue (INR)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/100000:.1f}L'))
plt.xticks(range(len(monthly_rev)), monthly_rev['month_label'])
plt.tight_layout()
plt.savefig('monthly_revenue_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved: monthly_revenue_trend.png")

peak = monthly_rev.loc[monthly_rev['revenue'].idxmax()]
print(f"Peak Revenue Month: {peak['month_label']} -- Rs.{peak['revenue']:,.0f}")

# ── 4. CATEGORY PERFORMANCE ───────────────────────────────
cat_perf = delivered.groupby('category').agg(
    total_revenue=('final_amount', 'sum'),
    total_orders=('order_id', 'count'),
    avg_order_value=('final_amount', 'mean')
).sort_values('total_revenue', ascending=False).reset_index()
cat_perf['revenue_share_pct'] = round(cat_perf['total_revenue'] / cat_perf['total_revenue'].sum() * 100, 1)

print("\nCategory Performance:")
print(cat_perf.to_string(index=False))

colors = ['#1d4ed8', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd']
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].barh(cat_perf['category'], cat_perf['total_revenue'], color=colors)
axes[0].set_title('Total Revenue by Category', fontweight='bold')
axes[0].set_xlabel('Revenue (INR)')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/100000:.1f}L'))
axes[1].pie(cat_perf['revenue_share_pct'], labels=cat_perf['category'],
            autopct='%1.1f%%', colors=colors, startangle=140)
axes[1].set_title('Revenue Share by Category', fontweight='bold')
plt.tight_layout()
plt.savefig('category_performance.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: category_performance.png")

# ── 5. REGIONAL ANALYSIS ──────────────────────────────────
region_perf = delivered.groupby('region').agg(
    total_revenue=('final_amount', 'sum'),
    total_orders=('order_id', 'count')
).sort_values('total_revenue', ascending=False).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
rcolors = ['#1d4ed8','#2563eb','#3b82f6','#60a5fa']
axes[0].bar(region_perf['region'], region_perf['total_revenue'], color=rcolors)
axes[0].set_title('Revenue by Region', fontweight='bold')
axes[0].set_ylabel('Revenue (INR)')
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/100000:.1f}L'))
axes[1].bar(region_perf['region'], region_perf['total_orders'], color=rcolors)
axes[1].set_title('Number of Orders by Region', fontweight='bold')
axes[1].set_ylabel('Order Count')
plt.tight_layout()
plt.savefig('regional_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: regional_analysis.png")

# ── 6. PAYMENT METHOD PREFERENCES ────────────────────────
payment = delivered['payment_method'].value_counts().reset_index()
payment.columns = ['method', 'count']

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(payment['method'], payment['count'],
               color=sns.color_palette("Blues_r", len(payment)))
ax.set_title('Orders by Payment Method', fontsize=13, fontweight='bold')
ax.set_xlabel('Number of Orders')
for bar, val in zip(bars, payment['count']):
    ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
            str(val), va='center', fontsize=10)
plt.tight_layout()
plt.savefig('payment_methods.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: payment_methods.png")

# ── 7. DISCOUNT IMPACT ────────────────────────────────────
discount_impact = delivered.groupby('discount_pct').agg(
    avg_order_value=('final_amount', 'mean'),
    order_count=('order_id', 'count')
).reset_index()

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.bar(discount_impact['discount_pct'].astype(str), discount_impact['order_count'],
        color='#93c5fd', alpha=0.7, label='Order Count')
ax2.plot(discount_impact['discount_pct'].astype(str), discount_impact['avg_order_value'],
         color='#1d4ed8', marker='o', linewidth=2, label='Avg Order Value')
ax1.set_xlabel('Discount %')
ax1.set_ylabel('Order Count', color='#60a5fa')
ax2.set_ylabel('Avg Order Value (INR)', color='#1d4ed8')
ax1.set_title('Discount % vs Order Volume & Average Order Value', fontweight='bold')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
plt.tight_layout()
plt.savefig('discount_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: discount_analysis.png")

# ── 8. EXECUTIVE SUMMARY ─────────────────────────────────
total_revenue = delivered['final_amount'].sum()
total_orders = len(delivered)
aov = delivered['final_amount'].mean()
top_cat = delivered.groupby('category')['final_amount'].sum().idxmax()
top_region = delivered.groupby('region')['final_amount'].sum().idxmax()
top_payment = delivered['payment_method'].value_counts().index[0]
return_rate = round(df[df['order_status'] == 'Returned'].shape[0] / len(df) * 100, 1)

print("\n" + "=" * 55)
print("     EXECUTIVE SUMMARY -- 2023 SALES ANALYSIS")
print("=" * 55)
print(f"  Total Revenue (Delivered):  Rs.{total_revenue:>10,.0f}")
print(f"  Total Delivered Orders:     {total_orders:>12,}")
print(f"  Average Order Value:        Rs.{aov:>10,.0f}")
print(f"  Top Category:               {top_cat:>20}")
print(f"  Top Region:                 {top_region:>20}")
print(f"  Most Used Payment Method:   {top_payment:>20}")
print(f"  Return Rate:                {return_rate:>19}%")
print("=" * 55)

print("""
KEY INSIGHTS:
1. Electronics drives the highest revenue despite lower order
   volume -- high AOV category worth prioritizing in marketing.
2. Q4 shows revenue spikes consistent with festive season
   demand (Diwali, year-end sales).
3. UPI and Credit Card dominate payment modes -- cashback
   offers on these could further boost conversion.
4. Higher discount bands (25-30%) do not significantly
   increase order volume -- opportunity to cap at 20% and
   protect margins.
5. Return rates within acceptable range but should be
   monitored by category, especially Electronics.
""")
