from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree
import copy
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = Document("d:/jfznt/仓库/jingfenzhinengti/test_plan/经分智能体测试方案2.0.docx")

# 找到"附录"段落索引
appendix_idx = None
for i, para in enumerate(doc.paragraphs):
    if '附录' in para.text:
        appendix_idx = i
        break

print(f"附录段落索引: {appendix_idx}")

# ---- 把附录标题改为"七、" ----
doc.paragraphs[appendix_idx].runs[0].text = doc.paragraphs[appendix_idx].runs[0].text.replace('六、', '七、')
print(f"附录已更新为: {doc.paragraphs[appendix_idx].text}")

# ---- 在附录段落前插入新章节 ----
# python-docx 不支持直接插入，需要用 XML 操作
body = doc.element.body
appendix_para_elem = doc.paragraphs[appendix_idx]._element

def make_paragraph(text, bold=False, size_pt=None, color=None, indent_level=0):
    """创建一个段落 XML 元素"""
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    # 缩进
    if indent_level > 0:
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), str(indent_level * 360))
        pPr.append(ind)
    p.append(pPr)

    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    # 字体
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:hint'), 'eastAsia')
    rPr.append(rFonts)
    # 粗体
    if bold:
        b = OxmlElement('w:b')
        rPr.append(b)
    # 字号
    if size_pt:
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(size_pt * 2))
        szCs = OxmlElement('w:szCs')
        szCs.set(qn('w:val'), str(size_pt * 2))
        rPr.append(sz)
        rPr.append(szCs)
    # 颜色
    if color:
        clr = OxmlElement('w:color')
        clr.set(qn('w:val'), color)
        rPr.append(clr)
    r.append(rPr)

    t = OxmlElement('w:t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    r.append(t)
    p.append(r)
    return p

def insert_before(ref_elem, new_elem):
    ref_elem.addprevious(new_elem)

def make_empty_line():
    return make_paragraph('')

def make_table_row(cells, bold_first=False):
    """简单文字表格行，用制表符分隔（实际表格需要更复杂的XML，这里用文本模拟）"""
    return make_paragraph('    '.join(cells))

# ---- 构建新章节内容 ----
new_elements = []

# 章节标题
new_elements.append(make_paragraph('六、 AI 辅助协作测试工程过程', bold=True, size_pt=16))
new_elements.append(make_empty_line())

# 导言
new_elements.append(make_paragraph(
    '本测试方案从零到一的构建过程，全程引入 Cursor AI（Agent 模式）作为协作工具，实现了"人机结合"的测试工程范式。以下为各阶段的协作过程与经验沉淀，供后续类似项目参考复用。',
    size_pt=11
))
new_elements.append(make_empty_line())

# 1. 协作工具与模式
new_elements.append(make_paragraph('1. 协作工具与模式', bold=True, size_pt=13))
new_elements.append(make_paragraph('工具：Cursor IDE + 内置 AI Agent（基于大模型的对话式编程助手）', size_pt=11, indent_level=1))
new_elements.append(make_paragraph('协作模式：测试工程师提需求与业务判断，AI 负责代码实现、方案草稿与文档整理', size_pt=11, indent_level=1))
new_elements.append(make_paragraph('核心价值：将原本需要数天的脚本开发与文档撰写压缩至数小时，并通过多轮对话迭代持续优化', size_pt=11, indent_level=1))
new_elements.append(make_empty_line())

# 2. 各阶段协作过程
new_elements.append(make_paragraph('2. 各阶段协作过程', bold=True, size_pt=13))
new_elements.append(make_empty_line())

stages = [
    ('阶段一：测试题库设计（需求分析 → 题目构建）',
     '协作内容：向 AI 描述业务背景（商机表、合同表、项目表的字段结构与业务含义），由 AI 辅助生成覆盖"查数、聚合、排序、归因分析、策略建议"等多种题型的测试问题集。',
     '迭代过程：初版生成后，测试工程师结合真实业务场景对题目进行筛选与修改，AI 同步调整题目措辞与难度分布，最终形成 80 道高拟真度测试题（非开放 50 题 + 开放 30 题）。',
     '关键产出：test_data/测试数据.xlsx（含问题、基准答案、三段式参考答案）'),
    ('阶段二：Ground Truth 计算（基准答案锁定）',
     '协作内容：将原始数据表结构告知 AI，由 AI 编写 Python 脚本，基于真实脱敏数据自动计算每道非开放题的绝对正确答案（Ground Truth）。',
     '迭代过程：AI 生成初版脚本后，测试工程师运行验证，对数值偏差的题目反馈给 AI 修正，最终确保 100% 基准答案与原始数据完全吻合。',
     '关键产出：scripts/data/ 目录下的系列计算脚本'),
    ('阶段三：RPA 自动化脚本开发（核心执行引擎）',
     '协作内容：向 AI 描述目标系统的页面结构（内网经分智能体对话框的 DOM 层级、流式输出特性、气泡定位方式），由 AI 使用 Playwright 编写自动化测试脚本。',
     '迭代过程：经历多轮调试——从元素定位失败、流式输出截断到异常重试机制的完善，测试工程师负责在真实环境中执行并反馈报错信息，AI 负责快速定位问题并修复代码。',
     '关键产出：scripts/rpa/run_edge_rpa.py（支持批量无人值守问答与结果自动落盘）'),
    ('阶段四：测试结果处理（数据清洗与评估）',
     '协作内容：RPA 抓取完成后，由 AI 辅助编写数据清洗脚本，对抓取失败的用例进行标记，并构建自动化评分脚本（调用 LLM 裁判接口）。',
     None,
     '关键产出：test_result/result.xlsx（含智能体回复、评分结果）、scripts/data/ 下的评分脚本'),
    ('阶段五：测试方案文档优化（本文档）',
     '协作内容：测试工程师提出文档规范要求（标题层级、加粗原则、表格格式），AI 对方案文档进行全面重排版，并根据评审反馈持续迭代优化。',
     None,
     '关键产出：test_plan/经分智能体测试方案2.0.md 及本 Word 文档'),
]

for stage_title, content1, content2, output in stages:
    new_elements.append(make_paragraph(stage_title, bold=True, size_pt=12, indent_level=1))
    new_elements.append(make_paragraph(content1, size_pt=11, indent_level=2))
    if content2:
        new_elements.append(make_paragraph(content2, size_pt=11, indent_level=2))
    new_elements.append(make_paragraph(output, size_pt=11, indent_level=2))
    new_elements.append(make_empty_line())

# 3. 协作经验总结
new_elements.append(make_paragraph('3. 协作经验总结', bold=True, size_pt=13))
new_elements.append(make_empty_line())

experiences = [
    ('业务上下文要给足', 'AI 对业务字段含义、数据结构不了解时，生成质量会明显下降。每次新开对话需先同步背景。'),
    ('反馈要具体', '描述"第3题答案算错了"不如直接贴出原始数据和期望结果，AI 修复效率更高。'),
    ('人负责判断，AI负责实现', '题目是否合理、答案是否符合业务逻辑，需由测试工程师把关；代码实现与文档整理交给 AI。'),
    ('迭代优于一次到位', '不追求 AI 第一次就完美输出，多轮对话逐步逼近目标比反复修改 Prompt 更高效。'),
    ('对话记录即知识资产', '完整的人机协作对话记录（与AI协作全过程.md）本身就是可追溯、可复盘的工程文档。'),
]

for exp_title, exp_desc in experiences:
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    ind = OxmlElement('w:ind')
    ind.set(qn('w:left'), '360')
    pPr.append(ind)
    p.append(pPr)

    # 加粗经验名
    r1 = OxmlElement('w:r')
    rPr1 = OxmlElement('w:rPr')
    b1 = OxmlElement('w:b')
    rPr1.append(b1)
    sz1 = OxmlElement('w:sz'); sz1.set(qn('w:val'), '22')
    szCs1 = OxmlElement('w:szCs'); szCs1.set(qn('w:val'), '22')
    rPr1.append(sz1); rPr1.append(szCs1)
    r1.append(rPr1)
    t1 = OxmlElement('w:t'); t1.text = f'【{exp_title}】'; t1.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r1.append(t1); p.append(r1)

    # 普通描述
    r2 = OxmlElement('w:r')
    rPr2 = OxmlElement('w:rPr')
    sz2 = OxmlElement('w:sz'); sz2.set(qn('w:val'), '22')
    szCs2 = OxmlElement('w:szCs'); szCs2.set(qn('w:val'), '22')
    rPr2.append(sz2); rPr2.append(szCs2)
    r2.append(rPr2)
    t2 = OxmlElement('w:t'); t2.text = f'  {exp_desc}'; t2.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r2.append(t2); p.append(r2)

    new_elements.append(p)

new_elements.append(make_empty_line())

# ---- 将所有新元素插入到附录段落前 ----
for elem in new_elements:
    appendix_para_elem.addprevious(elem)

# 保存
doc.save("d:/jfznt/仓库/jingfenzhinengti/test_plan/经分智能体测试方案2.0.docx")
print("docx 已更新，第六节写入完成！")
