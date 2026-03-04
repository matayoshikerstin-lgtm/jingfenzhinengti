import pandas as pd
import sys

# Force output encoding
sys.stdout.reconfigure(encoding='utf-8')

# 数据源：test_data/测试数据.xlsx（商机表 + 合同表）
DATA_PATH = 'test_data/测试数据.xlsx'
try:
    df = pd.read_excel(DATA_PATH, sheet_name='商机')
    con_df = pd.read_excel(DATA_PATH, sheet_name='合同')
except Exception as e:
    print(f"Error loading {DATA_PATH}: {e}")
    exit()

# Column Mapping (Based on verified Chinese names)
COL_EXCLUDE = '不纳入原因'  # Previously: exclude_reason
COL_STAGE = '销售流程'      # Previously: stage/sales_process
COL_OWNER = '负责人'        # Previously: owner_id
COL_CUST = '客户名称'       # Previously: customer_name
COL_LINE = '军团产品线'     # Previously: legion_product_line
COL_AMT = '商机金额'        # Previously: opp_amount
COL_WIN = '赢单率'          # Previously: win_rate
COL_DATE = '预计成交日期'   # Previously: est_deal_date
COL_STATUS = '生命状态'     # Previously: life_status
COL_BU = '所属业务单元'     # Previously: business_unit_name

# Preprocessing
num_cols = [COL_AMT, COL_WIN]
for c in num_cols:
    if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')

if COL_DATE in df.columns:
    df[COL_DATE] = pd.to_datetime(df[COL_DATE], errors='coerce')

# --- Helper Functions ---

def get_dist(col, top_n=3):
    if col not in df.columns: return "Column not found"
    return df[col].value_counts().head(top_n).to_dict()

def get_filtered_dist(filter_col, filter_val, target_col, top_n=3):
    filtered = df[df[filter_col] == filter_val]
    if filtered.empty: return "No data"
    return filtered[target_col].value_counts().head(top_n).to_dict()

# --- Q41-Q55 Answers ---

answers = {}

# Q41: Why high loss rate? (Exclude reason dist)
answers["Q41"] = f"主要原因: {get_dist(COL_EXCLUDE)}"

# Q42: '合同风险过高' concentrated where?
answers["Q42"] = f"集中客户: {get_filtered_dist(COL_EXCLUDE, '合同风险过高', COL_CUST)}"

# Q43: Wang Fang issues
wf_df = df[df[COL_OWNER] == 'U003-王芳']
if not wf_df.empty:
    top_stage = wf_df[COL_STAGE].value_counts().idxmax()
    top_reason = wf_df[COL_EXCLUDE].value_counts().head(1).to_dict()
    answers["Q43"] = f"主要滞留: {top_stage}; 主要阻碍: {top_reason}"
else: answers["Q43"] = "无数据"

# Q44: Shuzhi Ops Line low win rate?
sz_df = df[df[COL_LINE] == '数智运营产品线']
if not sz_df.empty:
    avg_win = sz_df[COL_WIN].mean()
    top_r = sz_df[COL_EXCLUDE].value_counts().head(1).to_dict()
    answers["Q44"] = f"平均赢单率: {avg_win:.2f}; 主要阻碍: {top_r}"
else: answers["Q44"] = "无数据"

# Q45: CMCC loss reasons
answers["Q45"] = f"流失原因: {get_filtered_dist(COL_CUST, '中国移动通信集团公司', COL_EXCLUDE)}"

# Q46: 2025 H1 Outlook
start, end = pd.Timestamp('2025-01-01'), pd.Timestamp('2025-06-30')
h1_df = df[(df[COL_DATE] >= start) & (df[COL_DATE] <= end)]
h1_total = h1_df[COL_AMT].sum()
# Risks: Amt > 3000 & Win < 0.3
risks = h1_df[(h1_df[COL_AMT] > 3000) & (h1_df[COL_WIN] < 0.3)]['商机名称'].head(2).tolist()
answers["Q46"] = f"H1预计总额: {h1_total:.2f}; 风险项目: {risks}"

# Q47: Future 3 months star sales
# 假设起点为 2025-02-12 (或根据实际数据分布调整，这里按之前逻辑保持 2025-02-12)
start_f = pd.Timestamp('2025-02-12')
end_f = start_f + pd.DateOffset(months=3)
fut_df = df[(df[COL_DATE] >= start_f) & (df[COL_DATE] <= end_f)]
if not fut_df.empty:
    top_s = fut_df.groupby(COL_OWNER)[COL_AMT].sum().nlargest(1)
    answers["Q47"] = f"{top_s.index[0]} (预计: {top_s.values[0]:.2f}，统计区间: {start_f.strftime('%Y-%m-%d')} 至 {end_f.strftime('%Y-%m-%d')})"
else: answers["Q47"] = "无预测数据"

# Q48: Potential Product Line
line_stats = df.groupby(COL_LINE).agg({COL_AMT: 'sum', COL_WIN: 'mean'})
line_stats['score'] = line_stats[COL_AMT] * line_stats[COL_WIN]
top_line_amt = line_stats.nlargest(1, COL_AMT)
answers["Q48"] = f"储备最高: {top_line_amt.index[0]} (金额: {top_line_amt[COL_AMT].values[0]:.0f}, 平均赢单率: {top_line_amt[COL_WIN].values[0]:.4f})"

# Q49: Bottleneck Stage
active_df = df[df[COL_STATUS] == '活跃']
if not active_df.empty:
    bottleneck = active_df[COL_STAGE].value_counts().head(1)
    answers["Q49"] = f"滞留最多: {bottleneck.index[0]} ({bottleneck.values[0]}个)"
else: answers["Q49"] = "无活跃商机"

# Q50: High Prob Return (赢单率>50% 的商机主要集中在哪些客户)
high_prob = df[df[COL_WIN] > 0.5]
if not high_prob.empty:
    top_high_prob_cust = high_prob[COL_CUST].value_counts().head(5).to_dict()
    answers["Q50"] = f"高赢单率集中客户: {top_high_prob_cust}"
else:
    answers["Q50"] = "无赢单率>50%的数据"

# Q51: Top 10 Risk
top10 = df.nlargest(10, COL_AMT)
risky_top10 = top10[top10[COL_EXCLUDE].notnull()]['商机名称'].tolist()
answers["Q51"] = f"Top10风险项目: {risky_top10}"

# Q52: Low Margin（基于测试数据.xlsx 合同表）
# 合同表列：净利润、毛利率、销售额汇总等，按实际列名取数
con_amount_col = next((c for c in con_df.columns if '销售额' in str(c) or '销售' in str(c) and '额' in str(c)), None)
con_margin_col = next((c for c in con_df.columns if '毛利率' in str(c)), None)
if con_amount_col and con_margin_col:
    con_df[con_amount_col] = pd.to_numeric(con_df[con_amount_col], errors='coerce')
    con_df[con_margin_col] = pd.to_numeric(con_df[con_margin_col], errors='coerce')
    bad = con_df[(con_df[con_amount_col] > 1000) & (con_df[con_margin_col].notna()) & (con_df[con_margin_col] < 0.1)]
    answers["Q52"] = f"大额低毛利合同数: {len(bad)} (基于测试数据.xlsx 合同表)"
else:
    answers["Q52"] = "需合同表销售额/毛利率列 (测试数据.xlsx 合同表)"

# Q53: Huawei Dependency
hw_df = df[df[COL_CUST].str.contains('华为', na=False)]
if not hw_df.empty:
    dep = hw_df[COL_LINE].value_counts(normalize=True).head(1)
    answers["Q53"] = f"集中于: {dep.index[0]} ({dep.values[0]:.0%})"
else: answers["Q53"] = "无华为数据"

# Q54: Stage advanced but low win rate
abnormal = df[(df[COL_STAGE].isin(['推进明确建设方案', '进入项目审批流程'])) & (df[COL_WIN] < 0.2)]
answers["Q54"] = f"异常数量: {len(abnormal)}"

# Q55: Sales Load
load = active_df[COL_OWNER].value_counts().head(1)
answers["Q55"] = f"负荷最重: {load.index[0]} ({load.values[0]}个)"

# Q56: 推进明确建设方案阶段分析
stage_df = df[df[COL_STAGE] == '推进明确建设方案']
active_stage_count = len(stage_df[stage_df[COL_STATUS] == '活跃'])
excluded_stage_df = stage_df[stage_df[COL_EXCLUDE].notna()]
if not excluded_stage_df.empty:
    top_reasons = excluded_stage_df[COL_EXCLUDE].value_counts().head(3).to_dict()
    answers["Q56"] = f"活跃商机数: {active_stage_count}个; 输单主要原因: {top_reasons}"
else:
    answers["Q56"] = f"活跃商机数: {active_stage_count}个; 无输单数据"

# Q57: 休眠商机分析
sleep_df = df[df[COL_STATUS] == '休眠']
sleep_count = len(sleep_df)
if not sleep_df.empty and sleep_df[COL_EXCLUDE].notna().any():
    top_reasons = sleep_df[COL_EXCLUDE].value_counts().head(3).to_dict()
    answers["Q57"] = f"休眠商机数: {sleep_count}个; 输单/排除主要原因: {top_reasons}"
else:
    # 如果休眠状态的商机没有填排除原因，则看整体的或者提示无数据
    answers["Q57"] = f"休眠商机数: {sleep_count}个; 无明确排除原因记录"

# Output formatted
print("--- 开放问题答案 (数据源: test_data/测试数据.xlsx 商机表+合同表) ---")
for q in sorted(answers.keys()):
    print(f"[{q}] {answers[q]}")
