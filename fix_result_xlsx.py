# 将 result.xlsx 从 TSV 文本转为真正的 Excel，解决用 Excel 打开乱码的问题
# 依赖: pip install pandas openpyxl

import os

def main():
    path = os.path.join(os.path.dirname(__file__), 'test_result', 'result.xlsx')
    if not os.path.exists(path):
        print(f'文件不存在: {path}')
        return

    import pandas as pd

    # 当前 result.xlsx 可能是 TSV 文本，编码多为 GBK（中文 Windows）或 UTF-8
    content = None
    for enc in ('gbk', 'gb2312', 'utf-8', 'utf-8-sig'):
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if content is None:
        raise SystemExit('无法用常见编码读取文件。')

    df = pd.read_csv(__import__('io').StringIO(content), sep='\t', dtype=str)
    df = df.fillna('')  # 空单元格

    # 先写入新文件，避免原文件被 Excel/编辑器占用无法覆盖
    out_dir = os.path.dirname(path)
    out_path = os.path.join(out_dir, 'result_fixed.xlsx')
    df.to_excel(out_path, index=False, engine='openpyxl')
    print('已生成可正常打开的 Excel 文件:', out_path)
    print('请关闭 result.xlsx 后，用 result_fixed.xlsx 替换它，或直接使用 result_fixed.xlsx。')

if __name__ == '__main__':
    main()
