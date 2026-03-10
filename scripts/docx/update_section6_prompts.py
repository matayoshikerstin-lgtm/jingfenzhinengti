"""
在 docx 第六节各阶段中，找到"协作内容"段落后插入"参考 Prompt"段落。
逻辑：
  - 遍历所有段落，找到包含特定阶段标志文字的段落，
  - 然后在该阶段的"协作内容"段落之后插入 Prompt 段落。
由于 python-docx 不支持任意位置插入，使用 lxml addprevious/addnext 操作。
"""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOC_PATH = "d:/jfznt/仓库/jingfenzhinengti/test_plan/经分智能体测试方案2.0.docx"
doc = Document(DOC_PATH)

def make_paragraph(text, bold=False, size_pt=11, indent_left=720):
    """创建段落 XML 元素"""
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    if indent_left > 0:
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), str(indent_left))
        pPr.append(ind)
    p.append(pPr)

    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:hint'), 'eastAsia')
    rPr.append(rFonts)
    if bold:
        b = OxmlElement('w:b')
        rPr.append(b)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(size_pt * 2))
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), str(size_pt * 2))
    rPr.append(sz); rPr.append(szCs)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    r.append(t)
    p.append(r)
    return p

def make_mixed_paragraph(label, content, size_pt=11, indent_left=720):
    """创建 [加粗标签] + [普通正文] 的混合段落"""
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    if indent_left > 0:
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), str(indent_left))
        pPr.append(ind)
    p.append(pPr)

    # 加粗部分
    r1 = OxmlElement('w:r')
    rPr1 = OxmlElement('w:rPr')
    b1 = OxmlElement('w:b'); rPr1.append(b1)
    sz1 = OxmlElement('w:sz'); sz1.set(qn('w:val'), str(size_pt * 2)); rPr1.append(sz1)
    szCs1 = OxmlElement('w:szCs'); szCs1.set(qn('w:val'), str(size_pt * 2)); rPr1.append(szCs1)
    r1.append(rPr1)
    t1 = OxmlElement('w:t'); t1.text = label
    t1.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r1.append(t1); p.append(r1)

    # 普通部分
    r2 = OxmlElement('w:r')
    rPr2 = OxmlElement('w:rPr')
    sz2 = OxmlElement('w:sz'); sz2.set(qn('w:val'), str(size_pt * 2)); rPr2.append(sz2)
    szCs2 = OxmlElement('w:szCs'); szCs2.set(qn('w:val'), str(size_pt * 2)); rPr2.append(szCs2)
    r2.append(rPr2)
    t2 = OxmlElement('w:t'); t2.text = content
    t2.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r2.append(t2); p.append(r2)
    return p

# 各阶段 Prompt 内容
stage_prompts = {
    '阶段一': (
        '我正在测试一款面向销售管理的经营分析智能体。底层数据有三张表：'
        '商机表（含商机金额、销售流程/阶段、预计签单日期、赢单率等字段）、'
        '合同表（含合同金额、净利润、最终用户名等字段）、项目表。'
        '请基于这些数据维度，帮我设计 80 道测试问题，其中 50 道非开放题'
        '（含单表查询、聚合求和、排序 TOP N、多表关联）、30 道开放题'
        '（面向老板视角，如商机卡点分析、客户风险预警）。'
        '每道题需注明数据来源字段，非开放题需提供基准答案。'
    ),
    '阶段二': (
        '现在我有真实的脱敏数据文件（fact_opportunity.csv、fact_contract.csv），'
        '数据字段如下：[粘贴字段列表]。'
        '请帮我编写 Python 脚本，依次计算以下非开放题的基准答案：[粘贴题目列表]。'
        '要求：每道题单独一个函数，输出题号和计算结果，方便我逐题核对。'
    ),
    '阶段三': (
        '请用 Playwright（Python）帮我写一个自动化测试脚本。'
        '目标系统是内网的经分智能体对话页面，已用 Edge 浏览器登录。'
        '页面结构：输入框 CSS 选择器为 [xxx]，发送按钮为 [xxx]，回复气泡为 [xxx]'
        '（流式输出，需等待文字不再变化后再提取）。'
        '脚本需读取 test_data/测试数据.xlsx 的问题列，逐题输入问题并抓取完整回复，'
        '结果追加写入 result.xlsx 的"智能体回复"列。'
        '网络超时自动重试 3 次，失败用例标注"【抓取失败】"。'
    ),
    '阶段四': (
        '请阅读工作区里的"与AI协作全过程.md"和"测试方案优化总结.md"，'
        '快速了解我们之前做过的所有工作和 RPA 测试策略。'
        '然后帮我处理 RPA 抓回来的测试结果数据：'
        '① 检查 result.xlsx，统计抓取失败用例并标注；'
        '② 编写自动化评分脚本，调用大模型 API，对开放题按"事实准确度、业务洞察力、建议可行性"三维打分（1-5分），输出分数和扣分理由；'
        '③ 非开放题用正则与 Ground Truth 对比，输出是否匹配。'
    ),
    '阶段五': (
        '请帮我优化"经分智能体测试方案2.0.md"的排版格式。'
        '要求：① 标题层级规范，# 为全局主标题，## 为章节标题，### 为子章节；'
        '② 加粗克制精准，只对核心名词和关键指标加粗，大段描述文本不加粗；'
        '③ 表格对齐使用标准 Markdown 三线表；'
        '④ 全文结构清晰，逻辑层次分明。'
    ),
}

# 找到各阶段"协作内容"段落，在其后插入 Prompt 段落
paras = doc.paragraphs
current_stage = None
inserted = {}

for i, para in enumerate(paras):
    text = para.text.strip()

    # 检测当前处于哪个阶段
    for stage_key in stage_prompts:
        if stage_key in text:
            current_stage = stage_key
            break

    # 找到"协作内容"段落且当前阶段未插入过
    if current_stage and '协作内容' in text and current_stage not in inserted:
        # 在"协作内容"段落之后、下一段之前插入 Prompt 段落
        ref_elem = para._element
        prompt_label = make_mixed_paragraph('参考 Prompt：', '', size_pt=11, indent_left=360)
        prompt_content = make_paragraph(
            stage_prompts[current_stage],
            bold=False, size_pt=10, indent_left=720
        )
        ref_elem.addnext(prompt_content)
        ref_elem.addnext(prompt_label)
        inserted[current_stage] = True
        print(f"✅ 已在 {current_stage} 的协作内容后插入 Prompt（段落 {i}）")

print(f"\n共插入 {len(inserted)} 个阶段的 Prompt。")
doc.save(DOC_PATH)
print("docx 已保存。")
