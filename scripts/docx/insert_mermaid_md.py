import os

with open(r'test_plan\经分智能体测试方案2.0.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out_lines = []
for line in lines:
    out_lines.append(line)
    if '五、 自动化与智能化测试执行流程' in line:
        out_lines.append('\n```mermaid\ngraph TD\n    classDef blue fill:#e1f5fe,stroke:#29b6f6,stroke-width:2px,color:#000;\n    classDef green fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#000;\n    classDef orange fill:#fff3e0,stroke:#ffa726,stroke-width:2px,color:#000;\n    classDef red fill:#ffebee,stroke:#ef5350,stroke-width:2px,color:#000;\n\n    A[题库构建: 80道业务问题]:::blue --> B(RPA 自动化引擎):::orange\n    B --> C[模拟人工登入内网]:::orange\n    C --> D[逐题提问并抓取回复]:::orange\n    D --> E{双轨智能交叉验证}:::blue\n    \n    E -->|非开放问题| F[脚本硬性比对: 正则提取 + Ground Truth]:::green\n    E -->|开放问题| G[LLM裁判: 事实/洞察/建议 量化打分]:::green\n    \n    F --> H[判断准确率]:::green\n    G --> I{分数 < 3 或 幻觉?}:::red\n    \n    I -->|Yes| J[触发人工兜底复检]:::red\n    I -->|No| K[通过]:::green\n    \n    H --> L((输出高维可视化测试报告)):::blue\n    J --> L\n    K --> L\n```\n\n')

with open(r'test_plan\经分智能体测试方案2.0.md', 'w', encoding='utf-8') as f:
    f.writelines(out_lines)

print("Mermaid diagram added to MD.")
