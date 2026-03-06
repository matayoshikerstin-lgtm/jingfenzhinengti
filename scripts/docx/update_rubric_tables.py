import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_table_borders(table):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        tblBorders = OxmlElement('w:tblBorders')
        for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            border = OxmlElement(f'w:{border_name}')
            border.set(qn('w:val'), 'single')
            border.set(qn('w:sz'), '4')
            border.set(qn('w:space'), '0')
            border.set(qn('w:color'), '000000')
            tblBorders.append(border)
        tblPr[0].append(tblBorders)

doc = docx.Document(r'test_plan\经分智能体测试方案2.0.docx')

# 1. Update non-open questions scoring
target_p1 = None
for p in doc.paragraphs:
    if "1-5 分量化打分标准：" in p.text:
        target_p1 = p
        break

if target_p1:
    # Delete the next 5 paragraphs (the bullet points)
    p_element = target_p1._p
    for _ in range(5):
        next_p = p_element.getnext()
        if next_p is not None:
            p_element.getparent().remove(next_p)

    # Insert table after target_p1
    table_p1 = target_p1.insert_paragraph_before("")
    target_p1._p.addnext(table_p1._p)
    
    table1 = doc.add_table(rows=6, cols=2)
    set_table_borders(table1)
    table_p1._p.addnext(table1._tbl)
    table_p1._element.getparent().remove(table_p1._element)

    cells = table1.rows[0].cells
    cells[0].text = '分值'
    cells[1].text = '打分标准'
    
    cells = table1.rows[1].cells
    cells[0].text = '5 分'
    cells[1].text = '核心数值/名单完全匹配，无多余错误信息。'
    
    cells = table1.rows[2].cells
    cells[0].text = '4 分'
    cells[1].text = '核心结论正确，但存在冗余的非关键错误信息或轻微单位格式瑕疵。'
    
    cells = table1.rows[3].cells
    cells[0].text = '3 分'
    cells[1].text = '列表型问题命中大部分（如 Top3 对了 2 个），或数值误差在极小可接受范围内。'
    
    cells = table1.rows[4].cells
    cells[0].text = '2 分'
    cells[1].text = '核心数据错误，但命中了部分相关实体，答非所问但大方向在相关领域。'
    
    cells = table1.rows[5].cells
    cells[0].text = '1 分'
    cells[1].text = '完全错误或产生严重幻觉（凭空捏造数据/名单）。'

    # Make header bold
    for cell in table1.rows[0].cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
    # Make points bold
    for row in table1.rows[1:]:
        for paragraph in row.cells[0].paragraphs:
            for run in paragraph.runs:
                run.bold = True

# 2. Update open questions scoring
target_p2 = None
for p in doc.paragraphs:
    if "忽略排版格式，穿透底层语义，LLM 裁判会对以下三个维度分别进行 1-5 分的独立打分" in p.text:
        target_p2 = p
        break

if target_p2:
    # Delete the next 18 paragraphs (the bullet points and spacing)
    p_element = target_p2._p
    count = 0
    while count < 18:
        next_p = p_element.getnext()
        if next_p is not None:
            p_element.getparent().remove(next_p)
            count += 1
        else:
            break

    # Insert table after target_p2
    table_p2 = target_p2.insert_paragraph_before("")
    target_p2._p.addnext(table_p2._p)
    
    table2 = doc.add_table(rows=4, cols=6)
    set_table_borders(table2)
    table_p2._p.addnext(table2._tbl)
    table_p2._element.getparent().remove(table_p2._element)

    cells = table2.rows[0].cells
    cells[0].text = '评分维度'
    cells[1].text = '5 分 (优秀)'
    cells[2].text = '4 分 (良好)'
    cells[3].text = '3 分 (及格)'
    cells[4].text = '2 分 (较差)'
    cells[5].text = '1 分 (极差)'

    cells = table2.rows[1].cells
    cells[0].text = '事实与数据层\n(40%权重)'
    cells[1].text = '精准提取所有关键业务数据和实体，无遗漏，与底层事实 100% 吻合。'
    cells[2].text = '提取大部分核心数据，次要数据轻微遗漏，不影响整体准确性。'
    cells[3].text = '存在部分关键数据缺失，或使用了模糊的定性描述而非精确数值。'
    cells[4].text = '关键数据提取错误或遗漏严重，事实基础薄弱。'
    cells[5].text = '完全没有引用数据，或出现严重的“数据幻觉”（凭空捏造）。'

    cells = table2.rows[2].cells
    cells[0].text = '归纳与分析层\n(30%权重)'
    cells[1].text = '洞察极其深刻，精准击中业务根因，逻辑推演严密且闭环。'
    cells[2].text = '分析逻辑合理，指出主要问题，但深度略显不足，偏向现象总结。'
    cells[3].text = '逻辑尚可，但分析较为模式化或套话，缺乏针对性解读。'
    cells[4].text = '归因错误，逻辑混乱，或结论与前文事实数据相矛盾。'
    cells[5].text = '毫无分析可言，仅重复数据，或完全答非所问。'

    cells = table2.rows[3].cells
    cells[0].text = '落地与建议层\n(30%权重)'
    cells[1].text = '建议极具实操性、针对性，能直接转化为管理动作（有明确抓手）。'
    cells[2].text = '建议具备一定可行性，方向正确，但在具体落地细节上略显宽泛。'
    cells[3].text = '建议属于行业“车轱辘话”（如“加强管理”），放之四海而皆准。'
    cells[4].text = '建议不切实际，或完全无法在当前业务场景下落地。'
    cells[5].text = '未给出任何建议，或给出的建议会对业务产生负面影响。'

    # Make header and first column bold
    for cell in table2.rows[0].cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
    for row in table2.rows[1:]:
        for paragraph in row.cells[0].paragraphs:
            for run in paragraph.runs:
                run.bold = True

doc.save(r'test_plan\经分智能体测试方案2.0.docx')
print("Tables created successfully.")
