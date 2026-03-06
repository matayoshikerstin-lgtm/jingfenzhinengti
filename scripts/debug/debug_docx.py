import docx
import sys

sys.setrecursionlimit(2000)

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('utf-8', errors='ignore').decode('utf-8'))

def debug_docx(file_path):
    doc = docx.Document(file_path)
    print("Scanning tables...")
    for i, table in enumerate(doc.tables):
        print(f"Table {i}")
        for j, row in enumerate(table.rows):
            for k, cell in enumerate(row.cells):
                text = cell.text
                if "高并发" in text:
                    safe_print(f"FOUND '高并发' in Table {i} Row {j} Cell {k}")
                if "零差异" in text:
                    safe_print(f"FOUND '零差异' in Table {i} Row {j} Cell {k}")

if __name__ == "__main__":
    debug_docx(r"d:\jfznt\仓库\jingfenzhinengti\test_plan\经分智能体测试方案2.0.docx")
