import docx

doc = docx.Document(r'test_plan\经分智能体测试方案2.0.docx')

for p in doc.paragraphs:
    if "忽略排版格式，穿透底层语义" in p.text:
        p.text = p.text.replace("忽略排版格式，穿透底层语义", "忽略智能体的回答的表面排版格式，纯粹穿透底层要义，考察其是否涵盖三大核心考点。")

doc.save(r'test_plan\经分智能体测试方案2.0.docx')
print("Replaced successfully in docx")
