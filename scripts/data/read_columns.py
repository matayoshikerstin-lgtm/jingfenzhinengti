import pandas as pd
import sys
import os

# Set encoding for output to handle Chinese characters correctly
sys.stdout.reconfigure(encoding='utf-8')

# Try both Z: and D: paths
excel_paths = [
    r'Z:\jingfenzhinengti\测试数据\总数据.xlsx',
    r'd:\经分智能体\仓库\jingfenzhinengti\测试数据\总数据.xlsx'
]

for excel_path in excel_paths:
    print(f"Trying path: {excel_path}")
    try:
        if os.path.exists(excel_path):
            print("File exists!")
            xls = pd.ExcelFile(excel_path)
            print("Sheets found:", xls.sheet_names)
            
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name, nrows=0)
                print(f"\n--- Sheet: {sheet_name} ---")
                print(list(df.columns))
            break # Success
        else:
            print("File not found via os.path.exists")
    except Exception as e:
        print(f"Error accessing {excel_path}: {e}")
