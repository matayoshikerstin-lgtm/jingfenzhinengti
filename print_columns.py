import pandas as pd
import sys

# Force standard output to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('test_data/total_data.xlsx')
    # Print columns with index for clarity
    for idx, col in enumerate(df.columns):
        print(f"{idx}: {col}")
except Exception as e:
    print(f"Error: {e}")
