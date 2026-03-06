import pandas as pd
import sys

# Force output encoding
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'test_data/测试数据.xlsx'

try:
    # 加载商机表
    xls = pd.ExcelFile(file_path)
    sheet_name = next((s for s in xls.sheet_names if '商机' in s), None)
    if not sheet_name:
        print("未找到商机表")
        sys.exit()
        
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # 查找列名
    col_exclude = next((c for c in df.columns if '不纳入原因' in c), '不纳入原因')
    col_cust = next((c for c in df.columns if '客户名称' in c), '客户名称')
    
    # 筛选"合同风险过高"
    risk_df = df[df[col_exclude] == '合同风险过高']
    
    # 分组统计
    top_risk = risk_df[col_cust].value_counts().head(5)
    
    print(f"筛选条件: {col_exclude} == '合同风险过高'")
    print(f"总条数: {len(risk_df)}")
    print("Top 风险客户:")
    for cust, count in top_risk.items():
        print(f"{cust}: {count}")

except Exception as e:
    print(f"Error: {e}")
