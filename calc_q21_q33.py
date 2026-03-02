import pandas as pd
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load data
xl = pd.ExcelFile('test_data/测试数据.xlsx')
opp = pd.read_excel(xl, sheet_name='商机')
con = pd.read_excel(xl, sheet_name='合同')

# Ensure numeric
opp['商机金额'] = pd.to_numeric(opp['商机金额'], errors='coerce').fillna(0)
opp['预计毛利金额'] = pd.to_numeric(opp['预计毛利金额'], errors='coerce').fillna(0)
opp['赢单率'] = pd.to_numeric(opp['赢单率'], errors='coerce').fillna(0)
opp['预计成交日期'] = pd.to_datetime(opp['预计成交日期'], errors='coerce')

con['销售额汇总(元)'] = pd.to_numeric(con['销售额汇总(元)'], errors='coerce').fillna(0)
con['合同毛利(元)'] = pd.to_numeric(con['合同毛利(元)'], errors='coerce').fillna(0)
con['净利润(元)'] = pd.to_numeric(con['净利润(元)'], errors='coerce').fillna(0)
con['毛利率'] = pd.to_numeric(con['毛利率'], errors='coerce').fillna(0)
con['净利率'] = pd.to_numeric(con['净利率'], errors='coerce').fillna(0)

cutoff = pd.Timestamp('2026-02-11')

# Q21: Overdue opps
overdue = opp[(opp['预计成交日期'] < cutoff) & (opp['生命状态'].isin(['活跃', '休眠']))]
q21 = {
    'count': len(overdue),
    'sum_amount': float(overdue['商机金额'].sum()),
    'top_3_owners': overdue.groupby('负责人')['商机金额'].sum().nlargest(3).index.tolist()
}

# Q22: Top 5 opps by est_gross_profit
top5 = opp.nlargest(5, '预计毛利金额')[['商机名称', '负责人', '商机金额', '预计毛利金额']]
q22 = [{'name': r['商机名称'], 'owner': r['负责人'], 'amount': float(r['商机金额']), 'profit': float(r['预计毛利金额'])} for _, r in top5.iterrows()]

# Q23: Opp Amount by Sales Stage
q23 = opp.groupby('销售流程')['商机金额'].sum().sort_values(ascending=False).head(10).to_dict()
q23 = {k: float(v) for k, v in q23.items()}

# Q24: Dormant opps
dormant = opp[opp['生命状态'] == '休眠']
total_amt = opp['商机金额'].sum()
dormant_amt = dormant['商机金额'].sum()
q24 = {'amount': float(dormant_amt), 'ratio': float(dormant_amt / total_amt) if total_amt else 0}

# Q25: Opp Amount by Business Unit
q25 = opp.groupby('所属业务单元')['商机金额'].sum().to_dict()
q25 = {str(k): float(v) for k, v in q25.items()}

# Q26: Opps with Win Rate < 20%
low_win = opp[opp['赢单率'] < 0.20]
q26 = {'count': len(low_win), 'amount': float(low_win['商机金额'].sum())}

# Q27: Opp Amount by Product Line
q27 = opp.groupby('军团产品线')['商机金额'].sum().to_dict()
q27 = {str(k): float(v) for k, v in q27.items()}

# Q28: Exclude Ratio for Top 5 Customers (by opp count)
top5_cust = opp.groupby('客户名称').agg({'id': 'count', '商机金额': 'sum'}).nlargest(5, 'id')
top5_count = top5_cust['id'].sum()
top5_amt = top5_cust['商机金额'].sum()
total_count = len(opp)
total_opp_amt = opp['商机金额'].sum()
q28 = {
    'exclude_ratio_by_count': float(top5_count / total_count) if total_count else 0,
    'exclude_ratio_by_amount': float(top5_amt / total_opp_amt) if total_opp_amt else 0
}

# Q29: Top 3 High & Low Gross Margin Contracts
con_valid = con[con['毛利率'].notna() & (con['毛利率'] != 0)]
high3 = con_valid.nlargest(3, '毛利率')[['合同名称', '毛利率', '销售额汇总(元)', '合同毛利(元)']]
low3 = con_valid.nsmallest(3, '毛利率')[['合同名称', '毛利率', '销售额汇总(元)', '合同毛利(元)']]
q29 = {
    'top_3_high': [{'name': r['合同名称'], 'gross_margin': float(r['毛利率']), 'amount': float(r['销售额汇总(元)']), 'gross_profit': float(r['合同毛利(元)'])} for _, r in high3.iterrows()],
    'top_3_low': [{'name': r['合同名称'], 'gross_margin': float(r['毛利率']), 'amount': float(r['销售额汇总(元)']), 'gross_profit': float(r['合同毛利(元)'])} for _, r in low3.iterrows()]
}

# Q30: Top 5 Contract Customers by Amount
q30 = con.groupby('最终用户')['销售额汇总(元)'].sum().nlargest(5)
q30 = [{'customer': k, 'amount': float(v)} for k, v in q30.items()]

# Q31: Top 3 Sales Owners by Contract Amount
q31 = con.groupby('负责人')['销售额汇总(元)'].sum().nlargest(3)
q31 = [{'owner': k, 'amount': float(v)} for k, v in q31.items()]

# Q32: Top 3 Low Net Margin Contracts
con_nm = con[con['净利率'].notna()]
low_nm = con_nm.nsmallest(3, '净利率')[['合同名称', '净利率', '净利润(元)', '销售额汇总(元)']]
q32 = [{'name': r['合同名称'], 'net_margin': float(r['净利率']), 'net_profit': float(r['净利润(元)']), 'amount': float(r['销售额汇总(元)'])} for _, r in low_nm.iterrows()]

# Q33: 软件智能 BU Contract Performance
sw = con[con['所属业务单元'] == '软件智能']
q33 = {'amount': float(sw['销售额汇总(元)'].sum()), 'net_profit': float(sw['净利润(元)'].sum())}

result = {
    'Q21': q21, 'Q22': q22, 'Q23': q23, 'Q24': q24, 'Q25': q25,
    'Q26': q26, 'Q27': q27, 'Q28': q28, 'Q29': q29, 'Q30': q30,
    'Q31': q31, 'Q32': q32, 'Q33': q33
}
print(json.dumps(result, ensure_ascii=False, indent=2))
