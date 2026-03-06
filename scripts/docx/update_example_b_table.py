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

# Find the Table for Example B
# We can look for the table where the first cell starts with '回复质量' and second is '智能体回复示例' and third is 'LLM 裁判打分逻辑拆解'

target_table = None
for table in doc.tables:
    if len(table.rows) >= 3 and len(table.rows[0].cells) == 4:
        if 'LLM 裁判打分逻辑拆解' in table.rows[0].cells[2].text:
            target_table = table
            break

if target_table:
    # We need to replace this table with a 6-column table.
    # We can create a new table right after it, and delete the old one.
    
    new_table = doc.add_table(rows=3, cols=6)
    set_table_borders(new_table)
    
    # Move the new table right after the target_table
    target_table._element.addnext(new_table._element)
    
    # Fill new table
    cells = new_table.rows[0].cells
    cells[0].text = '评级'
    cells[1].text = '智能体回复示例'
    cells[2].text = '事实与数据层\n(满分2分)'
    cells[3].text = '归纳与分析层\n(满分1.5分)'
    cells[4].text = '落地与建议层\n(满分1.5分)'
    cells[5].text = '最终得分'

    for cell in cells:
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                
    cells = new_table.rows[1].cells
    cells[0].text = '🟢 优秀'
    cells[1].text = '“目前数智运营产品线赢单率徘徊在 51% 左右，主要痛点在于商务条款分歧以及项目审批延期导致大量商机流失。建议针对延期现象设立阶段停留红线并加强追踪；针对商务难点，方案团队应推出敏捷版/豪华版的梯次化报价策略，以提升最终转化。”'
    cells[2].text = '得 2 分\n覆盖核心数据。'
    cells[3].text = '得 1.5 分\n精准指出延期与条款痛点。'
    cells[4].text = '得 1.5 分\n梯次报价与防延期追踪完全具备实操性。'
    cells[5].text = '5 分'
    
    cells = new_table.rows[2].cells
    cells[0].text = '🔴 不及格'
    cells[1].text = '“数智运营产品线商机转化率低主要是因为前端销售团队不够努力，产品缺乏吸引力。建议大家多跑一线跟客户沟通，了解客户真实想法，争取多签单。”'
    cells[2].text = '得 0 分\n完全缺失真实数据支撑。'
    cells[3].text = '得 0.5 分\n归因流于表面，无视真实记录。'
    cells[4].text = '得 0.5 分\n建议宽泛空洞，属车轱辘话。'
    cells[5].text = '1 分\n(人工复检)'

    # Make "得 X 分" bold in cells
    for row_idx in [1, 2]:
        for col_idx in [2, 3, 4, 5]: # also final score
            for p in new_table.rows[row_idx].cells[col_idx].paragraphs:
                for r in p.runs:
                    if '得' in r.text or '分' in r.text:
                        r.bold = True
                        
    # Delete the old table
    target_table._element.getparent().remove(target_table._element)
    
    doc.save(r'test_plan\经分智能体测试方案2.0.docx')
    print("Example B table replaced successfully.")
else:
    print("Target table not found.")
