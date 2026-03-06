# -*- coding: utf-8 -*-
"""Inspect test_data/测试数据.xlsx and print structure + sample stats."""
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
path = r'test_data/测试数据.xlsx'
xls = pd.ExcelFile(path)
print('Sheets:', xls.sheet_names)

for s in xls.sheet_names:
    df = pd.read_excel(path, sheet_name=s)
    print('\n--- Sheet:', s, '---')
    print('rows:', len(df), '| cols:', list(df.columns))
    if '不纳入原因' in df.columns or '排除原因' in str(df.columns):
        exc_col = '不纳入原因' if '不纳入原因' in df.columns else [c for c in df.columns if '原因' in str(c)][0]
        cust_col = '客户名称' if '客户名称' in df.columns else [c for c in df.columns if '客户' in str(c)]
        cust_col = cust_col[0] if isinstance(cust_col, list) else cust_col
        risk = df[df[exc_col] == '合同风险过高']
        if not risk.empty and cust_col in risk.columns:
            top = risk[cust_col].value_counts().head(10)
            print('合同风险过高 按客户 Top10:', top.to_dict())
