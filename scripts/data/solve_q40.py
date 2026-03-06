import pandas as pd

# Load data
try:
    opp_df = pd.read_csv('test_data/fact_opportunity_202602111036.csv')
    con_df = pd.read_csv('test_data/fact_contract_202602101728.csv')
except Exception as e:
    print(f"Error loading files: {e}")
    exit(1)

# Ensure numeric types
numeric_cols_opp = ['opp_amount', 'win_rate', 'est_gross_profit']
for col in numeric_cols_opp:
    if col in opp_df.columns:
        opp_df[col] = pd.to_numeric(opp_df[col], errors='coerce')

numeric_cols_con = ['sales_amount_total', 'gross_margin_rate', 'net_profit']
for col in numeric_cols_con:
    if col in con_df.columns:
        con_df[col] = pd.to_numeric(con_df[col], errors='coerce')

# Ensure date types
if 'est_deal_date' in opp_df.columns:
    opp_df['est_deal_date'] = pd.to_datetime(opp_df['est_deal_date'], errors='coerce')
if 'archive_time' in con_df.columns:
    con_df['archive_time'] = pd.to_datetime(con_df['archive_time'], errors='coerce')

def get_val(df, filter_col, filter_val, target_col):
    try:
        res = df[df[filter_col] == filter_val][target_col]
        return res.iloc[0] if not res.empty else "Not Found"
    except: return "Error"

# 40: Find contract with max amount where sales_amount_total > opp_amount
opp_key = 'opp_id'
con_key = 'opp_code'
if opp_key in opp_df.columns and con_key in con_df.columns:
    merged = pd.merge(con_df, opp_df, left_on=con_key, right_on=opp_key, how='inner')
    filtered = merged[merged['sales_amount_total'] > merged['opp_amount']]
    if not filtered.empty:
        max_contract = filtered.nlargest(1, 'sales_amount_total')[['contract_name', 'sales_amount_total']]
        ans40 = f"{max_contract.iloc[0,0]} ({max_contract.iloc[0,1]})"
    else:
        ans40 = "None"
else:
    ans40 = "Join keys not found"

print(f"Q40: 查找合同金额大于商机金额的所有合同中，金额最高的那一个合同名称是什么？")
print(f"答案: {ans40}")
