import docx

doc = docx.Document(r'test_plan\经分智能体测试方案2.0.docx')

# The logic I used to reverse the list of lines caused them to be inserted backwards 
# above the target paragraph, or caused some other strange ordering. 
# Let's fix this properly.

# Find "三. 自动化打分与判断方法"
start_idx = -1
end_idx = -1

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if text == '三. 自动化打分与判断方法':
        start_idx = i
    elif text == '四. 核心度量指标体系 (Core Evaluation Metrics)':
        end_idx = i

if start_idx != -1 and end_idx != -1:
    # clear all between start and end
    for i in range(start_idx + 1, end_idx):
        p = doc.paragraphs[i]
        p.text = ""

    new_text = """
本方案摒弃纯人工审阅，全面拥抱自动化与智能化评估。

1. 非开放问题（硬性比对）
• 比对标准：提前基于测试数据集计算所得的绝对真理（Ground Truth）。
• 执行方法：自动化脚本对比智能体的文本输出，精准核对数字大小、排名顺序及名单是否匹配，完全匹配则得满分（5分），残缺或错误自动扣分，彻底杜绝主观偏差。

2. 开放问题（LLM-as-a-Judge 智能裁判法）
鉴于大模型（智能体）的输出为非结构化自由文本，测试方案引入高阶大模型作为自动化裁判。

核心评估理念：
忽略智能体回答的表面排版格式，纯粹穿透底层语义，考察其是否涵盖三大核心考核点：
• 事实与数据层（40%权重，满分2分）：是否精准找对底层数据，严防任何虚构或数据混用（幻觉）。
• 归纳与分析层（30%权重，满分1.5分）：是否将冷冰冰的数据转化为有业务深度的根因洞察。
• 落地与建议层（30%权重，满分1.5分）：是否输出了具备实操性、针对性的经营管理对策。

自动化测试实施路径：
1) 数据捕获：通过 RPA 脚本批量拉取智能体对 30 道开放题的实际回答，落盘至 result.xlsx 的“智能体回复”列。
2) 裁判审阅：评测脚本循环读取“用户提问 + 三段式标准答案 + 智能体实际回复”，将三者拼装进入裁判大模型的 Prompt 模板。
3) 量化定级：由裁判大模型以专家视角输出分数（1-5分）与详细的扣分理由。
4) 人工兜底 (Human-in-the-loop)：仅对裁判大模型给出异常低分（<3分）或涉嫌严重幻觉的极端 Case 触发人工介入复检。

3. 测试用例与评分展示（典型示例）
为了更直观地展示打分逻辑，以下提供了开放与非开放问题的标准范例与评分解析：

【示例 A】非开放问题（客观事实与逻辑计算）
• 测试提问：“当前总金额超千万且净利率低于 10% 的大额低利润合同共有多少个？”
• Ground Truth（系统真理）：28
• 🟢 高分回复示例（满分 5 分）：“根据系统数据查询，当前金额超千万且净利率<10%的合同共有 28 个。”
  > 自动化脚本判定：正则精准提取到核心数值 28，与 Ground Truth 完全等值匹配，自动判为满分。
• 🔴 低分回复示例（0 分）：“当前此类大额低利合同共有 25 个，主要集中在软件智能业务线。”
  > 自动化脚本判定：提取数值为 25，与事实严重不符，判定为计算错误或出现幻觉，自动判为 0 分。

【示例 B】开放问题（主观洞察与策略推演）
• 测试提问：“为什么数智运营产品线的商机转化率偏低？请结合数据给出破局建议。”
• 标准评估基准（三段式 Target）：
  1) 事实与数据：赢单率约 51.37%，排除原因 Top2 为商务条款(25个)与延期(25个)。
  2) 洞察与分析：转化偏低的核心流失原因为“项目周期拖延”与“商务价格底线未达成一致”。
  3) 落地建议：建立里程碑追踪防延期，推出模块化/分级报价方案降低商务门槛。
• 🟢 智能体高分回复示例（4.5 - 5 分）：“目前数智运营产品线赢单率徘徊在 51% 左右，主要痛点在于商务条款分歧以及项目审批延期导致大量商机流失。建议针对延期现象设立阶段停留红线并加强追踪；针对商务难点，方案团队应推出敏捷版/豪华版的梯次化报价策略，以提升最终转化。”
  > LLM裁判打分逻辑：覆盖了约 51% 的核心数据（得2分），精准指出延期与条款两项流失根因（得1.5分），给出的梯次报价与防延期追踪建议完全具备实操性（得1.5分），总计满分 5 分。
• 🔴 智能体低分回复示例（1 - 2 分）：“数智运营产品线商机转化率低主要是因为前端销售团队不够努力，产品缺乏吸引力。建议大家多跑一线跟客户沟通，了解客户真实想法，争取多签单。”
  > LLM裁判打分逻辑：完全缺失真实的系统数据支撑（扣 2 分），归因流于表面且无视真实的排除原因记录（扣 1 分），给出的建议极其宽泛空洞，属于无效的车轱辘话（扣 1 分）。总计判 1 分，系统立即触发红灯人工复检。
"""

    # We will just write all this text sequentially into the paragraphs between start and end
    # to avoid the insertion ordering issue.
    lines = [L for L in new_text.split('\n') if L.strip() != '']
    
    current_idx = start_idx + 1
    for line in lines:
        if current_idx < end_idx:
            p = doc.paragraphs[current_idx]
            p.text = line
            if line.startswith("【示例") or line.startswith("1. 非开放问题") or line.startswith("2. 开放问题") or line.startswith("3. 测试用例"):
                p.runs[0].bold = True
            current_idx += 1
        else:
            # if we run out of paragraphs, we insert before the end_idx
            p = doc.paragraphs[end_idx].insert_paragraph_before(line)
            if line.startswith("【示例") or line.startswith("1. 非开放问题") or line.startswith("2. 开放问题") or line.startswith("3. 测试用例"):
                p.runs[0].bold = True

doc.save(r'test_plan\经分智能体测试方案2.0.docx')
print("Fixed Word Document ordering issue.")
