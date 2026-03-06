import docx
from docx.shared import RGBColor, Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_COLOR_INDEX

def update_docx(file_path):
    print(f"Opening {file_path}")
    doc = docx.Document(file_path)
    
    # 1. Update Consistency
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if "在高并发压力测试下" in p.text and "非开放题要求" not in p.text:
                         print("Found '在高并发压力测试下' in table")
                         run = p.add_run("非开放题要求结果绝对一致；开放题要求核心观点与数据无冲突，允许措辞微调（语义一致性）。")
                         run.font.color.rgb = RGBColor(255, 0, 0)
                    
                    if "100% 零差异率" in p.text and "非开放题" not in p.text:
                        print("Found '100% 零差异率' in table")
                        run = p.add_run("（非开放题 100% 零差异；开放题语义一致性 ≥ 95%）")
                        run.font.color.rgb = RGBColor(255, 0, 0)

    # 2. Update RPA section
    for p in doc.paragraphs:
        if "RPA 无人值守执行" in p.text and "result.xlsx" in p.text:
            print("Found RPA section")
            target_text = "，彻底消除"
            found_run_index = -1
            for i, run in enumerate(p.runs):
                if target_text in run.text:
                    found_run_index = i
                    break
            
            if found_run_index != -1:
                # Reconstruct paragraph
                runs_data = []
                for r in p.runs:
                    runs_data.append({
                        'text': r.text,
                        'bold': r.bold,
                        'italic': r.italic,
                        'color': r.font.color.rgb if r.font.color else None
                    })
                
                p.clear()
                
                for data in runs_data:
                    text = data['text']
                    if target_text in text:
                        parts = text.split(target_text)
                        
                        # Part 1
                        r1 = p.add_run(parts[0] + "。")
                        r1.bold = data['bold']
                        r1.italic = data['italic']
                        if data['color']: r1.font.color.rgb = data['color']
                        
                        # Red text
                        r_red = p.add_run("（注：脚本需内置异常重试机制，如元素加载超时自动重试 3 次，并详细记录失败用例以便排查）")
                        r_red.font.color.rgb = RGBColor(255, 0, 0)
                        
                        # Part 2
                        r2 = p.add_run("彻底消除" + parts[1])
                        r2.bold = data['bold']
                        r2.italic = data['italic']
                        if data['color']: r2.font.color.rgb = data['color']
                    else:
                        r = p.add_run(text)
                        r.bold = data['bold']
                        r.italic = data['italic']
                        if data['color']: r.font.color.rgb = data['color']
                print("Updated RPA section")

    # 3. Add Appendix
    found_appendix = False
    for p in doc.paragraphs:
        if "附录：LLM 裁判 Prompt 模板" in p.text:
            found_appendix = True
            break
    
    if not found_appendix:
        print("Adding Appendix")
        doc.add_page_break()
        
        # Try to find a heading style
        heading_style = None
        for style in doc.styles:
            if style.name == 'Heading 2' or style.name == '标题 2':
                heading_style = style
                break
        
        if heading_style:
            p = doc.add_paragraph('六、 附录：LLM 裁判 Prompt 模板', style=heading_style)
        else:
            p = doc.add_paragraph('六、 附录：LLM 裁判 Prompt 模板')
            p.runs[0].bold = True
            p.runs[0].font.size = Pt(16) # Approx Heading 2 size

        for run in p.runs:
            run.font.color.rgb = RGBColor(255, 0, 0)
            
        code_content = """{
  "role_definition": {
    "role": "资深经营分析总监兼质量审核官",
    "mission": "评估经分智能体回答的准确性、深度与落地性。",
    "tone": "严格、客观、数据驱动"
  },
  "evaluation_criteria": {
    "fact_check (1-5)": "是否包含所有关键数值和实体？有无幻觉？(权重 40%)",
    "analysis_depth (1-5)": "是否挖掘了数据背后的根因？逻辑是否闭环？(权重 30%)",
    "actionable_advice (1-5)": "建议是否具体可行？是否具备实操抓手？(权重 30%)"
  },
  "input_data": {
    "user_question": "{question}",
    "standard_answer": "{standard_answer}",
    "agent_response": "{agent_response}"
  },
  "output_format": {
    "type": "json",
    "schema": {
      "scores": {
        "fact": 0,
        "analysis": 0,
        "advice": 0
      },
      "weighted_total_score": 0.0,
      "reasoning": "扣分理由简述...",
      "is_hallucination": false,
      "need_human_review": false
    }
  }
}"""
        p = doc.add_paragraph(code_content)
        # Try 'No Spacing' or default
        try:
            p.style = 'No Spacing'
        except:
            pass
            
        for run in p.runs:
            run.font.color.rgb = RGBColor(255, 0, 0)
            run.font.name = 'Courier New'

    doc.save(file_path)
    print("Done")

if __name__ == "__main__":
    update_docx(r"d:\jfznt\仓库\jingfenzhinengti\test_plan\经分智能体测试方案2.0.docx")
