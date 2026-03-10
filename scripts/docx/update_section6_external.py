"""
在 docx 第六节各阶段中，在"协作内容"段落前插入"所需外部协作"段落。
"""
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOC_PATH = "d:/jfznt/仓库/jingfenzhinengti/test_plan/经分智能体测试方案2.0.docx"
doc = Document(DOC_PATH)

def make_paragraph(text, bold=False, size_pt=11, indent_left=360):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    if indent_left > 0:
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), str(indent_left))
        pPr.append(ind)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts'); rFonts.set(qn('w:hint'), 'eastAsia'); rPr.append(rFonts)
    if bold:
        b = OxmlElement('w:b'); rPr.append(b)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(size_pt * 2)); rPr.append(sz)
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), str(size_pt * 2)); rPr.append(szCs)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    t.text = text
    r.append(t); p.append(r)
    return p

def make_bold_then_normal(label, content, size_pt=11, indent_left=360):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    if indent_left > 0:
        ind = OxmlElement('w:ind')
        ind.set(qn('w:left'), str(indent_left))
        pPr.append(ind)
    p.append(pPr)
    for text, bold in [(label, True), (content, False)]:
        r = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        if bold:
            b = OxmlElement('w:b'); rPr.append(b)
        sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(size_pt * 2)); rPr.append(sz)
        szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), str(size_pt * 2)); rPr.append(szCs)
        r.append(rPr)
        t = OxmlElement('w:t')
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = text
        r.append(t); p.append(r)
    return p

# 各阶段外部协作内容：(阶段标志文字, [(角色, 说明), ...])
stage_external = {
    '阶段一': [
        ('开发', '提供数据字典（各表字段名、字段含义、枚举值说明）'),
        ('产品', '提供 PRD 或业务需求文档（核心业务场景、用户角色与典型查询意图）'),
        ('业务方', '提供真实业务问题样例（"老板最常问什么"），校验题目业务合理性'),
    ],
    '阶段二': [
        ('开发', '提供脱敏后的原始数据导出文件（CSV/Excel），并确认数据口径（如金额单位、日期格式）'),
        ('开发', '如数据量大，提供数据库只读查询权限或视图，便于脚本直连验证'),
    ],
    '阶段三': [
        ('开发', '提供测试环境访问地址（内网 URL）及登录账号，说明页面关键 DOM 结构或 API 接口'),
        ('运维/IT', '提供内网 VPN 接入方式，确保自动化脚本所在机器可访问测试环境'),
    ],
    '阶段四': [
        ('开发/算法', '提供 LLM 裁判接口文档（API Key、调用格式、模型版本），或授权使用现有大模型服务'),
        ('业务方', '对裁判评分存疑的典型 Bad Case 进行人工复核，给出最终业务判断'),
    ],
    '阶段五': [
        ('产品/项目经理', '提供文档规范模板（章节结构要求、公司文档标准）'),
        ('评审人员', '对文档内容进行评审（测试负责人、业务方），提出修改意见'),
    ],
}

paras = doc.paragraphs
current_stage = None
inserted = {}

for i, para in enumerate(paras):
    text = para.text.strip()

    for stage_key in stage_external:
        if stage_key in text:
            current_stage = stage_key
            break

    # 找到"协作内容"段落且当前阶段未插入
    if current_stage and '协作内容' in text and current_stage not in inserted:
        ref_elem = para._element
        items = stage_external[current_stage]

        # 从后往前插入，保证顺序正确
        for role, desc in reversed(items):
            bullet = make_bold_then_normal(f'  {role}：', desc, size_pt=11, indent_left=720)
            ref_elem.addprevious(bullet)

        # 插入"所需外部协作："标题行
        title = make_paragraph('所需外部协作：', bold=True, size_pt=11, indent_left=360)
        ref_elem.addprevious(title)

        inserted[current_stage] = True
        print(f"✅ 已在 {current_stage} 的协作内容前插入外部协作（段落 {i}）")

print(f"\n共插入 {len(inserted)} 个阶段。")
doc.save(DOC_PATH)
print("docx 已保存。")
