import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def optimize_metrics():
    file_path = r'test_plan\经分智能体测试方案2.0.docx'
    try:
        doc = docx.Document(file_path)
    except Exception as e:
        print(f"Error opening document: {e}")
        return

    # Find where "四. 测试指标" starts
    metrics_idx = -1
    for i, p in enumerate(doc.paragraphs):
        if '四. 测试指标' in p.text or '测试指标' in p.text:
            metrics_idx = i
            break
            
    if metrics_idx == -1:
        print("未找到四. 测试指标")
        return

    # We also need to locate Table 2 and remove it.
    # In python-docx, getting the exact table associated with a paragraph can be tricky.
    # But we know it's the last table in the doc currently.
    table_to_remove = None
    for tbl in doc.tables:
        if len(tbl.rows) > 0 and '指标名称' in tbl.rows[0].cells[0].text:
            table_to_remove = tbl
            break

    target_p = doc.paragraphs[metrics_idx]
    target_p.text = '四. 核心度量指标体系 (Core Evaluation Metrics)'
    
    # We will remove the paragraph immediately following "四. 测试指标"
    # because it currently says "综合通过率：准确率≥4.5分 + 一致性100%"
    next_p = doc.paragraphs[metrics_idx + 1]
    if '综合通过率' in next_p.text or '综合' in next_p.text:
        next_p._element.getparent().remove(next_p._element)

    # Insert the new content before the next heading (which is 五. 自动化...)
    # Actually, we can just insert after target_p
    insert_point = target_p

    def insert_after(prev_element, text, bold_prefix=""):
        p = prev_element.insert_paragraph_before('')
        # Hack to move it after: python-docx only has insert_paragraph_before, so we insert before the NEXT paragraph
        pass

    # Find index of '五. '
    next_heading_idx = -1
    for i in range(metrics_idx + 1, len(doc.paragraphs)):
        if '五.' in doc.paragraphs[i].text:
            next_heading_idx = i
            break
            
    insert_target = doc.paragraphs[next_heading_idx] if next_heading_idx != -1 else None

    if insert_target:
        p1 = insert_target.insert_paragraph_before('本方案摒弃了传统的单一黑盒打分，构建了涵盖“精确度、鲁棒性、可溯源性”的 3D 黄金度量矩阵，以确保智能体在真实高管应用场景下的极致可靠。')
        
        # Table generation or bullet points? A table is better.
        table = insert_target.insert_paragraph_before().insert_paragraph_before()._parent.add_table(rows=1, cols=5, width=docx.shared.Inches(6))
        # Move the table to before insert_target:
        p_element = insert_target._element
        table_element = table._element
        p_element.addprevious(table_element)
        
        # Set table header
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '核心度量维度'
        hdr_cells[1].text = '指标定义与评判逻辑'
        hdr_cells[2].text = '量化计算方式'
        hdr_cells[3].text = '企业级目标阈值'
        hdr_cells[4].text = '适用场景'
        
        row1 = table.add_row().cells
        row1[0].text = '多维准确性\n(Multidimensional Accuracy)'
        row1[1].text = '事实与逻辑双重校验。确保数据检索不漏、业务计算不错、逻辑推演不偏。'
        row1[2].text = '非开放题：自动化精准比对匹配度\n开放题：LLM 裁判 1-5 分量化矩阵 (事实/洞察/建议)'
        row1[3].text = '非开放题：100%\n开放题：平均分 ≥ 4.5'
        row1[4].text = '全量题库\n(非开放 + 开放)'
        
        row2 = table.add_row().cells
        row2[0].text = '一致性与鲁棒性\n(Consistency & Robustness)'
        row2[1].text = '面对相同的高阶经营提问或存在微小扰动的 Prompt 时，系统能否提供绝对稳定的解答输出。'
        row2[2].text = '高并发压力测试下，对同一问题抽样 20 次并计算输出结果的零差异比率。'
        row2[3].text = '100% 零差异率'
        row2[4].text = '重点针对大额合同与高危商机类的严谨查询'
        
        row3 = table.add_row().cells
        row3[0].text = '零幻觉溯源率\n(Zero-Hallucination)'
        row3[1].text = '输出文本中引用的任意具体数值、阶段名称或最终用户实体，必须 100% 拥有底层测试数据集的引用依据凭证。严防模型脑补。'
        row3[2].text = '实体链接穿透率计算：由 LLM 裁判提取数值/实体，并交由脚本与源库比对，计算捏造实体个数。'
        row3[3].text = '绝对 0 幻觉\n(容忍度 0%)'
        row3[4].text = '全量开放问题深度分析段落'

        # table.style = 'Table Grid'
        
        insert_target.insert_paragraph_before('')

    # Remove the old table
    if table_to_remove:
        table_to_remove._element.getparent().remove(table_to_remove._element)

    try:
        doc.save(file_path)
        print("【四. 测试指标】已完成极致优化！")
    except Exception as e:
        print(f"保存文件失败: {e}")

if __name__ == '__main__':
    optimize_metrics()