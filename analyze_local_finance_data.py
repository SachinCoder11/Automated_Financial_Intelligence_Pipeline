"""Evidence-based profile of the local finance datasets used by the notebooks."""
from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "XBRL-XBRL-PL-2025_part1.csv"
DERIVED = ROOT / "MCA_PL_FY2024_25_Clean_Analysis.csv"
OUT = ROOT / "output" / "analysis"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(SOURCE, low_memory=False)
raw_rows, raw_cols = df.shape
empty_cols = [c for c in df.columns if df[c].isna().all()]
clean = df.drop(columns=empty_cols)
duplicates = int(clean.duplicated().sum())
period = clean[
    (clean["current_previous"].astype(str).str.strip().eq("current"))
    & clean["DateStartReportingPeriod"].eq("2024-04-01")
    & clean["DateEndReportingPeriod"].eq("2025-03-31")
].copy()

financial_cols = [
    "Revenue", "Expenses", "ProfitBeforeTax", "TaxExpense", "ProfitLossForPeriod",
    "FinanceCosts", "EmployeeBenefitExpense", "DepreciationExpense", "OtherExpenses",
    "ResearchDevelopmentExpenditure", "CSRExpenditure"
]
for col in financial_cols:
    if col in period:
        period[col] = pd.to_numeric(period[col], errors="coerce")

analysis = period[period["Revenue"] > 0].copy()
analysis["Profit_Margin"] = analysis["ProfitLossForPeriod"] / analysis["Revenue"] * 100
analysis["Expense_Ratio"] = analysis["Expenses"] / analysis["Revenue"] * 100
analysis["Finance_Cost_Ratio"] = analysis["FinanceCosts"] / analysis["Revenue"] * 100
analysis["Employee_Cost_Ratio"] = analysis["EmployeeBenefitExpense"] / analysis["Revenue"] * 100
analysis["R&D_Intensity"] = analysis["ResearchDevelopmentExpenditure"] / analysis["Revenue"] * 100

margin = analysis["Profit_Margin"].replace([np.inf, -np.inf], np.nan).dropna()
q1, q3 = margin.quantile([0.25, 0.75])
iqr = q3 - q1
outlier_count = int(((margin < q1 - 1.5 * iqr) | (margin > q3 + 1.5 * iqr)).sum())
finance = analysis["Finance_Cost_Ratio"].replace([np.inf, -np.inf], np.nan).dropna()
finance_frame = analysis.loc[finance.index, ["Finance_Cost_Ratio", "Profit_Margin"]].copy()
if len(finance_frame) >= 4:
    finance_frame["burden"] = pd.qcut(finance_frame["Finance_Cost_Ratio"].rank(method="first"), 4, labels=["Q1 Low", "Q2", "Q3", "Q4 High"])
    burden_medians = finance_frame.groupby("burden", observed=False)["Profit_Margin"].median()
else:
    burden_medians = pd.Series(dtype=float)

features = [c for c in ["Revenue", "Expenses", "ProfitBeforeTax", "FinanceCosts", "EmployeeBenefitExpense", "DepreciationExpense", "OtherExpenses", "ProfitLossForPeriod", "Profit_Margin", "Expense_Ratio", "Finance_Cost_Ratio", "Employee_Cost_Ratio", "R&D_Intensity"] if c in analysis]
corr = analysis[features].corr(numeric_only=True)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(8.4, 4.7))
plot_margin = margin.clip(margin.quantile(.01), margin.quantile(.99))
sns.histplot(plot_margin, bins=50, color="#1F6E8C")
plt.axvline(margin.median(), color="#E76F51", linewidth=2, label=f"Median = {margin.median():.2f}%")
plt.title("Profit Margin Distribution - FY 2024-25")
plt.xlabel("Profit Margin (%) - clipped only for display")
plt.ylabel("Companies")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "profit_margin_distribution.png", dpi=180)
plt.close()

plt.figure(figsize=(8.4, 4.7))
if not burden_medians.empty:
    plt.bar(burden_medians.index.astype(str), burden_medians.values, color="#2A9D8F")
    plt.axhline(0, color="#263238", linewidth=1)
plt.title("Median Profit Margin by Finance-Cost Burden")
plt.xlabel("Finance Costs / Revenue Quartile")
plt.ylabel("Median Profit Margin (%)")
plt.tight_layout()
plt.savefig(OUT / "finance_cost_burden.png", dpi=180)
plt.close()

plt.figure(figsize=(9, 7))
sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1, square=True, cbar_kws={"shrink": .7})
plt.title("Financial Variable Correlation Matrix - FY 2024-25")
plt.tight_layout()
plt.savefig(OUT / "financial_correlation_matrix.png", dpi=180)
plt.close()

profile = {
    "source_file": SOURCE.name,
    "source_origin_status": "The workspace does not contain provenance metadata establishing the original external publisher or download URL.",
    "raw_rows": raw_rows,
    "raw_columns": raw_cols,
    "fully_empty_columns_removed": len(empty_cols),
    "columns_after_empty_removal": clean.shape[1],
    "duplicate_rows_after_empty_removal": duplicates,
    "total_missing_cells_raw": int(df.isna().sum().sum()),
    "filtered_current_fy_2024_25_rows": len(period),
    "revenue_positive_analysis_rows": len(analysis),
    "revenue_nonpositive_or_missing_excluded_from_ratio_analysis": len(period) - len(analysis),
    "unique_company_uids_in_analysis": int(analysis["company_uid"].nunique()),
    "profit_margin_median_percent": float(margin.median()),
    "profit_margin_iqr_outlier_count": outlier_count,
    "profitability_counts": {
        "profitable": int((period["ProfitLossForPeriod"] > 0).sum()),
        "loss_making": int((period["ProfitLossForPeriod"] < 0).sum()),
        "zero_profit": int((period["ProfitLossForPeriod"] == 0).sum()),
        "missing_profit": int(period["ProfitLossForPeriod"].isna().sum()),
    },
    "selected_linear_correlations": {
        "revenue_expenses": float(corr.loc["Revenue", "Expenses"]),
        "revenue_profit_after_tax": float(corr.loc["Revenue", "ProfitLossForPeriod"]),
        "expenses_profit_after_tax": float(corr.loc["Expenses", "ProfitLossForPeriod"]),
        "finance_cost_ratio_profit_margin": float(corr.loc["Finance_Cost_Ratio", "Profit_Margin"]),
    },
    "finance_cost_burden_median_profit_margin_percent": {str(k): float(v) for k, v in burden_medians.items()},
    "derived_file": DERIVED.name,
    "derived_file_rows": int(pd.read_csv(DERIVED, usecols=["company_uid"]).shape[0]),
    "derived_file_columns": len(pd.read_csv(DERIVED, nrows=1).columns),
    "graphs": ["profit_margin_distribution.png", "finance_cost_burden.png", "financial_correlation_matrix.png"],
}
(OUT / "local_data_profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")
print(json.dumps(profile, indent=2))
