# Check whether P&L contains identity-related columns
import pandas as pc
analysis =pc.read_csv(r"XBRL-XBRL-PL-2025_part1.csv")
identity_cols = [
    col for col in analysis.columns
    if any(word in col.lower()
           for word in ["cin", "company", "address", "pin", "state", "uid"])
]

print("Possible identity columns in P&L:")
for col in identity_cols:
    print(col)
    
# print(analysis["company_uid"].head(20).to_list())
# print("\nUnique UIDs:", analysis["company_uid"].nunique())
# print("Total rows:", len(analysis))
print(analysis["company_uid"].head(30).tolist())
print(analysis["company_uid"].str.len().value_counts())