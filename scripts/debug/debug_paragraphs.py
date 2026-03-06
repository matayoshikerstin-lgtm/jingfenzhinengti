import docx

doc = docx.Document(r'test_plan\经分智能体测试方案2.0.docx')

with open('debug_paragraphs.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text:
            f.write(f'{i}: {text}\n')
