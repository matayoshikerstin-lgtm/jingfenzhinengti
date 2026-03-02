import pandas as pd

# Load Excel data
try:
    df = pd.read_excel('test_data/total_data.xlsx')
except Exception as e:
    print(f"Error loading file: {e}")
    exit(1)

# Preprocessing: Convert Chinese columns if needed, but we use them directly
# Relevant columns: '丢单/排除原因' (exclude_reason), '销售流程' (stage)

# Question Analysis: 为什么商机输单率（或排除率）这么高？主要受阻在哪些环节？

# 1. 统计丢单/排除原因的分布 (Why high loss rate?)
if '丢单/排除原因' in df.columns:
    reason_counts = df['丢单/排除原因'].value_counts()
    top_reasons = reason_counts.head(3).to_dict()
    total_excluded = reason_counts.sum()
else:
    top_reasons = "Column '丢单/排除原因' not found"
    total_excluded = 0

# 2. 统计受阻环节 (Where blocked?)
# We look at the stage distribution for opportunities that have an exclude_reason
if '丢单/排除原因' in df.columns and '销售流程' in df.columns:
    blocked_df = df[df['丢单/排除原因'].notnull()]
    stage_counts = blocked_df['销售流程'].value_counts()
    top_stages = stage_counts.head(3).to_dict()
else:
    top_stages = "Columns not found"

print(f"Q: 为什么我们的商机输单率（或排除率）这么高？主要受阻在哪些环节？")
print(f"答案数据支撑:")
print(f"1. 输单/排除总数: {total_excluded}")
print(f"2. 主要原因 (Top 3): {top_reasons}")
print(f"3. 主要受阻环节 (Top 3): {top_stages}")
