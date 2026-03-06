import docx
from docx.shared import Inches

doc = docx.Document(r'test_plan\经分智能体测试方案2.0.docx')

for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith('五.') or p.text.strip().startswith('五、'):
        # Insert the image right after this paragraph
        run = p.add_run()
        run.add_break()
        run.add_picture(r'test_plan\flowchart.png', width=Inches(6.0))
        break

doc.save(r'test_plan\经分智能体测试方案2.0.docx')
print("Image inserted into Word document.")
