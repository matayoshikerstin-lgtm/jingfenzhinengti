import pandas as pd

try:
    opp_df = pd.read_csv('test_data/fact_opportunity_202602111036.csv')
    con_df = pd.read_csv('test_data/fact_contract_202602101728.csv')
except Exception as e:
    print(f"Error loading: {e}")
    exit()

# Preprocessing
num_cols = ['opp_amount', 'win_rate', 'est_gross_profit']
for c in num_cols:
    if c in opp_df.columns: opp_df[c] = pd.to_numeric(opp_df[c], errors='coerce')

con_num_cols = ['sales_amount_total', 'gross_margin_rate', 'net_profit']
for c in con_num_cols:
    if c in con_df.columns: con_df[c] = pd.to_numeric(con_df[c], errors='coerce')

if 'est_deal_date' in opp_df.columns:
    opp_df['est_deal_date'] = pd.to_datetime(opp_df['est_deal_date'], errors='coerce')

# --- 开放问题 (Open-Ended) 数据支撑计算 ---

# Q41: 输单/排除原因分布
def get_exclude_reason_dist():
    if 'exclude_reason' not in opp_df.columns: return "No exclude_reason col"
    dist = opp_df['exclude_reason'].value_counts().head(3)
    return dist.to_dict()

# Q42: "合同风险过高" 集中在哪些客户
def get_risk_concentration():
    risk_df = opp_df[opp_df['exclude_reason'] == '合同风险过高']
    if risk_df.empty: return "No data"
    top_cust = risk_df['customer_name'].value_counts().head(3).to_dict()
    return top_cust

# Q43: U003-王芳 卡点 (Stage & Reason)
def get_wangfang_issues():
    wf_df = opp_df[opp_df['owner_id'] == 'U003-王芳']
    if wf_df.empty: return "No data"
    # Stage where count is high
    top_stage = wf_df['sales_process'].value_counts().head(1).index[0]
    # Top exclude reason
    top_reason = wf_df['exclude_reason'].value_counts().head(1)
    reason_str = f"{top_reason.index[0]}({top_reason.values[0]})" if not top_reason.empty else "无明显排除原因"
    return f"主要滞留在'{top_stage}'; 主要阻碍是: {reason_str}"

# Q44: 数智运营产品线 赢单率低原因
def get_shuzhi_low_win():
    sz_df = opp_df[opp_df['legion_product_line'] == '数智运营产品线']
    avg_win = sz_df['win_rate'].mean()
    top_reason = sz_df['exclude_reason'].value_counts().head(1)
    reason_str = f"{top_reason.index[0]}" if not top_reason.empty else "未知"
    return f"平均赢单率: {avg_win:.2f}; 主要排除原因: {reason_str}"

# Q45: 中国移动 流失原因
def get_cmcc_loss():
    cmcc_df = opp_df[opp_df['customer_name'] == '中国移动通信集团公司']
    reasons = cmcc_df['exclude_reason'].value_counts().head(2).to_dict()
    return f"主要原因分布: {reasons}"

# Q46: 2025 H1 业绩与大雷
def get_2025h1_outlook():
    start = pd.Timestamp('2025-01-01')
    end = pd.Timestamp('2025-06-30')
    h1_df = opp_df[(opp_df['est_deal_date'] >= start) & (opp_df['est_deal_date'] <= end)]
    total = h1_df['opp_amount'].sum()
    # Risk: high amount (>3000) but low win rate (<0.3)
    risks = h1_df[(h1_df['opp_amount'] > 3000) & (h1_df['win_rate'] < 0.3)]['opp_name'].head(2).tolist()
    return f"预计总额: {total:.2f}; 风险项目示例: {risks}"

# Q47: 未来3个月主力 Sales
def get_future_star():
    start = pd.Timestamp('2025-02-12') # Assuming today
    end = start + pd.DateOffset(months=3)
    future_df = opp_df[(opp_df['est_deal_date'] >= start) & (opp_df['est_deal_date'] <= end)]
    if future_df.empty: return "None"
    top_sales = future_df.groupby('owner_id')['opp_amount'].sum().nlargest(1)
    return f"{top_sales.index[0]} (预计: {top_sales.values[0]:.2f})"

# Q48: 潜力产品线 (Pipeline & Win Rate)
def get_potential_line():
    stats = opp_df.groupby('legion_product_line').agg({'opp_amount': 'sum', 'win_rate': 'mean'})
    # Simple score: amount * win_rate
    stats['score'] = stats['opp_amount'] * stats['win_rate']
    top = stats.nlargest(1, 'score')
    return f"{top.index[0]} (储备: {top['opp_amount'].values[0]:.0f}, 赢单率: {top['win_rate'].values[0]:.2f})"

# Q49: 耗时最长阶段 (Current Bottleneck)
def get_bottleneck_stage():
    # Since we don't have history, check where most active opps are stuck
    active_df = opp_df[opp_df['life_status'] == '活跃']
    stage_counts = active_df['sales_process'].value_counts().head(1)
    return f"当前滞留最多的阶段: {stage_counts.index[0]} ({stage_counts.values[0]}个)"

# Q50: 高赢单率回款预期
def get_high_prob_return():
    high_prob = opp_df[opp_df['win_rate'] > 0.6]
    # Assume amount as return for now
    total = high_prob['opp_amount'].sum()
    return f"{total:.2f}"

# Q51: Top 10 商机风险
def get_top10_risk():
    top10 = opp_df.nlargest(10, 'opp_amount')
    risky = top10[top10['exclude_reason'].notnull()]['opp_name'].tolist()
    return f"Top10中存在排除原因的: {risky}"

# Q52: 增收不增利 (Low Margin Contracts)
def get_low_margin_contracts():
    # High Sales (>1000w) but Low Margin (< 10%)
    bad_cons = con_df[(con_df['sales_amount_total'] > 10000000) & (con_df['gross_margin_rate'] < 0.1)]
    return f"大额低毛利合同数: {len(bad_cons)}"

# Q53: 华为依赖风险
def get_huawei_dependency():
    hw_df = opp_df[opp_df['customer_name'].str.contains('华为', na=False)]
    if hw_df.empty: return "No data"
    line_dist = hw_df['legion_product_line'].value_counts(normalize=True).head(1)
    return f"华为商机主要集中在: {line_dist.index[0]} (占比: {line_dist.values[0]:.0%})"

# Q54: 推进阶段赢单率低
def get_abnormal_low_win():
    # Stage advanced but win_rate < 0.2
    abnormal = opp_df[(opp_df['sales_process'].isin(['推进明确建设方案', '进入项目审批流程'])) & (opp_df['win_rate'] < 0.2)]
    return f"异常商机数: {len(abnormal)}; 示例: {abnormal['opp_name'].head(1).values}"

# Q55: 销售负荷
def get_sales_load():
    active = opp_df[opp_df['life_status'] == '活跃']
    load = active['owner_id'].value_counts().head(1)
    return f"负荷最重: {load.index[0]} ({load.values[0]}个活跃商机)"

# Q56-60 (Advice generation based on data)
# These are logic-based, we provide data context

# Output
answers = {
    "Q41": get_exclude_reason_dist(),
    "Q42": get_risk_concentration(),
    "Q43": get_wangfang_issues(),
    "Q44": get_shuzhi_low_win(),
    "Q45": get_cmcc_loss(),
    "Q46": get_2025h1_outlook(),
    "Q47": get_future_star(),
    "Q48": get_potential_line(),
    "Q49": get_bottleneck_stage(),
    "Q50": get_high_prob_return(),
    "Q51": get_top10_risk(),
    "Q52": get_low_margin_contracts(),
    "Q53": get_huawei_dependency(),
    "Q54": get_abnormal_low_win(),
    "Q55": get_sales_load(),
}

print("--- 开放问题参考答案 (基于数据支撑) ---")
for q, a in answers.items():
    print(f"[{q}] 数据支撑: {a}")

print("\n--- 建议类问题 (Q56-Q60) 逻辑 ---")
print("[Q56] 预算不足: 建议基于 Q41 数据，若'预算不足'占比高，推荐推行分期付款或模块化报价。")
print("[Q57] 软件智能冲刺: 建议关注 Q47 识别出的主力，以及 Q50 中的高赢单率项目。")
print("[Q58] 激活休眠: 针对 Q12/Q15 统计的休眠商机，建议按 Owner 盘点，如李明。")
print("[Q59] 技术评估: 针对 Q13/Q38 发现的技术卡点，建议产研介入。")
print("[Q60] 资源投入: 建议投向 Q48 识别出的高潜力产品线。")
