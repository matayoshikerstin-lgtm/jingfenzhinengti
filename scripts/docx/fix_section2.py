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

# Find section 2
target_p = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("三.") or p.text.strip().startswith("三、"):
        target_p = p
        break

if target_p:
    def insert_paragraph_before(p_target, text, bold=False):
        new_p = p_target.insert_paragraph_before("")
        run = new_p.add_run(text)
        if bold:
            run.bold = True
        return new_p

    insert_paragraph_before(target_p, "• 输入数据源：构造高度拟真的高阶业务问题集（共 80 题），数据底座基于脱敏的真实系统报表（商机表、合同表、项目表等）。")
    insert_paragraph_before(target_p, "• 执行方式：通过 RPA（Robotic Process Automation）自动化脚本驱动 Edge 浏览器，在系统内网对话框中进行无人值守的批量问题注入与回答抓取，并将回复内容秒级落盘。")
    insert_paragraph_before(target_p, "• 问题分类与校验维度：")

    # Add table
    p_for_table = target_p.insert_paragraph_before("")
    table = doc.add_table(rows=3, cols=4)
    set_table_borders(table)
    p_for_table._p.addnext(table._tbl)
    p_for_table._element.getparent().remove(p_for_table._element)

    # Header
    cells = table.rows[0].cells
    cells[0].text = '问题类型'
    cells[1].text = '题型定义与特性'
    cells[2].text = '数量分布'
    cells[3].text = '核心评判标准与验证逻辑'
    
    # Make header bold
    for cell in cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True

    # Row 1
    cells = table.rows[1].cells
    cells[0].text = '非开放问题\n（硬逻辑校验）'
    cells[1].text = '客观事实查询、跨表统计、极值聚合。有绝对唯一的数值或明确的枚举列表答案。'
    cells[2].text = '50 题'
    cells[3].text = '事实级精准度 (Accuracy)。\n利用 Python 脚本正则匹配提取核心数值或特定实体，与 Ground Truth 进行 100% 强等值比对。'

    # Row 2
    cells = table.rows[2].cells
    cells[0].text = '开放问题\n（高维主观校验）'
    cells[1].text = '面向经营管理层的宏观主观分析、流失归因推演与高阶策略建议。'
    cells[2].text = '30 题'
    cells[3].text = '逻辑与建议可行性 (Insight & Action)。\n引入 LLM 裁判，依据“事实匹配、深度分析、建议有效性”三大维度进行结构化评分。'

    # Add spacing
    target_p.insert_paragraph_before("")

    doc.save(r'test_plan\经分智能体测试方案2.0.docx')
    print("Section 2 restored successfully.")
else:
    print("Could not find section 3 to insert before.")
