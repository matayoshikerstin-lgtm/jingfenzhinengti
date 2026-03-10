from docx import Document
import sys
sys.stdout.reconfigure(encoding='utf-8')

doc = Document("d:/jfznt/仓库/jingfenzhinengti/test_plan/经分智能体测试方案2.0.docx")
print(f"总段落数: {len(doc.paragraphs)}")
for i, para in enumerate(doc.paragraphs):
    try:
        if para.runs and para.runs[0].bold and para.text.strip():
            print(f"[{i}] {para.text[:70]}")
    except:
        pass
