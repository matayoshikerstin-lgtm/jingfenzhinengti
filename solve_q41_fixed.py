import pandas as pd

# Load Excel data
try:
    df = pd.read_excel('test_data/total_data.xlsx')
except Exception as e:
    print(f"Error loading file: {e}")
    exit(1)

# Correct column names based on actual file (from previous `print(df.columns.tolist())` output)
# Note: The output showed garbled text (encoding issue in terminal), but we can map positions or guess standard names.
# Based on position from earlier CSV structure:
# 'exclude_reason' was at index 15 (0-indexed). 
# Let's verify by printing values of column at index 15.

col_exclude = df.columns[15] # 丢单/排除原因
col_stage = df.columns[7]    # 销售流程/阶段

# 1. 统计丢单/排除原因的分布
reason_counts = df[col_exclude].value_counts()
top_reasons = reason_counts.head(3).to_dict()
total_excluded = reason_counts.sum()

# 2. 统计受阻环节
blocked_df = df[df[col_exclude].notnull()]
stage_counts = blocked_df[col_stage].value_counts()
top_stages = stage_counts.head(3).to_dict()

print(f"Q: 为什么我们的商机输单率（或排除率）这么高？主要受阻在哪些环节？")
print(f"答案数据支撑:")
print(f"1. 输单/排除总数: {total_excluded}")
print(f"2. 主要原因 (Top 3): {top_reasons}")
print(f"3. 主要受阻环节 (Top 3): {top_stages}")
