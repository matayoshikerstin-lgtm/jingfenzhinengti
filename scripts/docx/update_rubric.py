import docx

doc = docx.Document(r'test_plan\经分智能体测试方案2.0.docx')

# Update Section 1: 非开放问题
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("• 执行方法：自动化脚本对比智能体的文本输出"):
        p.text = "• 执行方法：自动化脚本提取智能体回复的核心数值或实体名单，与 Ground Truth 进行精准比对。"
        # Insert 1-5 rubric below
        p_target = p
        
        def insert_paragraph_after(p_target, text):
            new_p = p_target.insert_paragraph_before("")
            new_p.add_run(text)
            p_target._p.addnext(new_p._p)
            return new_p
        
        p1 = insert_paragraph_after(p_target, "• 1-5 分量化打分标准：")
        p2 = insert_paragraph_after(p1, "  - 5 分：核心数值/名单完全匹配，无多余错误信息。")
        p3 = insert_paragraph_after(p2, "  - 4 分：核心结论正确，但存在冗余的非关键错误信息或轻微单位格式瑕疵。")
        p4 = insert_paragraph_after(p3, "  - 3 分：列表型问题命中大部分（如 Top3 对了 2 个），或数值误差在极小可接受范围内。")
        p5 = insert_paragraph_after(p4, "  - 2 分：核心数据错误，但命中了部分相关实体，答非所问但大方向在相关领域。")
        p6 = insert_paragraph_after(p5, "  - 1 分：完全错误或产生严重幻觉（凭空捏造数据/名单）。")
        break

# Update Section 2: 开放问题
start_idx = -1
end_idx = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "核心评估理念：":
        start_idx = i
    elif p.text.strip() == "自动化测试实施路径：":
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    # Clear old text
    for i in range(start_idx + 1, end_idx):
        doc.paragraphs[i].text = ""
        
    p_insert = doc.paragraphs[end_idx]
    
    def insert_before(text, bold_prefix=None, rest_text=None):
        new_p = p_insert.insert_paragraph_before("")
        if bold_prefix:
            run = new_p.add_run(bold_prefix)
            run.bold = True
            if rest_text:
                new_p.add_run(rest_text)
        else:
            new_p.add_run(text)
        return new_p

    insert_before("忽略排版格式，穿透底层语义，LLM 裁判会对以下三个维度分别进行 1-5 分的独立打分，最终按权重核算总分：\n")
    
    insert_before("", bold_prefix="• 事实与数据层（40%权重，转化后满分2分）：")
    insert_before("  - 5 分：精准提取所有关键业务数据和实体，无任何遗漏，与底层事实 100% 吻合。")
    insert_before("  - 4 分：提取了大部分核心数据，次要数据轻微遗漏，但不影响整体事实准确性。")
    insert_before("  - 3 分：存在部分关键数据缺失，或使用了模糊的定性描述而非精确数值。")
    insert_before("  - 2 分：关键数据提取错误或遗漏严重，事实基础薄弱。")
    insert_before("  - 1 分：完全没有引用数据，或出现严重的“数据幻觉”（凭空捏造数值和实体）。\n")
    
    insert_before("", bold_prefix="• 归纳与分析层（30%权重，转化后满分1.5分）：")
    insert_before("  - 5 分：洞察极其深刻，精准击中业务根因，逻辑推演严密且闭环。")
    insert_before("  - 4 分：分析逻辑合理，指出主要问题，但深度略显不足，偏向现象总结。")
    insert_before("  - 3 分：逻辑尚可，但分析较为模式化或套话，缺乏对特定数据的针对性解读。")
    insert_before("  - 2 分：归因错误，逻辑混乱，或结论与前文事实数据相矛盾。")
    insert_before("  - 1 分：毫无分析可言，仅重复数据，或完全答非所问。\n")
    
    insert_before("", bold_prefix="• 落地与建议层（30%权重，转化后满分1.5分）：")
    insert_before("  - 5 分：建议极具实操性、针对性，能直接转化为管理动作（有明确抓手或策略）。")
    insert_before("  - 4 分：建议具备一定可行性，方向正确，但在具体落地细节上略显宽泛。")
    insert_before("  - 3 分：建议属于行业“车轱辘话”（如“加强管理”），放之四海而皆准。")
    insert_before("  - 2 分：建议不切实际，或完全无法在当前业务场景下落地。")
    insert_before("  - 1 分：未给出任何建议，或给出的建议会对业务产生负面影响。")
    
doc.save(r'test_plan\经分智能体测试方案2.0.docx')
print("Document updated successfully with 1-5 point rubrics.")
