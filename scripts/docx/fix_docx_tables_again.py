import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re

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

# Update DOCX
doc = docx.Document(r'test_plan\经分智能体测试方案2.0.docx')

start_idx = -1
end_idx = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "3. 测试用例与评分展示（典型示例）":
        start_idx = i
    elif p.text.strip().startswith("四.") or p.text.strip().startswith("四、"):
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    # Clear text between
    for i in range(start_idx + 1, end_idx):
        doc.paragraphs[i].text = ""

    # Clear tables that might be in between
    for t in doc.tables:
        t._element.getparent().remove(t._element)

    target_p = doc.paragraphs[end_idx]

    def insert_paragraph_before(p, text, bold=False):
        new_p = p.insert_paragraph_before("")
        run = new_p.add_run(text)
        if bold:
            run.bold = True
        return new_p

    insert_paragraph_before(target_p, "为了更直观地展示打分逻辑，以下提供了开放与非开放问题的标准范例与评分解析：\n")

    insert_paragraph_before(target_p, "【示例 A】非开放问题（客观事实与逻辑计算）", bold=True)
    insert_paragraph_before(target_p, "• 测试提问：“当前总金额超千万且净利率低于 10% 的大额低利润合同共有多少个？”")
    insert_paragraph_before(target_p, "• Ground Truth（系统真理）：28")

    p_for_table = target_p.insert_paragraph_before("")
    table_a = doc.add_table(rows=3, cols=4)
    set_table_borders(table_a)
    p_for_table._p.addnext(table_a._tbl)
    p_for_table._element.getparent().remove(p_for_table._element)

    cells = table_a.rows[0].cells
    cells[0].text = '回复质量'
    cells[1].text = '智能体回复示例'
    cells[2].text = '自动化评估逻辑'
    cells[3].text = '最终得分'

    cells = table_a.rows[1].cells
    cells[0].text = '优秀'
    cells[1].text = '“根据系统数据查询，当前金额超千万且净利率<10%的合同共有 28 个。”'
    cells[2].text = '自动化脚本判定：正则精准提取到核心数值 28，与 Ground Truth 完全等值匹配。'
    cells[3].text = '5 分'

    cells = table_a.rows[2].cells
    cells[0].text = '不及格'
    cells[1].text = '“当前此类大额低利合同共有 25 个，主要集中在软件智能业务线。”'
    cells[2].text = '自动化脚本判定：提取数值为 25，与事实严重不符，判定为计算错误或出现幻觉。'
    cells[3].text = '0 分'

    insert_paragraph_before(target_p, "\n【示例 B】开放问题（主观洞察与策略推演）", bold=True)
    insert_paragraph_before(target_p, "• 测试提问：“为什么数智运营产品线的商机转化率偏低？请结合数据给出破局建议。”")
    insert_paragraph_before(target_p, "• 标准评估基准（三段式 Target）：")
    insert_paragraph_before(target_p, "  1) 事实与数据：赢单率约 51.37%，排除原因 Top2 为商务条款(25个)与延期(25个)。")
    insert_paragraph_before(target_p, "  2) 洞察与分析：转化偏低的核心流失原因为“项目周期拖延”与“商务价格底线未达成一致”。")
    insert_paragraph_before(target_p, "  3) 落地建议：建立里程碑追踪防延期，推出模块化/分级报价方案降低商务门槛。")

    p_for_table_b = target_p.insert_paragraph_before("")
    table_b = doc.add_table(rows=3, cols=4)
    set_table_borders(table_b)
    p_for_table_b._p.addnext(table_b._tbl)
    p_for_table_b._element.getparent().remove(p_for_table_b._element)

    cells = table_b.rows[0].cells
    cells[0].text = '回复质量'
    cells[1].text = '智能体回复示例'
    cells[2].text = 'LLM 裁判打分逻辑拆解'
    cells[3].text = '最终得分'

    cells = table_b.rows[1].cells
    cells[0].text = '优秀'
    cells[1].text = '“目前数智运营产品线赢单率徘徊在 51% 左右，主要痛点在于商务条款分歧以及项目审批延期导致大量商机流失。建议针对延期现象设立阶段停留红线并加强追踪；针对商务难点，方案团队应推出敏捷版/豪华版的梯次化报价策略，以提升最终转化。”'
    cells[2].text = '事实层(2分)：覆盖核心数据。\n洞察层(1.5分)：指出延期与条款痛点。\n建议层(1.5分)：梯次报价与防延期追踪完全具备实操性。'
    cells[3].text = '5 分'

    cells = table_b.rows[2].cells
    cells[0].text = '不及格'
    cells[1].text = '“数智运营产品线商机转化率低主要是因为前端销售团队不够努力，产品缺乏吸引力。建议大家多跑一线跟客户沟通，了解客户真实想法，争取多签单。”'
    cells[2].text = '事实层(0分)：完全缺失真实数据。\n洞察层(0.5分)：归因流于表面。\n建议层(0.5分)：建议宽泛空洞，属无效车轱辘话。'
    cells[3].text = '1 分\n(触发人工复检)'

    doc.save(r'test_plan\经分智能体测试方案2.0.docx')
    print("Word Document updated with correct table placement.")
