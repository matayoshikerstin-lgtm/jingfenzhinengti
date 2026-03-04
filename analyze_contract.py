import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('test_data/测试数据.xlsx', sheet_name='合同')
print('Total Contracts:', len(df))

# Columns to numeric
num_cols = ['销售额汇总(元)', '合同毛利(元)', '净利润(元)', '毛利率', '净利率', '费毛率', '硬件毛利率', '成本总额', '硬件成本总额']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# 1. 增收不增利 (High sales, low/negative net profit)
bad_profit = df[(df['销售额汇总(元)'] > 10000000) & (df['净利率'] < 0.1)]
print(f'\n1. 大额(>1000万)但净利率<10%的合同数: {len(bad_profit)}')

# 2. 客户集中度
top_cust = df.groupby('最终用户')['销售额汇总(元)'].sum().nlargest(3)
print(f'\n2. 头部客户销售额Top3:\n{top_cust}')

# 3. 业务单元毛利表现
bu_profit = df.groupby('所属业务单元').agg(
    合同数=('id', 'count'),
    总销售额=('销售额汇总(元)', 'sum'),
    平均毛利率=('毛利率', 'mean'),
    平均净利率=('净利率', 'mean')
)
print(f'\n3. BU利润表现:\n{bu_profit}')

# 4. 销售个人表现 (Sales star)
top_owner = df.groupby('负责人').agg(销售额=('销售额汇总(元)', 'sum'), 净利润=('净利润(元)', 'sum')).nlargest(3, '销售额')
print(f'\n4. 头部销售:\n{top_owner}')

# 5. 硬件成本占比过高的项目风险
if '硬件成本总额' in df.columns and '成本总额' in df.columns:
    df['硬件成本占比'] = df['硬件成本总额'] / df['成本总额']
    hw_heavy = df[df['硬件成本占比'] > 0.5]
    print(f'\n5. 硬件成本占比>50%的合同数: {len(hw_heavy)}')

# 6. 亏损合同 (净利润 < 0)
loss_con = df[df['净利润(元)'] < 0]
print(f'\n6. 亏损合同数: {len(loss_con)}')

# 7. 毛利率与净利率倒挂
diff_profit = df[(df['毛利率'] > 0.4) & (df['净利率'] < 0.05)]
print(f'\n7. 高毛利(>40%)低净利(<5%)合同数: {len(diff_profit)}')

# 8. 周期
date_cols = ['合同发起日期', '合同归档时间', '提交合同评审分发时间', '评审完成时间']
for c in date_cols:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors='coerce')

if '合同发起日期' in df.columns and '合同归档时间' in df.columns:
    df['归档耗时'] = (df['合同归档时间'] - df['合同发起日期']).dt.days
    long_cycle = df[df['归档耗时'] > 60]
    print(f'\n8. 归档耗时>60天的合同数: {len(long_cycle)}, 平均耗时: {df["归档耗时"].mean()}天')

if '提交合同评审分发时间' in df.columns and '评审完成时间' in df.columns:
    df['评审耗时'] = (df['评审完成时间'] - df['提交合同评审分发时间']).dt.days
    long_review = df[df['评审耗时'] > 30]
    print(f'\n9. 评审耗时>30天的合同数: {len(long_review)}, 平均耗时: {df["评审耗时"].mean()}天')

print("\n10. 最差的费毛率 (费用占比极高):")
print(df.nlargest(3, '费毛率')[['合同名称', '费毛率', '净利率']])
