import docx
from docx.shared import RGBColor, Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_COLOR_INDEX

def add_missing_table(file_path):
    print(f"Opening {file_path}")
    doc = docx.Document(file_path)
    
    # Create the table first (detached or at end)
    table = doc.add_table(rows=1, cols=4)
    try:
        table.style = 'Table Grid'
    except:
        try:
            table.style = '网格型'
        except:
            pass # Use default
            
    # Header
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '核心维度'
    hdr_cells[1].text = '评判逻辑'
    hdr_cells[2].text = '量化与验证方式'
    hdr_cells[3].text = '目标阈值'
    
    # Row 1
    row_cells = table.add_row().cells
    row_cells[0].text = '多维准确性 (Multidimensional Accuracy)'
    row_cells[1].text = '事实与逻辑双重校验。确保数据检索不漏、业务计算不错、逻辑推演不偏。'
    row_cells[2].text = '非开放题采用“脚本精准比对匹配度”；开放题采用“LLM 裁判 1-5 分量化矩阵”。'
    row_cells[3].text = '非开放题准确率 100%； 开放题平均分 ≥ 4.5 分。'
    
    # Row 2 (Consistency) - WITH RED TEXT
    row_cells = table.add_row().cells
    row_cells[0].text = '一致性与鲁棒性 (Consistency & Robustness)'
    row_cells[1].text = '面对相同的高阶经营提问或存在微小扰动的 Prompt 时，系统能否提供绝对稳定的解答输出。'
    
    # Cell 2: Mixed text
    p = row_cells[2].paragraphs[0]
    p.add_run('在高并发压力测试下，对同一问题抽样 20 次并计算输出结果的零差异比率。')
    run = p.add_run('非开放题要求结果绝对一致；开放题要求核心观点与数据无冲突，允许措辞微调（语义一致性）。')
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    # Cell 3: Mixed text
    p = row_cells[3].paragraphs[0]
    p.add_run('100% 零差异率。')
    run = p.add_run('（非开放题 100% 零差异；开放题语义一致性 ≥ 95%）')
    run.font.color.rgb = RGBColor(255, 0, 0)
    
    # Row 3
    row_cells = table.add_row().cells
    row_cells[0].text = '零幻觉溯源率 (Zero-Hallucination)'
    row_cells[1].text = '输出文本中引用的任意具体数值、阶段名称或最终用户实体，必须 100% 拥有底层测试数据集的引用依据凭证。严防模型脑补。'
    row_cells[2].text = '实体链接穿透率计算：由 LLM 裁判提取数值/实体，交由交叉脚本与原始数据表做溯源比对。'
    row_cells[3].text = '绝对 0 幻觉 （容忍度 0%）。'

    # Move table
    insert_p = None
    for p in doc.paragraphs:
        if "核心度量指标体系" in p.text:
            insert_p = p
            break
            
    if insert_p:
        print("Found insertion point.")
        body = doc.element.body
        p_index = -1
        # Find index of insert_p element in body
        for i, element in enumerate(body):
            if element == insert_p._element:
                p_index = i
                break
        
        if p_index != -1:
            # Insert after the next paragraph (intro sentence)
            # Check if next paragraph exists
            target_index = p_index + 2
            if target_index < len(body):
                target_element = body[target_index]
                # Insert before target_element? No, insert at index.
                # lxml insert takes index and element.
                # But body is not a list, it's an element.
                # body.insert(index, element)
                
                # We need to remove table from end and insert here.
                tbl = table._element
                body.remove(tbl) # Remove from end
                body.insert(target_index, tbl)
                print("Table moved successfully.")
            else:
                # Append (already there)
                pass
        else:
            print("Could not find paragraph in body.")
            
    doc.save(file_path)
    print("Done")

if __name__ == "__main__":
    add_missing_table(r"d:\jfznt\仓库\jingfenzhinengti\test_plan\经分智能体测试方案2.0.docx")
