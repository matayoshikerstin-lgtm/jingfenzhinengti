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

# Define questions and calculation logic
qa_pairs = []

# 1
ans1 = get_val(opp_df, 'opp_name', '中国农业银行股份有限公司智能营销项目', 'opp_amount')
qa_pairs.append(("Q1: “中国农业银行股份有限公司智能营销项目”的商机金额是多少？", ans1))

# 2
ans2 = get_val(opp_df, 'opp_id', 'O20241103', 'sales_process')
qa_pairs.append(("Q2: 商机“O20241103”（国家电网有限公司智能营销项目）当前的销售阶段是什么？", ans2))

# 3
ans3 = len(opp_df[opp_df['owner_id'] == 'U005-陈静'])
qa_pairs.append(("Q3: 销售负责人“U005-陈静”目前负责的商机数量是多少？", ans3))

# 4（合同名称有重名两条，用合同编号唯一确定）
ans4 = get_val(con_df, 'contract_approval_code', 'HT202410067', 'sales_amount_total')
qa_pairs.append(("Q4: 合同编号为“HT202410067”的合同（华为技术有限公司AI大模型应用合同）的销售总金额是多少？", ans4))

# 5
ans5 = get_val(opp_df, 'opp_id', 'O20241202', 'customer_name')
qa_pairs.append(("Q5: 商机“O20241202”的客户名称是什么？", ans5))

# 6
ans6 = get_val(con_df, 'contract_approval_code', 'HT202412220', 'archive_time')
qa_pairs.append(("Q6: 合同“HT202412220”（平安银行股份有限公司智慧运营合同）的归档时间是什么时候？", str(ans6)))

# 7
val7 = get_val(opp_df, 'opp_id', 'O20241204', 'est_deal_date')
ans7 = str(val7.date()) if hasattr(val7, 'date') else val7
qa_pairs.append(("Q7: 商机“O20241204”的预计签单日期是哪一天？", ans7))

# 8
ans8 = get_val(opp_df, 'opp_id', 'O20241202', 'life_status')
qa_pairs.append(("Q8: 客户“福建省农村信用社联合社”所属的商机（O20241202）目前的商机状态（life_status）是什么？", ans8))

# 9
ans9 = get_val(con_df, 'contract_approval_code', 'HT202503368', 'gross_margin_rate')
qa_pairs.append(("Q9: 合同“HT202503368”的毛利率（gross_margin_rate）是多少？", ans9))

# 10
ans10 = get_val(opp_df, 'opp_id', 'O20241019', 'exclude_reason')
qa_pairs.append(("Q10: 商机“O20241019”（中国建设银行股份有限公司智能客服项目）的排除原因是什么？", ans10))

# 11
ans11 = len(opp_df[opp_df['sales_process'] == '启动项目内部立项'])
qa_pairs.append(("Q11: 目前处于“启动项目内部立项”阶段的商机有多少个？", ans11))

# 12
ans12 = len(opp_df[opp_df['exclude_reason'] == '合同风险过高'])
qa_pairs.append(("Q12: 有多少个商机的排除原因是“合同风险过高”？", ans12))

# 13
ans13 = len(opp_df[(opp_df['customer_name'] == '中国移动通信集团公司') & (opp_df['life_status'] == '活跃')])
qa_pairs.append(("Q13: 客户“中国移动通信集团公司”目前有多少个活跃商机？", ans13))

# 14
ans14 = len(opp_df[opp_df['win_rate'] > 0.30])
qa_pairs.append(("Q14: 预计赢单率（win_rate）超过30%的商机有多少个？", ans14))

# 15
ans15 = len(opp_df[opp_df['life_status'] == '休眠'])
qa_pairs.append(("Q15: 处于“休眠”状态的商机有多少个？", ans15))

# 16
ans16 = len(opp_df[(opp_df['legion_product_line'] == '数智运营产品线') & (opp_df['opp_amount'] > 2000)])
qa_pairs.append(("Q16: “数智运营产品线”下，金额超过2000万元的商机有多少个？", ans16))

# 17
ans17 = len(opp_df[(opp_df['owner_id'] == 'U009-吴强') & (opp_df['sales_process'] == '推进明确建设方案')])
qa_pairs.append(("Q17: 销售负责人“U009-吴强”负责的且处于“推进明确建设方案”阶段的商机有多少个？", ans17))

# 18
ans18 = len(opp_df[opp_df['est_gross_profit'] > 1000])
qa_pairs.append(("Q18: 预计毛利（est_gross_profit）大于1000万元的商机有多少个？", ans18))

# 19
ans19 = len(con_df[con_df['sales_amount_total'] > 30000000])
qa_pairs.append(("Q19: 合同金额大于3000万元的合同有多少个？", ans19))

# 20
ans20 = len(opp_df[opp_df['business_unit_name'] == '软件智能'])
qa_pairs.append(("Q20: 归属部门为“软件智能”的商机有多少个？", ans20))

# 21
ans21 = opp_df[opp_df['owner_id'] == 'U005-陈静']['opp_amount'].sum()
qa_pairs.append(("Q21: 统计销售负责人“U005-陈静”名下所有商机的总金额是多少？", f"{ans21:.2f}"))

# 22
ans22 = opp_df[opp_df['legion_product_line'] == '营销决策产品线']['opp_amount'].sum()
qa_pairs.append(("Q22: “营销决策产品线”目前拥有的商机总金额是多少？", f"{ans22:.2f}"))

# 23
ans23 = opp_df[opp_df['win_rate'] > 0.30]['opp_amount'].sum()
qa_pairs.append(("Q23: 所有预计赢单率超过30%的商机总金额是多少？", f"{ans23:.2f}"))

# 24
ans24 = opp_df[(opp_df['owner_id'] == 'U009-吴强') & (opp_df['sales_process'] == '推进明确建设方案')]['opp_amount'].sum()
qa_pairs.append(("Q24: 销售负责人“U009-吴强”负责的且处于“推进明确建设方案”阶段的商机总金额是多少？", f"{ans24:.2f}"))

# 25
ans25 = con_df[con_df['final_user_name'] == '腾讯科技（深圳）有限公司']['sales_amount_total'].sum()
qa_pairs.append(("Q25: 客户“腾讯科技（深圳）有限公司”的所有合同总金额是多少？", f"{ans25:.2f}"))

# 26
ans26 = opp_df[opp_df['sales_process'] == '需求明确']['opp_amount'].mean()
qa_pairs.append(("Q26: 所有处于“需求明确”阶段商机的平均金额是多少？", f"{ans26:.2f}"))

# 27
mask_q27 = (opp_df['est_deal_date'] >= pd.Timestamp('2025-01-01')) & (opp_df['est_deal_date'] <= pd.Timestamp('2025-03-31'))
ans27 = opp_df[mask_q27]['opp_amount'].sum()
qa_pairs.append(("Q27: 2025年第一季度（1-3月）预计签单商机的总金额是多少？", f"{ans27:.2f}"))

# 28
ans28 = opp_df[opp_df['legion_product_line'] == '场景创新部']['est_gross_profit'].sum()
qa_pairs.append(("Q28: “场景创新部”目前拥有的商机总预计毛利是多少？", f"{ans28:.2f}"))

# 29
ans29 = con_df['net_profit'].sum()
qa_pairs.append(("Q29: 所有已签订合同的净利润（net_profit）总和是多少？", f"{ans29:.2f}"))

# 30
ans30 = opp_df[opp_df['owner_id'] == 'U002-李明']['opp_amount'].max()
qa_pairs.append(("Q30: 销售负责人“U002-李明”负责的所有商机中，最大的单笔商机金额是多少？", f"{ans30:.2f}"))

# 31
r31 = opp_df.nlargest(3, 'opp_amount')[['opp_name', 'opp_amount']]
ans31 = [f"{x[0]}({x[1]})" for x in r31.values]
qa_pairs.append(("Q31: 列出商机金额最大的前3个商机名称及其金额。", ", ".join(ans31)))

# 32
r32 = con_df.nlargest(1, 'gross_margin_rate')[['contract_name', 'gross_margin_rate']]
ans32 = f"{r32.iloc[0,0]} ({r32.iloc[0,1]})"
qa_pairs.append(("Q32: 哪一个合同的毛利率（gross_margin_rate）最高？请给出合同名称和毛利率。", ans32))

# 33
e_opp = opp_df.nsmallest(1, 'est_deal_date')[['opp_name', 'est_deal_date']]
if not e_opp.empty:
    ans33 = f"{e_opp.iloc[0,0]} ({e_opp.iloc[0,1].date()})"
else: ans33 = "None"
qa_pairs.append(("Q33: 哪一个商机的预计签单日期最早？请给出商机名称和日期。", ans33))

# 34
r34 = con_df.nsmallest(1, 'net_profit')[['contract_name', 'net_profit']]
ans34 = f"{r34.iloc[0,0]} ({r34.iloc[0,1]})"
qa_pairs.append(("Q34: 净利润（net_profit）最低的合同是哪一个？", ans34))

# 35
r35 = opp_df.nlargest(1, 'win_rate')[['opp_name', 'win_rate']]
ans35 = f"{r35.iloc[0,0]} ({r35.iloc[0,1]})"
qa_pairs.append(("Q35: 预计赢单率（win_rate）最高的商机是哪一个？", ans35))

# 36
mask_36 = (opp_df['customer_name'] == '中国农业银行股份有限公司') & (opp_df['sales_process'] == '启动项目内部立项')
r36 = opp_df[mask_36].nlargest(1, 'opp_amount')[['opp_name', 'opp_amount']]
ans36 = f"{r36.iloc[0,0]} ({r36.iloc[0,1]})" if not r36.empty else "无"
qa_pairs.append(("Q36: 客户“中国农业银行股份有限公司”相关的所有商机中，处于“启动项目内部立项”阶段且金额最大的商机是哪一个？", ans36))

# 37
mask_37 = (con_df['final_user_name'] == '华为技术有限公司')
r37 = con_df[mask_37].nlargest(2, 'sales_amount_total')[['contract_name', 'sales_amount_total']]
ans37 = [f"{x[0]} ({x[1]})" for x in r37.values]
qa_pairs.append(("Q37: 查找所有客户为“华为技术有限公司”的合同，并按金额从高到低排列，列出前2个。", ", ".join(ans37)))

# 38
ans38 = len(opp_df[(opp_df['owner_id'] == 'U003-王芳') & (opp_df['exclude_reason'] == '技术方案需重新评估')])
qa_pairs.append(("Q38: 销售负责人“U003-王芳”负责的商机中，有多少个是因为“技术方案需重新评估”而受阻的？", ans38))

# 39
ans39 = len(opp_df[(opp_df['business_unit_name'] == '软件智能') & (opp_df['life_status'] == '活跃') & (opp_df['win_rate'] > 0.50)])
qa_pairs.append(("Q39: 统计“软件智能”事业部下，所有处于“活跃”状态且预计赢单率大于50%的商机数量。", ans39))

# 40
opp_key = 'opp_id'
con_key = 'opp_code'
if opp_key in opp_df.columns and con_key in con_df.columns:
    merged = pd.merge(con_df, opp_df, left_on=con_key, right_on=opp_key, how='inner')
    filtered = merged[merged['sales_amount_total'] > merged['opp_amount']]
    ans40 = filtered['contract_name'].tolist()
else:
    ans40 = "Join keys not found"
qa_pairs.append(("Q40: 查找合同金额（sales_amount_total）大于其对应商机金额（opp_amount）的所有合同名称。", str(ans40)))

# Print results
for q, a in qa_pairs:
    print(f"**{q}**")
    print(f"> 答案: {a}")
    print()
